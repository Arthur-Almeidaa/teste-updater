"""
launcher.py — Entry point do aplicativo

Este é o único arquivo que o usuário executa (ou que vira um .exe).
Ele:
  1. Abre uma janela "Verificando atualizações..."
  2. Chama o updater em background
  3. Se houver update, mostra progresso e reinicia
  4. Se não houver, abre o app direto
"""

import tkinter as tk
import threading
import subprocess
import sys
import os
from updater import check_and_update


# ── Tela de splash (atualização) ─────────────────────────────

class SplashScreen:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Atualizando...")
        self.root.geometry("380x180")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e2e")

        # Centraliza na tela
        self.root.eval("tk::PlaceWindow . center")

        # Remove barra de título nativa (visual mais limpo)
        self.root.overrideredirect(True)

        # Borda arredondada simulada com frame
        frame = tk.Frame(self.root, bg="#313244", padx=2, pady=2)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        tk.Label(
            frame,
            text="⟳  Verificando atualizações",
            font=("Segoe UI", 13, "bold"),
            bg="#313244",
            fg="#cdd6f4"
        ).pack(pady=(20, 5))

        self.status_label = tk.Label(
            frame,
            text="Conectando ao servidor...",
            font=("Segoe UI", 9),
            bg="#313244",
            fg="#6c7086"
        )
        self.status_label.pack()

        # Barra de progresso manual (simples, sem ttk)
        self.canvas = tk.Canvas(frame, width=300, height=6, bg="#45475a",
                                 highlightthickness=0)
        self.canvas.pack(pady=15)
        self.bar = self.canvas.create_rectangle(0, 0, 0, 6, fill="#89b4fa", outline="")

        self._progress = 0

    def set_status(self, msg):
        """Atualiza o texto de status (chamado da thread de update)."""
        self.root.after(0, lambda: self.status_label.config(text=msg))

    def animate_progress(self, target, steps=20):
        """Anima a barra de progresso até o valor target (0-300)."""
        step = (target - self._progress) / steps

        def tick(i=0):
            if i >= steps:
                return
            self._progress += step
            self.canvas.coords(self.bar, 0, 0, max(0, self._progress), 6)
            self.root.after(30, lambda: tick(i + 1))

        tick()

    def close(self):
        self.root.after(0, self.root.destroy)


# ── Lógica principal ──────────────────────────────────────────

def launch_app():
    """Inicia o app.py como processo separado."""
    subprocess.Popen([sys.executable, "app.py"])


def run_updater(splash):
    """Roda o updater em uma thread separada para não travar a UI."""

    updated = [False]

    def status_callback(msg):
        splash.set_status(msg)
        # Avança a barra conforme as etapas
        if "Verificando" in msg:
            splash.animate_progress(60)
        elif "Versão local" in msg:
            splash.animate_progress(120)
        elif "Baixando" in msg:
            splash.animate_progress(200)
        elif "sucesso" in msg:
            splash.animate_progress(300)

    updated[0] = check_and_update(on_status=status_callback)

    # Progresso final
    splash.animate_progress(300)
    splash.set_status("Pronto! Abrindo o aplicativo...")

    import time
    time.sleep(0.8)  # Pausa para o usuário ver "Pronto!"

    # Fecha splash e abre o app
    splash.close()

    if updated[0]:
        # Reinicia o launcher para carregar o novo app.py
        os.execv(sys.executable, [sys.executable] + sys.argv)
    else:
        launch_app()


def main():
    splash = SplashScreen()

    # Roda o updater em background (não trava a janela)
    thread = threading.Thread(target=run_updater, args=(splash,), daemon=True)
    thread.start()

    splash.root.mainloop()


if __name__ == "__main__":
    main()