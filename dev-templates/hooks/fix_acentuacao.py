#!/usr/bin/env python3
"""
Script de correcao automatica de acentuacao PT-BR
Corrige palavras sem acento em arquivos de falas/dialogos
"""

import re
import sys
from pathlib import Path

from check_acentuacao import PALAVRAS_COMUNS


def corrigir_texto(texto: str) -> tuple[str, int]:
    correcoes = 0
    resultado = texto

    for errado, correto in PALAVRAS_COMUNS.items():
        if errado == correto:
            continue

        pattern = rf"\b{errado}\b"
        matches = len(re.findall(pattern, resultado, re.IGNORECASE))
        if matches > 0:

            def replace_case(match, correto=correto):
                word = match.group(0)
                if word.isupper():
                    return correto.upper()
                elif word[0].isupper():
                    return correto.capitalize()
                return correto

            resultado = re.sub(pattern, replace_case, resultado, flags=re.IGNORECASE)
            correcoes += matches

    return resultado, correcoes


def corrigir_arquivo(path: Path, dry_run: bool = True) -> int:
    try:
        content = path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"  [ERRO] Nao foi possivel ler {path}: {e}")
        return 0

    novo_content, correcoes = corrigir_texto(content)

    if correcoes > 0:
        if dry_run:
            print(f"  [DRY-RUN] {path}: {correcoes} correcao(oes)")
        else:
            path.write_text(novo_content, encoding="utf-8")
            print(f"  [OK] {path}: {correcoes} correcao(oes)")

    return correcoes


def main():
    dry_run = "--execute" not in sys.argv
    arquivos = [a for a in sys.argv[1:] if not a.startswith("--")]

    if not arquivos:
        src_path = Path("src")
        if src_path.exists():
            arquivos = [str(p) for p in src_path.rglob("*.py")]
            arquivos += [str(p) for p in src_path.rglob("*.json")]

    if dry_run:
        print("\n[MODO DRY-RUN] Simulando correcoes (use --execute para aplicar)\n")
    else:
        print("\n[EXECUTANDO] Aplicando correcoes...\n")

    total = 0
    for arquivo in arquivos:
        path = Path(arquivo)
        if path.exists() and path.suffix in [".py", ".json", ".txt", ".md"]:
            total += corrigir_arquivo(path, dry_run)

    print(f"\nTotal: {total} correcao(oes)")

    if dry_run and total > 0:
        print("\nPara aplicar as correcoes, execute:")
        print("  python scripts/hooks/fix_acentuacao.py --execute\n")


if __name__ == "__main__":
    main()
