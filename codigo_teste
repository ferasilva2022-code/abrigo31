"""
ABRIGO 31 — Quando a Sirene Toca
Jogo de detetive em texto baseado na apresentação do grupo.
Coleta provas -> cada prova vira uma proposição lógica -> o motor de dedução
aplica as regras (Modus Ponens, Silogismo Disjuntivo...) até chegar ao culpado.
"""

# ---------------------------------------------------------------- PROPOSIÇÕES
PROP = {
    "P": "Portas trancadas durante a Hora Cinza",
    "Q": "Vivienne morreu durante a Hora Cinza",
    "R": "O culpado entrou no Gabinete",
    "S": "O culpado acionou o mecanismo remotamente",
    "L": "Dante usou a chave mestra",
    "M": "Scarlett manipulou o reator",
    "G": "O registro das portas apresentou anomalia",
    "A": "Axel subiu à superfície",
    "B": "Dosímetro de Axel acima do limite",
    "C": "Scarlett é a culpada",
}

# ------------------------------------------------------------- PERSONAGENS
SUSPEITOS = {
    "adrian":   ("Adrian Keller", "médico",
                 "Sim, faltam doses de soro. Mas eu passei a Hora Cinza na Enfermaria."),
    "scarlett": ("Scarlett Hayes", "engenheira",
                 "O reator? Eu só fiz a manutenção de rotina... acho. A neblina confunde tudo."),
    "dante":    ("Dante Mercer", "chefe de segurança",
                 "A chave mestra nunca saiu do cofre. Confira o lacre se quiser."),
    "raven":    ("Raven Sinclair", "operadora de rádio",
                 "Captei algo às 3h07. Está no rádio portátil. Ouça você mesmo."),
    "elias":    ("Elias Crowe", "líder religioso",
                 "Discuti com ela, sim. Mas a Hora Cinza é um julgamento, não um crime."),
    "axel":     ("Axel 'Rust' Carter", "explorador",
                 "Não subi nessa noite. Se quiser, olha meu dosímetro."),
    "violet":   ("Violet Ashford", "encarregada do estoque",
                 "Mexi nos registros de suprimentos, e daí? Isso não mata ninguém."),
}
CULPADO = "scarlett"

# --------------------------------------------- ITENS (cada um revela um fato)
ITENS = {
    "registro":  ("Registro automático das portas",
                  "Entre 3h00 e 3h20 todas as portas ficaram trancadas.", "P"),
    "radio":     ("Rádio portátil",
                  "Gravação das 3h07: Vivienne pede socorro em plena Hora Cinza.", "Q"),
    "pe_cabra":  ("Pé de cabra",
                  "Limpo, sem marcas. A porta do Gabinete nunca foi forçada.", "~R"),
    "chave":     ("Chave mestra",
                  "Encontrada no cofre da segurança com o lacre intacto.", "~L"),
    "dosimetro": ("Dosímetro pessoal de Axel",
                  "Leitura normal: abaixo do limite de radiação.", "~B"),
    "diario":    ("Diário da supervisora",
                  "'O registro das portas mostrou anomalias de novo. Alguém mexe nos sistemas.'", "G"),
    "seringa":   ("Seringa antirradiação",
                  "Soro comum. Não foi isso que a matou.", None),          # pista falsa
    "mascara":   ("Máscara de gás",
                  "Cheiro forte de gás tóxico perto do duto do reator.", None),
}

# ------------------------------------------------------------------- LOCAIS
LOCAIS = {
    "gabinete":  ("Gabinete da Supervisora", ["registro", "diario"]),
    "reator":    ("Sala do Reator", ["mascara"]),
    "enfermaria":("Enfermaria", ["seringa"]),
    "radio":     ("Sala de Rádio", ["radio"]),
    "capela":    ("Capela", ["chave"]),
    "estufa":    ("Estufa Hidropônica", []),
    "escotilha": ("Escotilha de Superfície", ["dosimetro"]),
    "deposito":  ("Depósito", ["pe_cabra"]),
}

# ------------------------------------------------ REGRAS DE INFERÊNCIA
# (precisa_de, conclusão, nome da regra) — premissas 2, 4, 5, 7 e 8 já embutidas
REGRAS = [
    ({"P", "Q"},  "RvS", "Modus Ponens (P∧Q → R∨S)"),
    ({"RvS", "~R"}, "S", "Silogismo Disjuntivo"),
    ({"S"},       "LvM", "Modus Ponens (S → L∨M)"),
    ({"LvM", "~L"}, "M", "Silogismo Disjuntivo"),
    ({"M"},       "C",   "Modus Ponens (M → C)"),
    ({"~B"},      "~A",  "Modus Tollens (A → B, ¬B)"),
    ({"LvM"},     "G",   "Dilema Construtivo ((L→G)∧(M→G))"),
]


def texto(lit):
    if lit in ("RvS", "LvM"):
        a, b = lit.split("v")
        return f"{lit[0]} ∨ {lit[2]}: {PROP[a]} OU {PROP[b]}"
    neg = lit.startswith("~")
    base = PROP[lit.lstrip("~")]
    return f"{'¬' if neg else ''}{lit.lstrip('~')}: {'NÃO: ' if neg else ''}{base}"


def deduzir(fatos):
    novos = []
    mudou = True
    while mudou:
        mudou = False
        for precisa, conclusao, nome in REGRAS:
            if precisa <= fatos and conclusao not in fatos:
                fatos.add(conclusao)
                novos.append((conclusao, nome))
                mudou = True
    return novos


def escolher(titulo, opcoes):
    print(f"\n{titulo}")
    chaves = list(opcoes)
    for i, k in enumerate(chaves, 1):
        print(f"  {i}. {opcoes[k]}")
    print("  0. Voltar")
    resp = input("> ").strip()
    if resp.isdigit() and 1 <= int(resp) <= len(chaves):
        return chaves[int(resp) - 1]
    return None


def jogar():
    print("=" * 60)
    print("ABRIGO 31 — Quando a Sirene Toca".center(60))
    print("=" * 60)
    print("1961. A neblina apaga memórias. Às 3h a Hora Cinza tranca as portas.")
    print("A supervisora Vivienne Blackwood está morta. Sete suspeitos.")
    print("Depoimentos não são confiáveis: confie nas provas.\n")

    local = "gabinete"
    fatos, coletados = set(), set()

    while True:
        nome_local, itens = LOCAIS[local]
        print(f"\n--- Você está em: {nome_local} ---")
        acao = escolher("O que fazer?", {
            "examinar": "Examinar itens do local",
            "ir": "Ir para outro local",
            "interrogar": "Interrogar suspeito",
            "provas": "Ver provas e deduções",
            "acusar": "Fazer a acusação",
            "sair": "Sair",
        })

        if acao == "examinar":
            disponiveis = {i: ITENS[i][0] for i in itens}
            if not disponiveis:
                print("Nada de útil aqui. Só neblina e silêncio.")
                continue
            item = escolher("Examinar o quê?", disponiveis)
            if item:
                nome, pista, lit = ITENS[item]
                print(f"\n[{nome}] {pista}")
                if lit and item not in coletados:
                    coletados.add(item)
                    fatos.add(lit)
                    print(f"  ✔ Nova prova: {texto(lit)}")
                    for conc, regra in deduzir(fatos):
                        print(f"  ⚙ Dedução ({regra}): {texto(conc)}")

        elif acao == "ir":
            destino = escolher("Para onde?", {k: v[0] for k, v in LOCAIS.items()})
            local = destino or local

        elif acao == "interrogar":
            s = escolher("Quem?", {k: f"{v[0]} ({v[1]})" for k, v in SUSPEITOS.items()})
            if s:
                print(f'\n{SUSPEITOS[s][0]}: "{SUSPEITOS[s][2]}"')
                print("  (a neblina torna qualquer depoimento duvidoso)")

        elif acao == "provas":
            print("\nFATOS ESTABELECIDOS:")
            for f in sorted(fatos):
                print("  •", texto(f))
            print(f"\nProvas coletadas: {len(coletados)}/6")

        elif acao == "acusar":
            s = escolher("Quem é o culpado?", {k: v[0] for k, v in SUSPEITOS.items()})
            if not s:
                continue
            if "C" not in fatos:
                print("\nO conselho pede PROVAS. Sua dedução ainda não sustenta a acusação.")
                print("Você foi afastado da investigação. FIM.")
            elif s == CULPADO:
                print("\nCaso encerrado! Scarlett Hayes manipulou o reator durante a")
                print("Hora Cinza e liberou gás tóxico no Gabinete, sem nunca entrar lá.")
                print("Conclusão: S ∧ M ∧ G ∧ ¬L ∧ ¬A ∧ C. VOCÊ VENCEU.")
            else:
                print(f"\nVocê acusou {SUSPEITOS[s][0]}, mas a lógica aponta para outra pessoa.")
                print("O verdadeiro culpado continua solto no abrigo. FIM.")
            break

        elif acao == "sair":
            break


if __name__ == "__main__":
    jogar()
