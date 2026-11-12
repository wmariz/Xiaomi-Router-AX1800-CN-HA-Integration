"""Constants of the MiWiFi AX integration."""
DOMAIN = "miwifi_ax"
PLATFORMS = ["sensor", "binary_sensor", "switch", "button", "device_tracker"]
CONF_TRACKED = "tracked_macs"
CONF_PAINEL = "painel_url"
# Mesh node that follows the main router's admin password (the Mesh copies the password to the nodes)
CONF_MESMA_SENHA = "usar_senha_principal"
# hosts of Mesh nodes the user deleted (do not re-add automatically)
CONF_NOS_REMOVIDOS = "nos_removidos"
# options of the removed Zigbee-aware channel search (dropped from existing entries on setup)
OPCOES_CANAL_ANTIGAS = ("canal_auto_dias", "canal_auto_hora", "canal_auto_compensa", "zigbee_canal")
PAINEL_PADRAO = "homeassistant://roteadores"  # HA sidebar panel (alternative: http://127.0.0.1:8099/ on the PC)
SCAN_INTERVAL_S = 60
ROLE_MAIN = "principal"
ROLE_NODE = "repetidor"
CONN_TYPE = {0: "cabo", 1: "2,4 GHz", 2: "5 GHz", 3: "visitante"}
