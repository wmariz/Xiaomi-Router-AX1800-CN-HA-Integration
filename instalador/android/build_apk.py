"""Compila o app Android (MiWiFi Painel) sem Gradle, só com o SDK do Android.

Uso:  uv run --with pillow python instalador/android/build_apk.py
Requer: JDK (JAVA_HOME ou D:\\Android\\jdk) e Android SDK com build-tools 34 e platforms;android-34
(ANDROID_HOME ou D:\\Android\\sdk). Gera saida/MiWiFiPainel-<versão>.apk assinado.
A chave de assinatura fica em assinatura/ (fora do git); guarde-a: sem ela, uma versão nova
não instala por cima da antiga (seria preciso desinstalar antes).
"""
import os
import re
import secrets
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

from PIL import Image

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent.parent
JDK = Path(os.environ.get("JAVA_HOME", r"D:\Android\jdk"))
SDK = Path(os.environ.get("ANDROID_HOME", r"D:\Android\sdk"))
BT = SDK / "build-tools" / "34.0.0"
ANDROID_JAR = SDK / "platforms" / "android-34" / "android.jar"
EXE = ".exe" if os.name == "nt" else ""
BAT = ".bat" if os.name == "nt" else ""
VERSAO = re.search(r'versionName="([^"]+)"', (AQUI / "AndroidManifest.xml").read_text(encoding="utf-8")).group(1)
OBRA = AQUI / "obra"
SAIDA = AQUI / "saida"
ASSIN = AQUI / "assinatura"


def rodar(*args):
    env = dict(os.environ, JAVA_HOME=str(JDK))
    env["PATH"] = str(JDK / "bin") + os.pathsep + env.get("PATH", "")
    r = subprocess.run([str(a) for a in args], env=env, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout[-3000:], r.stderr[-3000:])
        sys.exit(f"falhou: {args[0]}")
    return r.stdout


def main():
    shutil.rmtree(OBRA, ignore_errors=True)
    (OBRA / "res" / "values").mkdir(parents=True)
    (OBRA / "assets").mkdir()
    SAIDA.mkdir(exist_ok=True)

    # recursos: nome e ícone (foto do AX1800, a mesma da integração)
    (OBRA / "res" / "values" / "strings.xml").write_text(
        '<?xml version="1.0" encoding="utf-8"?>\n<resources><string name="app_name">MiWiFi Painel</string></resources>\n',
        encoding="utf-8")
    foto = Image.open(RAIZ / "custom_components" / "miwifi_ax" / "brand" / "icon@2x.png").convert("RGBA")
    for pasta, px in {"mdpi": 48, "hdpi": 72, "xhdpi": 96, "xxhdpi": 144, "xxxhdpi": 192}.items():
        fundo = Image.new("RGBA", (px, px), (255, 255, 255, 255))
        mascara = Image.new("L", (px, px), 0)
        from PIL import ImageDraw
        ImageDraw.Draw(mascara).ellipse((0, 0, px - 1, px - 1), fill=255)
        icone = foto.resize((int(px * 0.78),) * 2, Image.LANCZOS)
        fundo.alpha_composite(icone, ((px - icone.width) // 2, (px - icone.height) // 2))
        fundo.putalpha(mascara)
        d = OBRA / "res" / f"mipmap-{pasta}"
        d.mkdir()
        fundo.save(d / "ic_launcher.png")

    # a mesma página do painel do PC
    shutil.copy(RAIZ / "desktop" / "painel.html", OBRA / "assets" / "painel.html")

    # recursos → apk base
    rodar(BT / f"aapt2{EXE}", "compile", "--dir", OBRA / "res", "-o", OBRA / "res.zip")
    (OBRA / "gen").mkdir()
    rodar(BT / f"aapt2{EXE}", "link", "-o", OBRA / "base.apk", "-I", ANDROID_JAR,
          "--manifest", AQUI / "AndroidManifest.xml", "-A", OBRA / "assets", "--java", OBRA / "gen",
          "--min-sdk-version", "24", "--target-sdk-version", "34", OBRA / "res.zip")

    # Java → .class → .dex
    fontes = [str(p) for p in (AQUI / "src").rglob("*.java")] + [str(p) for p in (OBRA / "gen").rglob("*.java")]
    (OBRA / "classes").mkdir()
    rodar(JDK / "bin" / f"javac{EXE}", "-source", "8", "-target", "8", "-encoding", "UTF-8", "-nowarn",
          "-bootclasspath", ANDROID_JAR, "-classpath", ANDROID_JAR, "-d", OBRA / "classes", *fontes)
    classes = [str(p) for p in (OBRA / "classes").rglob("*.class")]
    (OBRA / "dex").mkdir()
    rodar(BT / f"d8{BAT}", "--release", "--min-api", "24", "--lib", ANDROID_JAR, "--output", OBRA / "dex", *classes)

    with zipfile.ZipFile(OBRA / "base.apk", "a", zipfile.ZIP_DEFLATED) as z:
        z.write(OBRA / "dex" / "classes.dex", "classes.dex")
    rodar(BT / f"zipalign{EXE}", "-p", "-f", "4", OBRA / "base.apk", OBRA / "alinhado.apk")

    # assinatura (chave própria, guardada fora do git)
    ASSIN.mkdir(exist_ok=True)
    ks, arq_senha = ASSIN / "miwifi.jks", ASSIN / "senha.txt"
    if not ks.exists():
        arq_senha.write_text(secrets.token_urlsafe(18), encoding="utf-8")
        senha = arq_senha.read_text(encoding="utf-8").strip()
        rodar(JDK / "bin" / f"keytool{EXE}", "-genkeypair", "-keystore", ks, "-alias", "miwifi", "-keyalg", "RSA",
              "-keysize", "2048", "-validity", "10000", "-storepass", senha, "-keypass", senha,
              "-dname", "CN=MiWiFi Painel, O=wmariz")
    senha = arq_senha.read_text(encoding="utf-8").strip()
    apk = SAIDA / f"MiWiFiPainel-{VERSAO}.apk"
    rodar(BT / f"apksigner{BAT}", "sign", "--ks", ks, "--ks-pass", f"pass:{senha}", "--out", apk, OBRA / "alinhado.apk")
    print(rodar(BT / f"apksigner{BAT}", "verify", "--print-certs", apk).splitlines()[0])
    print(f"gerado: {apk} ({apk.stat().st_size / 1024:.0f} KiB)")


if __name__ == "__main__":
    main()
