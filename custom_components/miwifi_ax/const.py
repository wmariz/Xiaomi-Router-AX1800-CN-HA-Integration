"""Constants of the MiWiFi AX integration."""
DOMAIN = "miwifi_ax"
PLATFORMS = ["sensor", "binary_sensor", "switch", "button", "device_tracker"]
CONF_TRACKED = "tracked_macs"
CONF_PAINEL = "painel_url"
# Mesh node that follows the main router's admin password (the Mesh copies the password to the nodes)
CONF_MESMA_SENHA = "usar_senha_principal"
# hosts of Mesh nodes the user deleted (do not re-add automatically)
CONF_NOS_REMOVIDOS = "nos_removidos"
# Zigbee-aware 2.4 GHz channel search (main router options)
CONF_CANAL_DIAS = "canal_auto_dias"  # 0 = off; 1, 3, 7, 15, 30
CONF_CANAL_HORA = "canal_auto_hora"  # 0–23
CONF_CANAL_COMPENSA = "canal_auto_compensa"  # only switch if worth it
CONF_ZIGBEE_CANAL = "zigbee_canal"  # 0 = detect from ZHA
CANAL_DIAS_OPCOES = (0, 1, 3, 7, 15, 30)
PAINEL_PADRAO = "homeassistant://roteadores"  # HA sidebar panel (alternative: http://127.0.0.1:8099/ on the PC)
SCAN_INTERVAL_S = 60
ROLE_MAIN = "principal"
ROLE_NODE = "repetidor"
CONN_TYPE = {0: "cabo", 1: "2,4 GHz", 2: "5 GHz", 3: "visitante"}
