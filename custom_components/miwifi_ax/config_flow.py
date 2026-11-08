"""Configuração pela interface: IP + senha; opções: aparelhos rastreados."""
from __future__ import annotations

from ipaddress import ip_address
from typing import Any
from urllib.parse import urlparse

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry, ConfigEntryState, ConfigFlow, ConfigFlowResult, OptionsFlow
from homeassistant.const import CONF_HOST, CONF_PASSWORD
from homeassistant.core import callback
from homeassistant.helpers import selector
from homeassistant.helpers.aiohttp_client import async_create_clientsession

from .api import MiWiFiApi, MiWiFiAuthError, MiWiFiConnError
from .const import CONF_MESMA_SENHA, CONF_NOS_REMOVIDOS, CONF_PAINEL, CONF_TRACKED, DOMAIN, PAINEL_PADRAO




class MiWiFiConfigFlow(ConfigFlow, domain=DOMAIN):
    VERSION = 1

    def __init__(self) -> None:
        self._host: str | None = None
        self._nome: str | None = None
        self._principal: str | None = None  # entry_id do principal (descoberta pela Mesh)
        self._pedir_senha = False  # a senha do principal foi recusada: pedir a senha deste

    def _esquecer_remocao(self, principal: ConfigEntry) -> None:
        """O usuário readicionou um nó que tinha apagado: volta a ser adicionado sozinho no futuro."""
        nos = principal.data.get(CONF_NOS_REMOVIDOS, [])
        if self._host in nos:
            self.hass.config_entries.async_update_entry(
                principal, data={**principal.data, CONF_NOS_REMOVIDOS: [h for h in nos if h != self._host]})

    def _host_configurado(self, host: str) -> bool:
        return any(e.data.get(CONF_HOST) == host for e in self._async_current_entries(include_ignore=False))

    async def _criar(self, host: str, senha: str, mesma: bool = False) -> tuple[ConfigFlowResult | None, str | None]:
        """Testa o login e cria a entrada. Devolve (resultado, erro)."""
        api = MiWiFiApi(async_create_clientsession(self.hass), host, senha)
        try:
            await api.login()
            st = await api.call("misystem/status")
            tm = await api.safe("misystem/sys_time")
            nm = await api.safe("misystem/router_name")
        except MiWiFiAuthError:
            return None, "invalid_auth"
        except MiWiFiConnError:
            return None, "cannot_connect"
        mac = ((st.get("hardware") or {}).get("mac") or host).upper()
        await self.async_set_unique_id(mac, raise_on_progress=False)
        self._abort_if_unique_id_configured(updates={CONF_HOST: host})
        papel = "Repetidor" if tm.get("role") == "whc_re" else "Roteador principal"
        titulo = f"{papel} ({nm.get('name') or host})"
        return self.async_create_entry(title=titulo, data={CONF_HOST: host, CONF_PASSWORD: senha, CONF_MESMA_SENHA: mesma}), None

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        errors: dict[str, str] = {}
        if user_input is not None:
            res, erro = await self._criar(user_input[CONF_HOST], user_input[CONF_PASSWORD])
            if res:
                return res
            errors["base"] = erro
        schema = vol.Schema({vol.Required(CONF_HOST, default=self._host or "192.168.0.1"): str, vol.Required(CONF_PASSWORD): str})
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)

    # ---- descoberta na rede (o principal se anuncia por UPnP/SSDP) ----
    async def async_step_ssdp(self, discovery_info) -> ConfigFlowResult:
        host = urlparse(discovery_info.ssdp_location or "").hostname
        if not host:
            return self.async_abort(reason="cannot_connect")
        try:
            if ip_address(host).version != 4:
                # o roteador também se anuncia por IPv6; o anúncio IPv4 basta (evita "descoberta" duplicada)
                return self.async_abort(reason="not_ipv4")
        except ValueError:
            pass
        if self._host_configurado(host):
            return self.async_abort(reason="already_configured")
        await self.async_set_unique_id(f"host-{host}")
        self._abort_if_unique_id_configured()
        self._host = host
        self._nome = (discovery_info.upnp or {}).get("friendlyName") or "Xiaomi Router"
        self.context["title_placeholders"] = {"nome": self._nome, "host": host}
        return await self.async_step_discovery_confirm()

    # ---- descoberta pela Mesh (nós listados na topologia do principal) ----
    async def async_step_integration_discovery(self, discovery_info: dict[str, Any]) -> ConfigFlowResult:
        host = discovery_info[CONF_HOST]
        if self._host_configurado(host):
            return self.async_abort(reason="already_configured")
        await self.async_set_unique_id(f"host-{host}")
        self._abort_if_unique_id_configured()
        self._host = host
        self._nome = discovery_info.get("nome") or "Repetidor"
        self._principal = discovery_info.get("principal")
        self.context["title_placeholders"] = {"nome": self._nome, "host": host}
        principal = self.hass.config_entries.async_get_entry(self._principal) if self._principal else None
        # Nó da Mesh: adiciona sozinho com a senha do principal (a Mesh a copia para os nós),
        # a menos que o usuário já tenha apagado este nó antes — aí só oferece o cartão.
        if principal and host not in principal.data.get(CONF_NOS_REMOVIDOS, []):
            res, erro = await self._criar(host, principal.data[CONF_PASSWORD], True)
            if res:
                return res
            if erro == "invalid_auth":
                self._pedir_senha = True
        return await self.async_step_discovery_confirm()

    async def async_step_discovery_confirm(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        errors: dict[str, str] = {}
        principal = self.hass.config_entries.async_get_entry(self._principal) if self._principal else None
        if principal is None:  # sem principal: qualquer roteador já configurado serve de sugestão de senha
            principal = next(iter(self._async_current_entries(include_ignore=False)), None)
        if user_input is not None:
            if principal and not self._pedir_senha:
                # 1º passo: só confirmar. Testa a senha do principal (a Mesh a copia para os nós);
                # a senha só é pedida se ela não funcionar.
                res, erro = await self._criar(self._host, principal.data[CONF_PASSWORD], True)
                if res:
                    self._esquecer_remocao(principal)
                    return res
                if erro == "invalid_auth":
                    self._pedir_senha = True
                    errors["base"] = "senha_principal_recusada"
                else:
                    errors["base"] = erro  # ex.: sem conexão — confirmar de novo tenta outra vez
            else:
                senha = user_input.get(CONF_PASSWORD) or ""
                if not senha:
                    errors["base"] = "invalid_auth"
                else:
                    res, erro = await self._criar(self._host, senha)
                    if res:
                        if principal:
                            self._esquecer_remocao(principal)
                        return res
                    errors["base"] = erro
        campos: dict = {}
        if not principal or self._pedir_senha:
            campos[vol.Required(CONF_PASSWORD)] = str
        return self.async_show_form(
            step_id="discovery_confirm",
            data_schema=vol.Schema(campos),
            errors=errors,
            description_placeholders={"nome": self._nome or "", "host": self._host or ""},
        )

    async def async_step_reauth(self, entry_data: dict[str, Any]) -> ConfigFlowResult:
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        # Um nó com "usar a senha do principal" já tentou a senha do principal sozinho (coordinator);
        # chegar aqui significa que ela também não serviu.
        errors: dict[str, str] = {}
        entry = self._get_reauth_entry()
        if user_input is not None:
            senha = user_input[CONF_PASSWORD]
            api = MiWiFiApi(async_create_clientsession(self.hass), entry.data[CONF_HOST], senha)
            try:
                await api.login()
            except MiWiFiAuthError:
                errors["base"] = "invalid_auth"
            except MiWiFiConnError:
                errors["base"] = "cannot_connect"
            else:
                # nós que seguem a senha do principal e falharam: tentam de novo com a senha nova
                for e in self._async_current_entries(include_ignore=False):
                    if e.entry_id != entry.entry_id and e.data.get(CONF_MESMA_SENHA) and e.state is ConfigEntryState.SETUP_ERROR:
                        self.hass.config_entries.async_schedule_reload(e.entry_id)
                return self.async_update_reload_and_abort(entry, data_updates={CONF_PASSWORD: senha})
        return self.async_show_form(
            step_id="reauth_confirm", data_schema=vol.Schema({vol.Required(CONF_PASSWORD): str}), errors=errors,
            description_placeholders={"nome": entry.title},
        )

    async def async_step_reconfigure(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        """Trocar o IP (ex.: roteador mudou de endereço)."""
        entry = self._get_reconfigure_entry()
        errors: dict[str, str] = {}
        if user_input is not None:
            api = MiWiFiApi(async_create_clientsession(self.hass), user_input[CONF_HOST], entry.data[CONF_PASSWORD])
            try:
                await api.login()
            except MiWiFiAuthError:
                errors["base"] = "invalid_auth"
            except MiWiFiConnError:
                errors["base"] = "cannot_connect"
            else:
                return self.async_update_reload_and_abort(entry, data_updates={CONF_HOST: user_input[CONF_HOST]})
        schema = vol.Schema({vol.Required(CONF_HOST, default=entry.data[CONF_HOST]): str})
        return self.async_show_form(step_id="reconfigure", data_schema=schema, errors=errors)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> OptionsFlow:
        return MiWiFiOptions()


class MiWiFiOptions(OptionsFlow):
    async def async_step_init(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        if user_input is not None:
            return self.async_create_entry(data=user_input)
        coord = self.hass.data[DOMAIN][self.config_entry.entry_id]
        devs = await coord.async_devices() if coord.role == "principal" else {}
        opts = sorted(
            ({"value": mac, "label": f"{d['nome']} · {d.get('ip') or '-'} · {mac}"} for mac, d in devs.items() if not d.get("isap")),
            key=lambda o: o["label"].lower(),
        )
        atual = [m for m in self.config_entry.options.get(CONF_TRACKED, []) if m in devs]
        campos: dict = {}
        if opts:
            campos[vol.Optional(CONF_TRACKED, default=atual)] = selector.SelectSelector(
                selector.SelectSelectorConfig(options=opts, multiple=True, mode=selector.SelectSelectorMode.DROPDOWN)
            )
        campos[vol.Optional(CONF_PAINEL, default=self.config_entry.options.get(CONF_PAINEL, PAINEL_PADRAO))] = str
        schema = vol.Schema(campos)
        return self.async_show_form(step_id="init", data_schema=schema)
