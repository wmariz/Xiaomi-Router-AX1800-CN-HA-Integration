"""Constantes da integração MiWiFi AX."""
DOMAIN = "miwifi_ax"
PLATFORMS = ["sensor", "binary_sensor", "switch", "button", "device_tracker"]
CONF_TRACKED = "tracked_macs"
CONF_PAINEL = "painel_url"
# nó Mesh que segue a senha de administração do principal (a Mesh copia a senha para os nós)
CONF_MESMA_SENHA = "usar_senha_principal"
# hosts de nós Mesh que o usuário apagou (não readicionar sozinho)
CONF_NOS_REMOVIDOS = "nos_removidos"
PAINEL_PADRAO = "homeassistant://roteadores"  # painel da barra lateral do HA (alternativa: http://127.0.0.1:8099/ no PC)
SCAN_INTERVAL_S = 60
ROLE_MAIN = "principal"
ROLE_NODE = "repetidor"
CONN_TYPE = {0: "cabo", 1: "2,4 GHz", 2: "5 GHz", 3: "visitante"}
