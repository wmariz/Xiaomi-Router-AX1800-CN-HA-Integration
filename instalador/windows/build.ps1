# Builds MiWiFiPainel.exe (PyInstaller) and the installer (Inno Setup 6).
# Usage (from the repository root):  powershell -File instalador\windows\build.ps1
$ErrorActionPreference = "Stop"
$raiz = Resolve-Path "$PSScriptRoot\..\.."
Push-Location $PSScriptRoot
uv run --quiet --with pillow python -c "from PIL import Image; Image.open(r'$raiz\custom_components\miwifi_ax\brand\icon@2x.png').convert('RGBA').save('miwifi.ico', sizes=[(16,16),(24,24),(32,32),(48,48),(64,64),(128,128),(256,256)])"
uv run --quiet --with pyinstaller pyinstaller --noconfirm --clean --onefile --noconsole --name MiWiFiPainel `
  --icon "$PSScriptRoot\miwifi.ico" --add-data "$raiz\desktop\painel.html;." `
  --distpath dist --workpath build --specpath build "$raiz\desktop\painel.py"
$iscc = @("$env:LOCALAPPDATA\Programs\Inno Setup 6\ISCC.exe", "${env:ProgramFiles(x86)}\Inno Setup 6\ISCC.exe", "$env:ProgramFiles\Inno Setup 6\ISCC.exe") | Where-Object { Test-Path $_ } | Select-Object -First 1
& $iscc /Q MiWiFiPainel.iss
Get-ChildItem saida
Pop-Location
