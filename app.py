"""
app.py — Programa principal
Este arquivo fica hospedado no GitHub.
Quando você alterar aqui e mudar a versão no version.json,
todos os usuários receberão a atualização ao abrir o launcher.
"""

import tkinter as tk

# =============================================
#   MUDE AQUI PARA SIMULAR UMA ATUALIZAÇÃO
#   (depois suba o arquivo novo no GitHub e
#    atualize a versão no version.json)
# =============================================
APP_VERSION = "2.0.0"


def main():
    root = tk.Tk()
    root.title(f"Meu App  v{APP_VERSION}")
    root.geometry("400x300")
    root.resizable(False, False)
    root.configure(bg="#1e1e2e")

    # Título
    tk.Label(
        root,
        text="Meu Aplicativo",
        font=("Segoe UI", 18, "bold"),
        bg="#1e1e2e",
        fg="#cdd6f4"
    ).pack(pady=30)

    tk.Label(
        root,
        text=f"Versão {APP_VERSION}",
        font=("Segoe UI", 10),
        bg="#1e1e2e",
        fg="#6c7086"
    ).pack()

    # ── BOTÃO 1 (versão 1.0.0) ──────────────────
    tk.Button(
        root,
        text="🟢  Botão Original",
        font=("Segoe UI", 11),
        bg="#89b4fa",
        fg="#1e1e2e",
        relief="flat",
        padx=20,
        pady=8,
        cursor="hand2",
        command=lambda: print("Botão 1 clicado!")
    ).pack(pady=20)

    # ── BOTÃO 2 — descomente na v2.0.0 ──────────
    tk.Button(
         root,
         text="🟣  Botão Novo (v2.0.0)",
         font=("Segoe UI", 11),
         bg="#cba6f7",
         fg="#1e1e2e",
         relief="flat",
         padx=20,
         pady=8,
        cursor="hand2",
     command=lambda: print("Botão 2 clicado!")
    ).pack(pady=5)

    root.mainloop()


if __name__ == "__main__":
    main()
