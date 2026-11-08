"""Configuração pela interface: IP + senha; opções: aparelhos rastreados."""
from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry, ConfigFlow, ConfigFlowResult, OptionsFlow
from homeassistant.const import CONF_HOST, CONF_PASSWORD
from homeassistant.core import callback
from homeassistant.helpers import selector
from homeassistant.helpers.aiohttp_client import async_create_clientsession

from .api import MiWiFiApi, MiWiFiAuthError, MiWiFiConnError
from .const import CONF_PAINEL, CONF_TRACKED, DOMAIN, PAINEL_PADRAO


class MiWiFiConfigFlow(ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        errors: dict[str, str] = {}
        if user_input is not None:
            api = MiWiFiApi(async_create_clientsession(self.hass), user_input[CONF_HOST], user_input[CONF_PASSWORD])
            try:
                await api.login()
                st = await api.call("misystem/status")
                tm = await api.safe("misystem/sys_time")
                nm = await api.safe("misystem/router_name")
            except MiWiFiAuthError:
                errors["base"] = "invalid_auth"
            except MiWiFiConnError:
                errors["base"] = "cannot_connect"
            else:
                mac = ((st.get("hardware") or {}).get("mac") or user_input[CONF_HOST]).upper()
                await self.async_set_unique_id(mac)
                self._abort_if_unique_id_configured(updates={CONF_HOST: user_input[CONF_HOST]})
                papel = "Repetidor" if tm.get("role") == "whc_re" else "Roteador principal"
                titulo = f"{papel} ({nm.get('name') or user_input[CONF_HOST]})"
                return self.async_create_entry(title=titulo, data=user_input)
        schema = vol.Schema({vol.Required(CONF_HOST, default="192.168.0.1"): str, vol.Required(CONF_PASSWORD): str})
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)

    async def async_step_reauth(self, entry_data: dict[str, Any]) -> ConfigFlowResult:
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        errors: dict[str, str] = {}
        entry = self._get_reauth_entry()
        if user_input is not None:
            api = MiWiFiApi(async_create_clientsession(self.hass), entry.data[CONF_HOST], user_input[CONF_PASSWORD])
            try:
                await api.login()
            except MiWiFiAuthError:
                errors["base"] = "invalid_auth"
            except MiWiFiConnError:
                errors["base"] = "cannot_connect"
            else:
                return self.async_update_reload_and_abort(entry, data_updates={CONF_PASSWORD: user_input[CONF_PASSWORD]})
        return self.async_show_form(step_id="reauth_confirm", data_schema=vol.Schema({vol.Required(CONF_PASSWORD): str}), errors=errors)

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
