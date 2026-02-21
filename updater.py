"""
updater.py — Sistema de atualização
Compara a versão local com a do GitHub.
Se for diferente, baixa o novo app.py e substitui o local.
"""

import urllib.request
import json
import os
import sys

# ─────────────────────────────────────────────────────────────
#  CONFIGURE AQUI com seus dados do GitHub
# ─────────────────────────────────────────────────────────────
VERSION_URL = "https://raw.githubusercontent.com/Arthur-Almeidaa/teste-updater/main/version.json"
LOCAL_VERSION_FILE = "local_version.txt"
APP_FILE = "app.py"
# ─────────────────────────────────────────────────────────────


def get_local_version():
    """Lê a versão salva localmente (gravada após cada update)."""
    if not os.path.exists(LOCAL_VERSION_FILE):
        return "0.0.0"  # Nunca atualizou antes
    with open(LOCAL_VERSION_FILE, "r") as f:
        return f.read().strip()


def save_local_version(version):
    """Salva a versão atual no disco após um update bem-sucedido."""
    with open(LOCAL_VERSION_FILE, "w") as f:
        f.write(version)


def fetch_remote_info():
    """Busca o version.json do GitHub."""
    try:
        with urllib.request.urlopen(VERSION_URL, timeout=5) as response:
            data = json.loads(response.read().decode())
        return data  # {"version": "2.0.0", "download_url": "..."}
    except Exception as e:
        print(f"[Updater] Não foi possível verificar atualizações: {e}")
        return None


def download_update(download_url):
    """Baixa o novo app.py do GitHub e substitui o local."""
    try:
        with urllib.request.urlopen(download_url, timeout=10) as response:
            new_code = response.read()

        # Salva o novo arquivo
        with open(APP_FILE, "wb") as f:
            f.write(new_code)

        return True
    except Exception as e:
        print(f"[Updater] Erro ao baixar atualização: {e}")
        return False


def check_and_update(on_status=None):
    """
    Função principal do updater.
    
    on_status: callback opcional para atualizar a UI com mensagens.
               Recebe uma string de status.
    
    Retorna True se houve atualização, False caso contrário.
    """

    def status(msg):
        print(f"[Updater] {msg}")
        if on_status:
            on_status(msg)

    status("Verificando atualizações...")

    remote = fetch_remote_info()

    if remote is None:
        status("Sem conexão — iniciando versão atual.")
        return False

    remote_version = remote.get("version", "0.0.0")
    download_url   = remote.get("download_url", "")
    local_version  = get_local_version()

    status(f"Versão local: {local_version}  |  Versão disponível: {remote_version}")

    if remote_version == local_version:
        status("Aplicativo já está na versão mais recente!")
        return False

    # Versão diferente → atualizar
    status(f"Nova versão encontrada ({remote_version})! Baixando...")

    success = download_update(download_url)

    if success:
        save_local_version(remote_version)
        status(f"Atualizado para v{remote_version} com sucesso!")
        return True
    else:
        status("Falha no download. Iniciando versão atual.")
        return False