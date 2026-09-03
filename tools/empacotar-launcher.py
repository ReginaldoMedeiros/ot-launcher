# -*- coding: utf-8 -*-
"""
Empacota o launcher PrimeOT pronto pra enviar ao tester.

Uso: python tools/empacotar-launcher.py

Saida: D:/Otserver/_dist/PrimeOT-Launcher.zip
Conteudo: PrimeOT-Launcher.exe + as DLLs (Ionic.Zip, Newtonsoft.Json).
O tester extrai numa pasta vazia e abre o exe; o launcher cria a pasta do
client e baixa tudo sozinho.
"""
import os, shutil, zipfile

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BIN = os.path.join(REPO_ROOT, "bin", "Release")
OUT_DIR = r"D:\Otserver\_dist\PrimeOT-Launcher"
OUT_ZIP = r"D:\Otserver\_dist\PrimeOT-Launcher.zip"

FILES = [
    ("CanaryLauncher.exe", "PrimeOT-Launcher.exe"),
    ("Ionic.Zip.dll", "Ionic.Zip.dll"),
    ("Newtonsoft.Json.dll", "Newtonsoft.Json.dll"),
]

def main():
    exe = os.path.join(BIN, "CanaryLauncher.exe")
    if not os.path.exists(exe):
        raise SystemExit(f"ERRO: build nao encontrado em {BIN} (compile em Release antes)")

    if os.path.exists(OUT_DIR):
        shutil.rmtree(OUT_DIR)
    os.makedirs(OUT_DIR)

    for src, dst in FILES:
        s = os.path.join(BIN, src)
        if not os.path.exists(s):
            raise SystemExit(f"ERRO: falta {s}")
        shutil.copy2(s, os.path.join(OUT_DIR, dst))

    # LEIA-ME curto pro tester
    with open(os.path.join(OUT_DIR, "LEIA-ME.txt"), "w", encoding="utf-8") as f:
        f.write(
            "PrimeOT Launcher\n"
            "================\n\n"
            "1. Extraia esta pasta em qualquer lugar (ex.: Desktop).\n"
            "2. Abra PrimeOT-Launcher.exe.\n"
            "3. Ele baixa o client e os graficos sozinho (a 1a vez demora, ~130MB de assets).\n"
            "4. Clique em PLAY, digite email e senha, entre.\n\n"
            "IMPORTANTE (alpha): mantenha o Tailscale conectado — o servidor so existe\n"
            "na rede privada. Sem Tailscale o PLAY nao conecta no jogo.\n"
        )

    if os.path.exists(OUT_ZIP):
        os.remove(OUT_ZIP)
    with zipfile.ZipFile(OUT_ZIP, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(OUT_DIR):
            for fn in files:
                full = os.path.join(root, fn)
                zf.write(full, os.path.relpath(full, OUT_DIR))

    size_mb = os.path.getsize(OUT_ZIP) / 1048576
    print(f"OK: {OUT_ZIP}  ({size_mb:.2f} MB)")

if __name__ == "__main__":
    main()
