#!/usr/bin/env python3
"""
Hook de verificacao de acentuacao PT-BR
Detecta palavras comuns sem acento em arquivos de falas/dialogos
"""

import re
import sys
from pathlib import Path

PALAVRAS_COMUNS = {
    "voce": "você",
    "tambem": "também",
    "ja": "já",
    "so": "só",
    "ate": "até",
    "esta": "está",
    "nao": "não",
    "entao": "então",
    "ai": "aí",
    "la": "lá",
    "aqui": "aqui",
    "mae": "mãe",
    "pai": "pai",
    "irmao": "irmão",
    "irma": "irmã",
    "coracao": "coração",
    "razao": "razão",
    "relacao": "relação",
    "situacao": "situação",
    "informacao": "informação",
    "atencao": "atenção",
    "opcao": "opção",
    "funcao": "função",
    "secao": "seção",
    "sessao": "sessão",
    "conexao": "conexão",
    "acao": "ação",
    "reacao": "reação",
    "excecao": "exceção",
    "obrigacao": "obrigação",
    "traducao": "tradução",
    "producao": "produção",
    "reducao": "redução",
    "construcao": "construção",
    "destruicao": "destruição",
    "instrucao": "instrução",
    "solucao": "solução",
    "revolucao": "revolução",
    "evolucao": "evolução",
    "posicao": "posição",
    "condicao": "condição",
    "tradicao": "tradição",
    "educacao": "educação",
    "comunicacao": "comunicação",
    "organizacao": "organização",
    "administracao": "administração",
    "configuracao": "configuração",
    "implementacao": "implementação",
    "documentacao": "documentação",
    "especificacao": "especificação",
    "verificacao": "verificação",
    "validacao": "validação",
    "otimizacao": "otimização",
    "integracao": "integração",
    "e": "é",
    "voces": "vocês",
    "nos": "nós",
    "eles": "eles",
    "dificil": "difícil",
    "facil": "fácil",
    "impossivel": "impossível",
    "possivel": "possível",
    "incrivel": "incrível",
    "terrivel": "terrível",
    "horrivel": "horrível",
    "amavel": "amável",
    "agradavel": "agradável",
    "desagradavel": "desagradável",
    "responsavel": "responsável",
    "disponivel": "disponível",
    "indisponivel": "indisponível",
    "compativel": "compatível",
    "incompativel": "incompatível",
    "util": "útil",
    "inutel": "inútil",
    "numero": "número",
    "unico": "único",
    "ultimo": "último",
    "proximo": "próximo",
    "minimo": "mínimo",
    "maximo": "máximo",
    "otimo": "ótimo",
    "pessimo": "péssimo",
    "necessario": "necessário",
    "desnecessario": "desnecessário",
    "obrigatorio": "obrigatório",
    "voluntario": "voluntário",
    "temporario": "temporário",
    "permanente": "permanente",
    "frequente": "frequente",
    "urgente": "urgente",
    "evidente": "evidente",
    "diferente": "diferente",
    "excelente": "excelente",
    "presente": "presente",
    "ausente": "ausente",
    "consciente": "consciente",
    "inconsciente": "inconsciente",
    "eficiente": "eficiente",
    "ineficiente": "ineficiente",
    "suficiente": "suficiente",
    "insuficiente": "insuficiente",
    "obvia": "óbvia",
    "obvio": "óbvio",
    "serio": "sério",
    "seria": "séria",
    "varios": "vários",
    "varias": "várias",
    "necessaria": "necessária",
    "necessarias": "necessárias",
    "necessarios": "necessários",
    "historia": "história",
    "memoria": "memória",
    "vitoria": "vitória",
    "gloria": "glória",
    "categoria": "categoria",
    "estrategia": "estratégia",
    "tecnologia": "tecnologia",
    "metodologia": "metodologia",
    "psicologia": "psicologia",
    "ideologia": "ideologia",
    "energia": "energia",
    "sinergia": "sinergia",
    "alergia": "alergia",
    "magica": "mágica",
    "logica": "lógica",
    "musica": "música",
    "fisica": "física",
    "quimica": "química",
    "matematica": "matemática",
    "gramatica": "gramática",
    "pratica": "prática",
    "teorica": "teórica",
    "tecnica": "técnica",
    "politica": "política",
    "economica": "econômica",
    "academica": "acadêmica",
    "automatica": "automática",
    "sistematica": "sistemática",
    "problematica": "problemática",
    "tematica": "temática",
    "dramatica": "dramática",
    "romantica": "romântica",
    "fantastica": "fantástica",
    "elastica": "elástica",
    "plastica": "plástica",
    "acustica": "acústica",
    "rustica": "rústica",
    "domestica": "doméstica",
    "autentica": "autêntica",
    "identica": "idêntica",
    "genetica": "genética",
    "estetica": "estética",
    "aritmetica": "aritmética",
    "geometrica": "geométrica",
    "simetrica": "simétrica",
    "eletrica": "elétrica",
    "mecanica": "mecânica",
    "organica": "orgânica",
    "botanica": "botânica",
    "oceanica": "oceânica",
    "volcanica": "vulcânica",
    "britanica": "britânica",
    "hispanica": "hispânica",
    "germanica": "germânica",
    "romanica": "românica",
    "cronica": "crônica",
    "ironica": "irônica",
    "harmonica": "harmônica",
    "sinfonica": "sinfônica",
    "eletronica": "eletrônica",
    "telefonica": "telefônica",
    "ergonomica": "ergonômica",
    "astronomica": "astronômica",
    "gastronomica": "gastronômica",
    "anatomica": "anatômica",
    "autonoma": "autônoma",
    "sinonimo": "sinônimo",
    "antonimo": "antônimo",
    "anonimo": "anônimo",
    "homonimo": "homônimo",
    "fenomeno": "fenômeno",
    "copia": "cópia",
    "propria": "própria",
    "proprio": "próprio",
    "seculo": "século",
    "obstaculo": "obstáculo",
    "espetaculo": "espetáculo",
    "milagre": "milagre",
    "portugues": "português",
    "ingles": "inglês",
    "frances": "francês",
    "holandes": "holandês",
    "japones": "japonês",
    "chines": "chinês",
    "tres": "três",
    "pes": "pés",
    "mes": "mês",
    "ves": "vez",
    "atraves": "através",
    "talvez": "talvez",
    "cafe": "café",
    "pure": "purê",
    "bebe": "bebê",
    "reve": "revê",
    "previsto": "previsto",
    "imprevisto": "imprevisto",
    "visto": "visto",
    "revisto": "revisto",
    "misto": "misto",
    "lindo": "lindo",
    "fofo": "fofo",
    "bobo": "bobo",
    "louco": "louco",
    "doce": "doce",
    "triste": "triste",
    "feliz": "feliz",
    "infeliz": "infeliz",
    "capaz": "capaz",
    "incapaz": "incapaz",
    "eficaz": "eficaz",
    "ineficaz": "ineficaz",
    "audaz": "audaz",
    "sagaz": "sagaz",
    "tenaz": "tenaz",
    "voraz": "voraz",
    "feroz": "feroz",
    "atroz": "atroz",
    "veloz": "veloz",
    "precoce": "precoce",
    "atroce": "atroce",
}

PATTERNS_FALA = [
    r'"[^"]*"',
    r"'[^']*'",
    r'f"[^"]*"',
    r"f'[^']*'",
    r'"fala_tts":\s*"[^"]*"',
    r'"log_terminal":\s*"[^"]*"',
    r'"texto":\s*"[^"]*"',
    r'"mensagem":\s*"[^"]*"',
    r'"resposta":\s*"[^"]*"',
]


def extrair_falas(content: str) -> list[tuple[int, str]]:
    falas = []
    lines = content.split("\n")
    for i, line in enumerate(lines, 1):
        for pattern in PATTERNS_FALA:
            matches = re.findall(pattern, line)
            for match in matches:
                falas.append((i, match))
    return falas


def verificar_acentuacao(texto: str) -> list[tuple[str, str]]:
    problemas = []
    palavras = re.findall(r"\b[a-zA-Z]+\b", texto.lower())
    for palavra in palavras:
        if palavra in PALAVRAS_COMUNS:
            correcao = PALAVRAS_COMUNS[palavra]
            if palavra != correcao:
                problemas.append((palavra, correcao))
    return problemas


def verificar_arquivo(path: Path) -> list[dict]:
    erros = []
    try:
        content = path.read_text(encoding="utf-8")
    except Exception:
        return erros

    falas = extrair_falas(content)
    for linha, fala in falas:
        problemas = verificar_acentuacao(fala)
        for errado, correto in problemas:
            erros.append(
                {
                    "arquivo": str(path),
                    "linha": linha,
                    "errado": errado,
                    "correto": correto,
                    "contexto": fala[:100],
                }
            )
    return erros


def main():
    arquivos = sys.argv[1:] if len(sys.argv) > 1 else []

    if not arquivos:
        src_path = Path("src")
        if src_path.exists():
            arquivos = [str(p) for p in src_path.rglob("*.py")]
            arquivos += [str(p) for p in src_path.rglob("*.json")]

    todos_erros = []
    for arquivo in arquivos:
        path = Path(arquivo)
        if path.exists() and path.suffix in [".py", ".json", ".txt", ".md"]:
            erros = verificar_arquivo(path)
            todos_erros.extend(erros)

    if todos_erros:
        print("\n[ACENTUACAO] Palavras sem acento encontradas em falas:\n")
        for erro in todos_erros:
            print(f"  {erro['arquivo']}:{erro['linha']}")
            print(f"    '{erro['errado']}' -> '{erro['correto']}'")
            print(f"    Contexto: {erro['contexto'][:60]}...")
            print()

        print(f"\nTotal: {len(todos_erros)} problema(s) de acentuacao")
        print("\nPara corrigir automaticamente, execute:")
        print("  python scripts/hooks/fix_acentuacao.py\n")
        sys.exit(1)
    else:
        print("[ACENTUACAO] OK - Nenhum problema encontrado")
        sys.exit(0)


if __name__ == "__main__":
    main()
