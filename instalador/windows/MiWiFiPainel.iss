; Installer for the local panel of Xiaomi AX1800 (RM1800) routers
; Build:  ISCC.exe MiWiFiPainel.iss   (after creating dist\MiWiFiPainel.exe with PyInstaller — see build.ps1)

#define Nome "MiWiFi Painel"
#define Versao "1.1.2"
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
ShowLanguageDialog=auto
LanguageDetectionMethod=uilanguage

[Languages]
; English first = default when Windows is not in Portuguese
Name: "en"; MessagesFile: "compiler:Default.isl"
Name: "ptbr"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[CustomMessages]
en.Atalho=Create a desktop shortcut
en.Atalhos=Shortcuts:
en.Iniciar=Start the panel with Windows (without opening the browser)
en.Opcional=Optional:
en.Comentario=Xiaomi AX1800 routers panel
en.Desinstalar=Uninstall
en.AbrirAgora=Open {#Nome} now
ptbr.Atalho=Criar atalho na área de trabalho
ptbr.Atalhos=Atalhos:
ptbr.Iniciar=Iniciar o painel junto com o Windows (sem abrir o navegador)
ptbr.Opcional=Opcional:
ptbr.Comentario=Painel dos roteadores Xiaomi AX1800
ptbr.Desinstalar=Desinstalar
ptbr.AbrirAgora=Abrir o {#Nome} agora

[Tasks]
Name: "atalho"; Description: "{cm:Atalho}"; GroupDescription: "{cm:Atalhos}"
Name: "iniciar"; Description: "{cm:Iniciar}"; GroupDescription: "{cm:Opcional}"; Flags: unchecked

[Files]
Source: "dist\{#Exe}"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#Nome}"; Filename: "{app}\{#Exe}"; Comment: "{cm:Comentario}"
Name: "{group}\{cm:Desinstalar} {#Nome}"; Filename: "{uninstallexe}"
Name: "{userdesktop}\{#Nome}"; Filename: "{app}\{#Exe}"; Tasks: atalho
Name: "{userstartup}\{#Nome}"; Filename: "{app}\{#Exe}"; Parameters: "--sem-navegador"; Tasks: iniciar

[Run]
Filename: "{app}\{#Exe}"; Description: "{cm:AbrirAgora}"; Flags: nowait postinstall skipifsilent

[UninstallRun]
Filename: "{sys}\taskkill.exe"; Parameters: "/f /im {#Exe}"; Flags: runhidden; RunOnceId: "EncerrarPainel"

[UninstallDelete]
; the configuration (router addresses) lives in %APPDATA%\MiWiFiPainel and is kept
Type: filesandordirs; Name: "{app}"

