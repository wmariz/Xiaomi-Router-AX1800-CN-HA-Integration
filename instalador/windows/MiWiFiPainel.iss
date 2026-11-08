; Instalador do painel local dos roteadores Xiaomi AX1800 (RM1800)
; Compilar:  ISCC.exe MiWiFiPainel.iss   (depois de gerar dist\MiWiFiPainel.exe com o PyInstaller — ver build.ps1)

#define Nome "MiWiFi Painel"
#define Versao "1.0.0"
#define Exe "MiWiFiPainel.exe"

[Setup]
AppId={{94E12D9A-7E3C-4E73-B62C-3FD35C482FAF}
AppName={#Nome}
AppVersion={#Versao}
AppPublisher=wmariz
AppPublisherURL=https://github.com/wmariz/Xiaomi-Router-AX1800-CN-HA-Integration
DefaultDirName={localappdata}\Programs\{#Nome}
DefaultGroupName={#Nome}
DisableProgramGroupPage=yes
PrivilegesRequired=lowest
OutputDir=saida
OutputBaseFilename=MiWiFiPainel-Setup-{#Versao}
SetupIconFile=miwifi.ico
UninstallDisplayIcon={app}\{#Exe}
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
CloseApplications=yes

[Languages]
Name: "ptbr"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Tasks]
Name: "atalho"; Description: "Criar atalho na área de trabalho"; GroupDescription: "Atalhos:"
Name: "iniciar"; Description: "Iniciar o painel junto com o Windows (sem abrir o navegador)"; GroupDescription: "Opcional:"; Flags: unchecked

[Files]
Source: "dist\{#Exe}"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#Nome}"; Filename: "{app}\{#Exe}"; Comment: "Painel dos roteadores Xiaomi AX1800"
Name: "{group}\Desinstalar {#Nome}"; Filename: "{uninstallexe}"
Name: "{userdesktop}\{#Nome}"; Filename: "{app}\{#Exe}"; Tasks: atalho
Name: "{userstartup}\{#Nome}"; Filename: "{app}\{#Exe}"; Parameters: "--sem-navegador"; Tasks: iniciar

[Run]
Filename: "{app}\{#Exe}"; Description: "Abrir o {#Nome} agora"; Flags: nowait postinstall skipifsilent

[UninstallRun]
Filename: "{sys}\taskkill.exe"; Parameters: "/f /im {#Exe}"; Flags: runhidden; RunOnceId: "EncerrarPainel"

[UninstallDelete]
; a configuração (endereços dos roteadores) fica em %APPDATA%\MiWiFiPainel e é mantida
Type: filesandordirs; Name: "{app}"

