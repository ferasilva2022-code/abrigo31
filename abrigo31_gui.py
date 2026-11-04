"""
ABRIGO 31 — versão com interface gráfica (tkinter, já vem com o Python).
Reaproveita os dados e o motor de dedução de abrigo31.py.
Os dois arquivos precisam estar na mesma pasta. Rode: python3 abrigo31_gui.py
"""
import tkinter as tk
from tkinter import messagebox

from abrigo31 import LOCAIS, ITENS, SUSPEITOS, CULPADO, texto, deduzir

# Paleta inspirada na apresentação (escuro, bege, âmbar)
BG, PAINEL, BEGE, AMBAR, VERDE, CINZA = "#141210", "#201d1a", "#e8d9c4", "#d9a441", "#8fbf7a", "#7a7068"
FONTE_TITULO = ("Georgia", 22, "bold")
FONTE = ("Segoe UI", 11)


class Jogo(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Abrigo 31 — Quando a Sirene Toca")
        self.geometry("1100x680")
        self.configure(bg=BG)
        self.minsize(900, 560)

        self.local = "gabinete"
        self.fatos, self.coletados = set(), set()

        self._montar_layout()
        self.narrar("1961. A neblina apaga memórias. Às 3h, a Hora Cinza tranca as portas.\n"
                    "A supervisora Vivienne Blackwood está morta. Sete suspeitos.\n"
                    "Depoimentos não são confiáveis: confie nas provas.\n", AMBAR)
        self.atualizar()

    # ------------------------------------------------------------ LAYOUT
    def _montar_layout(self):
        tk.Label(self, text="ABRIGO 31", font=FONTE_TITULO, fg=BEGE, bg=BG).pack(pady=(12, 0))
        self.lbl_local = tk.Label(self, font=("Georgia", 13, "italic"), fg=AMBAR, bg=BG)
        self.lbl_local.pack(pady=(0, 8))

        corpo = tk.Frame(self, bg=BG)
        corpo.pack(fill="both", expand=True, padx=12, pady=4)
        corpo.columnconfigure(1, weight=1)
        corpo.rowconfigure(0, weight=1)

        # Coluna 1: mapa
        self.col_mapa = self._painel(corpo, "LOCAIS", 0)
        for chave, (nome, _) in LOCAIS.items():
            self._botao(self.col_mapa, nome, lambda k=chave: self.ir(k))

        # Coluna 2: narração
        meio = tk.Frame(corpo, bg=PAINEL)
        meio.grid(row=0, column=1, sticky="nsew", padx=8)
        self.txt = tk.Text(meio, wrap="word", bg=PAINEL, fg=BEGE, font=FONTE, relief="flat",
                           padx=14, pady=12, state="disabled", cursor="arrow")
        self.txt.pack(fill="both", expand=True)
        for cor in (BEGE, AMBAR, VERDE, CINZA):
            self.txt.tag_config(cor, foreground=cor)

        # Coluna 3: itens, suspeitos, provas
        direita = tk.Frame(corpo, bg=BG)
        direita.grid(row=0, column=2, sticky="ns")
        self.col_itens = self._painel(direita, "ITENS AQUI", None)
        self.col_susp = self._painel(direita, "INTERROGAR", None)
        for chave, (nome, cargo, _) in SUSPEITOS.items():
            self._botao(self.col_susp, f"{nome.split()[0]} · {cargo}", lambda k=chave: self.interrogar(k))

        # Rodapé: progresso + acusação
        rodape = tk.Frame(self, bg=BG)
        rodape.pack(fill="x", padx=12, pady=10)
        self.lbl_prog = tk.Label(rodape, font=FONTE, fg=CINZA, bg=BG)
        self.lbl_prog.pack(side="left")
        nomes = [v[0] for v in SUSPEITOS.values()]
        self.acusado = tk.StringVar(value=nomes[0])
        menu = tk.OptionMenu(rodape, self.acusado, *nomes)
        menu.config(bg=PAINEL, fg=BEGE, activebackground=AMBAR, highlightthickness=0, font=FONTE)
        tk.Button(rodape, text="ACUSAR", command=self.acusar, bg="#8b2e24", fg="white",
                  font=("Segoe UI", 11, "bold"), relief="flat", padx=16).pack(side="right")
        menu.pack(side="right", padx=8)

    def _painel(self, pai, titulo, coluna):
        f = tk.Frame(pai, bg=PAINEL, padx=10, pady=8)
        if coluna is None:
            f.pack(fill="x", pady=(0, 8))
        else:
            f.grid(row=0, column=coluna, sticky="ns")
        tk.Label(f, text=titulo, font=("Segoe UI", 9, "bold"), fg=AMBAR, bg=PAINEL).pack(anchor="w", pady=(0, 6))
        return f

    def _botao(self, pai, texto_, comando):
        b = tk.Button(pai, text=texto_, command=comando, bg="#2c2824", fg=BEGE, font=FONTE,
                      relief="flat", anchor="w", padx=10, activebackground=AMBAR, cursor="hand2")
        b.pack(fill="x", pady=2)
        return b

    # ------------------------------------------------------------ AÇÕES
    def narrar(self, msg, cor=BEGE):
        self.txt.config(state="normal")
        self.txt.insert("end", msg + "\n", cor)
        self.txt.see("end")
        self.txt.config(state="disabled")

    def atualizar(self):
        self.lbl_local.config(text=f"Você está em: {LOCAIS[self.local][0]}")
        self.lbl_prog.config(text=f"Provas coletadas: {len(self.coletados)}/6   ·   "
                                  f"Fatos estabelecidos: {len(self.fatos)}")
        for w in self.col_itens.winfo_children()[1:]:
            w.destroy()
        itens = LOCAIS[self.local][1]
        if not itens:
            tk.Label(self.col_itens, text="Só neblina e silêncio.", fg=CINZA, bg=PAINEL, font=FONTE).pack(anchor="w")
        for i in itens:
            marca = "✔ " if i in self.coletados else "🔍 "
            self._botao(self.col_itens, marca + ITENS[i][0], lambda k=i: self.examinar(k))

    def ir(self, chave):
        self.local = chave
        self.narrar(f"\n— Você caminha até: {LOCAIS[chave][0]}", CINZA)
        self.atualizar()

    def examinar(self, chave):
        nome, pista, lit = ITENS[chave]
        self.narrar(f"\n[{nome}] {pista}")
        if lit and chave not in self.coletados:
            self.coletados.add(chave)
            self.fatos.add(lit)
            self.narrar(f"  ✔ Nova prova → {texto(lit)}", VERDE)
            for conc, regra in deduzir(self.fatos):
                self.narrar(f"  ⚙ {regra} → {texto(conc)}", AMBAR)
        self.atualizar()

    def interrogar(self, chave):
        nome, _, fala = SUSPEITOS[chave]
        self.narrar(f'\n{nome}: "{fala}"')
        self.narrar("  (a neblina torna qualquer depoimento duvidoso)", CINZA)

    def acusar(self):
        nome = self.acusado.get()
        s = next(k for k, v in SUSPEITOS.items() if v[0] == nome)
        if not messagebox.askyesno("Acusação", f"Acusar {nome}? Não há volta."):
            return
        if "C" not in self.fatos:
            messagebox.showerror("Fim", "O conselho pede PROVAS. Sua dedução ainda não sustenta a acusação.")
        elif s == CULPADO:
            messagebox.showinfo("Caso encerrado!",
                                "Scarlett Hayes manipulou o reator durante a Hora Cinza e liberou gás "
                                "tóxico no Gabinete, sem nunca entrar lá.\n\nS ∧ M ∧ G ∧ ¬L ∧ ¬A ∧ C")
        else:
            messagebox.showerror("Fim", f"{nome} não é o culpado. O assassino segue solto no abrigo.")
        self.destroy()


if __name__ == "__main__":
    Jogo().mainloop()
