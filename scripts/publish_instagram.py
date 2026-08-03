"""
publish_instagram.py - Publicacao automatica no Instagram
Rota: Instagram API with Instagram Login (graph.instagram.com)
Gerado pelo setup-instagram skill do Claude Code

Uso:
    python publish_instagram.py --images foto.png --caption "legenda"
    python publish_instagram.py --images "slides/*.png" --caption "legenda"
    python publish_instagram.py --images a.png b.png --caption "legenda" --dry-run
"""
import argparse
import glob as globlib
import os
import sys
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

# ---------------------------------------------------------------- credenciais

SCRIPT_DIR = Path(__file__).resolve().parent
ENV_FILE = None
for candidate in [SCRIPT_DIR / ".env", *(p / ".env" for p in SCRIPT_DIR.parents)]:
    if candidate.exists():
        ENV_FILE = candidate
        load_dotenv(candidate)
        break

TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN")
IG_ID = os.getenv("INSTAGRAM_BUSINESS_ID")
API_BASE = os.getenv("INSTAGRAM_API_BASE", "https://graph.instagram.com")
VERSION = os.getenv("META_API_VERSION", "v23.0")
BASE_URL = f"{API_BASE}/{VERSION}"

# Nesta rota o endpoint /me resolve a conta autenticada sem ambiguidade
# entre o ID com escopo de app e o ID de negocio.
ACCOUNT = "me"


def die(msg: str) -> None:
    print(f"\nERRO: {msg}")
    sys.exit(1)


def check_credentials() -> None:
    if not TOKEN or not IG_ID:
        die("Credenciais nao encontradas. Rode /setup-instagram primeiro.")
    resp = requests.get(
        f"{BASE_URL}/{ACCOUNT}",
        params={"fields": "username", "access_token": TOKEN},
        timeout=30,
    )
    data = resp.json()
    if "username" not in data:
        die(
            "Token invalido ou expirado.\n"
            f"Resposta da API: {data}\n"
            "Gere um novo token e atualize INSTAGRAM_ACCESS_TOKEN no .env"
        )
    print(f"  Conta autenticada: @{data['username']}")


def expand(patterns: list) -> list:
    """Expande curingas (o shell do Windows nao expande sozinho)."""
    files = []
    for pattern in patterns:
        matches = sorted(globlib.glob(pattern))
        if matches:
            files.extend(matches)
        elif Path(pattern).exists():
            files.append(pattern)
        else:
            die(f"Arquivo nao encontrado: {pattern}")
    return files


# ------------------------------------------------------------------ hospedagem

def host_image(image_path: str) -> str:
    """
    Hospeda a imagem numa URL publica via catbox.moe.

    A API do Instagram nao aceita upload de arquivo local: ela exige uma URL
    publica que os servidores da Meta consigam baixar. O catbox.moe e um host
    publico e gratuito -- a imagem fica acessivel por link a quem tiver a URL.
    """
    with open(image_path, "rb") as fh:
        resp = requests.post(
            "https://catbox.moe/user/api.php",
            data={"reqtype": "fileupload"},
            files={"fileToUpload": (Path(image_path).name, fh)},
            timeout=120,
        )
    url = resp.text.strip()
    if not url.startswith("https://"):
        die(f"Falha ao hospedar {image_path}: {url}")
    print(f"  Hospedada: {Path(image_path).name} -> {url}")
    return url


# -------------------------------------------------------------------- API calls

def create_container(image_url: str, caption: str = None, carousel_item: bool = False) -> str:
    payload = {"access_token": TOKEN, "image_url": image_url}
    if carousel_item:
        payload["is_carousel_item"] = "true"
    if caption is not None:
        payload["caption"] = caption

    resp = requests.post(f"{BASE_URL}/{ACCOUNT}/media", data=payload, timeout=120)
    result = resp.json()
    if "id" not in result:
        die(f"Falha ao criar container: {result}")
    print(f"  Container: {result['id']}")
    return result["id"]


def create_carousel(children: list, caption: str) -> str:
    resp = requests.post(
        f"{BASE_URL}/{ACCOUNT}/media",
        data={
            "access_token": TOKEN,
            "media_type": "CAROUSEL",
            "children": ",".join(children),
            "caption": caption,
        },
        timeout=60,
    )
    result = resp.json()
    if "id" not in result:
        die(f"Falha ao montar carrossel: {result}")
    print(f"  Carrossel: {result['id']}")
    return result["id"]


def wait_ready(container_id: str, tries: int = 20, delay: int = 5) -> None:
    for attempt in range(tries):
        resp = requests.get(
            f"{BASE_URL}/{container_id}",
            params={"fields": "status_code,status", "access_token": TOKEN},
            timeout=30,
        )
        data = resp.json()
        status = data.get("status_code", "")
        if status == "FINISHED":
            return
        if status == "ERROR":
            die(f"Container falhou no processamento: {data}")
        print(f"  Processando... ({attempt * delay}s)")
        time.sleep(delay)
    die("Timeout: o container nao ficou pronto a tempo.")


def publish(container_id: str) -> str:
    resp = requests.post(
        f"{BASE_URL}/{ACCOUNT}/media_publish",
        data={"access_token": TOKEN, "creation_id": container_id},
        timeout=60,
    )
    result = resp.json()
    if "id" not in result:
        die(f"Falha ao publicar: {result}")
    return result["id"]


def permalink(post_id: str) -> str:
    resp = requests.get(
        f"{BASE_URL}/{post_id}",
        params={"fields": "permalink", "access_token": TOKEN},
        timeout=30,
    )
    return resp.json().get("permalink", "(link indisponivel)")


# --------------------------------------------------------------------- fluxo

def run(patterns: list, caption: str, dry_run: bool = False) -> None:
    print(f"\n.env carregado de: {ENV_FILE}")
    check_credentials()

    images = expand(patterns)
    if len(images) > 10:
        die(f"Maximo de 10 imagens por post (recebi {len(images)}).")

    tipo = "post unico" if len(images) == 1 else f"carrossel de {len(images)} slides"
    print(f"\nModo: {tipo}")
    for img in images:
        size_kb = Path(img).stat().st_size / 1024
        print(f"  - {img} ({size_kb:.0f} KB)")
    print(f"\nLegenda ({len(caption)} caracteres):")
    print(f"  {caption[:200]}{'...' if len(caption) > 200 else ''}")

    if dry_run:
        print("\n[DRY RUN] Nada foi enviado nem publicado.")
        print("Remova --dry-run para publicar de verdade.")
        return

    print("\nPasso 1/4 - Hospedando imagens...")
    urls = [host_image(img) for img in images]

    if len(images) == 1:
        print("\nPasso 2/4 - Criando container...")
        container_id = create_container(urls[0], caption=caption)
    else:
        print("\nPasso 2/4 - Criando containers dos slides...")
        children = [create_container(u, carousel_item=True) for u in urls]
        print("\n  Montando o carrossel...")
        container_id = create_carousel(children, caption)

    print("\nPasso 3/4 - Aguardando processamento...")
    wait_ready(container_id)

    print("\nPasso 4/4 - Publicando...")
    post_id = publish(container_id)

    print("\nPublicado com sucesso!")
    print(f"  Post ID: {post_id}")
    print(f"  Link:    {permalink(post_id)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Publica imagens no Instagram.")
    parser.add_argument("--images", nargs="+", required=True, help="Arquivos ou curingas (1 a 10).")
    parser.add_argument("--caption", required=True, help="Legenda do post.")
    parser.add_argument("--dry-run", action="store_true", help="Simula sem enviar nada.")
    args = parser.parse_args()
    run(args.images, args.caption, args.dry_run)
