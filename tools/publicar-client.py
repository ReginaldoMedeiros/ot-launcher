# -*- coding: utf-8 -*-
"""
Publica uma versao nova do client para o launcher PrimeOT.

Uso:
    python tools/publicar-client.py <versao> <pasta_do_client>
Ex.:
    python tools/publicar-client.py 1.0.0 D:/Otserver/_dist/CrystalClient

O que faz:
  1. Zipa a pasta do client SEM data/things (sprites da CipSoft) -> zip legal.
     O client baixa os assets sozinho do dudantas/tibia-client (client_assets).
  2. Calcula o SHA256 do zip.
  3. Cria/atualiza o Release no GitHub (repo ot-launcher) com o zip como asset.
  4. Reescreve o launcher_config.json (versao, URL, checksum) e faz commit + push.

Requisitos: gh CLI autenticado; rodar de dentro do repo ot-launcher.
"""
import sys, os, json, hashlib, subprocess, zipfile, io

REPO = "ReginaldoMedeiros/ot-launcher"
# raiz do repo = pai da pasta tools/
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def run(cmd, **kw):
    print("  $", " ".join(cmd))
    return subprocess.run(cmd, check=True, **kw)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def make_zip(client_dir, zip_path):
    """Zipa client_dir na raiz do zip, excluindo data/things."""
    exclude = {os.path.normpath(os.path.join(client_dir, "data", "things"))}
    if os.path.exists(zip_path):
        os.remove(zip_path)
    n = 0
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(client_dir):
            dirs[:] = [d for d in dirs
                       if os.path.normpath(os.path.join(root, d)) not in exclude]
            for f in files:
                full = os.path.join(root, f)
                zf.write(full, os.path.relpath(full, client_dir))
                n += 1
    return n


def gh_release(tag, zip_path, version):
    """Cria o release; se a tag ja existir, faz upload com --clobber."""
    try:
        run(["gh", "release", "create", tag, zip_path,
             "-R", REPO, "-t", tag, "-n", f"Client PrimeOT {version} (engine, sem assets CipSoft)"])
    except subprocess.CalledProcessError:
        print("  (release ja existe? tentando upload --clobber)")
        run(["gh", "release", "upload", tag, zip_path, "-R", REPO, "--clobber"])


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    version, client_dir = sys.argv[1], sys.argv[2]
    if not os.path.exists(os.path.join(client_dir, "otclient.exe")):
        print(f"ERRO: otclient.exe nao encontrado em {client_dir}")
        sys.exit(1)

    tag = f"client-v{version}"
    zip_name = f"client_{version}.zip"
    zip_path = os.path.join(REPO_ROOT, zip_name)

    print(f"[1/5] Zipando {client_dir} (sem data/things)...")
    n = make_zip(client_dir, zip_path)
    size_mb = os.path.getsize(zip_path) / 1048576
    print(f"      {n} arquivos, {size_mb:.1f} MB -> {zip_name}")

    print("[2/5] SHA256...")
    digest = sha256(zip_path)
    print("      ", digest)

    print("[3/5] Publicando release no GitHub...")
    gh_release(tag, zip_path, version)
    url = f"https://github.com/{REPO}/releases/download/{tag}/{zip_name}"

    print("[4/5] Atualizando launcher_config.json...")
    cfg_path = os.path.join(REPO_ROOT, "launcher_config.json")
    cfg = json.load(io.open(cfg_path, encoding="utf-8"))
    cfg["clientVersion"] = version
    cfg["newClientUrl"] = url
    cfg["clientChecksum"] = digest
    io.open(cfg_path, "w", encoding="utf-8").write(
        json.dumps(cfg, indent=2, ensure_ascii=False) + "\n")

    print("[5/5] Commit + push do config...")
    run(["git", "-C", REPO_ROOT, "add", "launcher_config.json"])
    run(["git", "-C", REPO_ROOT, "commit", "-m", f"release: client v{version} ({digest[:12]})"])
    run(["git", "-C", REPO_ROOT, "push", "origin", "main"])

    # limpa o zip local (ja esta no release)
    try:
        os.remove(zip_path)
    except OSError:
        pass
    print(f"\nOK: client v{version} publicado.\n  URL: {url}\n  SHA256: {digest}")


if __name__ == "__main__":
    main()
