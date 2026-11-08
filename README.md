# Xiaomi Router AX1800

Controle local completo dos roteadores **Xiaomi Mi Router AX1800 (RM1800)**, inclusive em rede **Mesh** (principal + repetidor), sem depender da nuvem nem do app chinês.

O projeto tem duas partes, que usam a mesma API local (LuCI) do roteador:

| Parte | Pasta | O que é |
|---|---|---|
| Integração do Home Assistant | `custom_components/miwifi_ax` | Cria um **dispositivo** por roteador com sensores, interruptores, botões e rastreamento de presença, e o painel **Roteadores** na barra lateral |
| Painel do PC | `desktop/` | A mesma interface do painel do HA, rodando sozinha no PC — útil quando o HA ou a rede estão com problema |

A interface (em português, no estilo da original, com **todas** as funções — inclusive as que o firmware esconde) é uma só: `desktop/painel.html`. O painel do HA é gerado a partir dela por `python tools/build_ha_panel.py`.

## Integração do Home Assistant

### Instalação
1. Copie `custom_components/miwifi_ax` para `/config/custom_components/` (ou adicione este repositório no HACS como *repositório personalizado*, tipo *Integração*).
2. Reinicie o Home Assistant.
3. **Configurações → Dispositivos e serviços → Adicionar integração → "Xiaomi Router AX1800"**.
4. Informe o IP e a senha de administrador. Repita para cada roteador da Mesh — o papel (principal/repetidor) é detectado sozinho.
5. Em **Configurar** (no principal): escolha os aparelhos a rastrear (presença) e o endereço do painel usado pelo botão *Visitar*.

### Entidades
- **Sensores:** ligado há, processador, memória, clientes por banda, canais, largura, potência, firmware, hora do roteador e diferença do relógio, aparelhos online/conhecidos, aparelhos por conexão (cabo / 2,4 GHz / 5 GHz / visitante — com a lista nos atributos), reservas de IP (lista nos atributos), filtro de MAC, intrusões bloqueadas, IP público, IPv6, gateway, DNS, internet conectada há, download/upload agora, picos e totais.
- **Sensores binários:** internet, cabo da operadora, repetidor na Mesh, atualização de firmware, Wi-Fi 2,4/5 GHz, Wi-Fi unificado, anti-intrusos, firewalls, WPS.
- **Interruptores:** LED (principal e repetidor), QoS, rede de visitante, MU-MIMO, modo de compatibilidade Wi-Fi 5, conexão rápida, varredura AIoT, prioridade para muitos aparelhos, filtro de MAC.
- **Botões:** reiniciar, atualizar dados.
- **Rastreamento:** aparelhos escolhidos (online/offline, IP, conexão, velocidade).
- **Serviço** `miwifi_ax.definir_internet` (`mac`, `liberar`): bloqueia/libera a internet de um aparelho.

Por padrão só ficam **ativadas** *Internet* (principal) e *Reiniciar* (cada roteador); as demais vêm **desativadas** — ative só o que for usar. A integração consulta no roteador apenas o que alguma entidade ativada precisa (menos tráfego e menos gravações no banco). A verificação de firmware, que consulta os servidores da Xiaomi, roda no máximo a cada 6 h.

### Painel "Roteadores" (barra lateral)
Aparece para administradores. Usa o login já guardado pela integração (não pede senha), funciona no app do HA e fora de casa. O botão **Visitar** da página do dispositivo abre o painel já no roteador certo (configurável nas opções — pode apontar para o painel do PC).

## Painel do PC

```bash
python desktop/painel.py
```

Abre em `http://127.0.0.1:8099` (só escuta neste computador). A senha de administrador é digitada na própria página, vai direto ao roteador (mesmo método da interface oficial) e **não é gravada**. Os endereços dos roteadores são configuráveis pelo botão **⚙ Roteadores** (salvos em `%APPDATA%\MiWiFiPainel`). Toda alteração pede confirmação.

Funções ocultas expostas: rede de visitante, desconexão de aparelhos com sinal fraco, varredura AIoT, prioridade para muitos aparelhos, região do Wi-Fi, fuso sem horário de verão, bloqueio de internet por aparelho e chamada direta a todas as funções internas.

## Notas técnicas

O registro completo das descobertas (API, funções ocultas, app oficial, armadilhas) está em [`docs/DESCOBERTAS.md`](docs/DESCOBERTAS.md).

- Login: `nonce = 0_<deviceId>_<timestamp>_<aleatório>`, senha enviada como `sha1(nonce + sha1(senha + chave))`, `POST /cgi-bin/luci/api/xqsystem/login` → `stok`.
- Rede de visitante: `xqnetwork/set_wifi` com `wifiIndex=3` (bloco comentado na interface do firmware).
- LED: `misystem/led?on=0|1`.
- O fuso "(UTC−3) Brasília" do firmware aplica o horário de verão antigo; use "(UTC−3) Fortaleza".
- Reinício agendado e configuração da rede de visitante pelo app oficial passam pela nuvem da Xiaomi.

Testado com firmware 1.0.399 (versão chinesa). Projeto não oficial, sem relação com a Xiaomi. Use por sua conta e risco.
