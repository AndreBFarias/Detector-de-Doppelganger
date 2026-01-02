#!/bin/bash
# Rotina automatizada de agentes para Detector de Doppelganger
# Uso: ./scripts/run_agents.sh [qa|audit|compliance|scorecard|build|all]

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
DOCS_DIR="${PROJECT_ROOT}/docs"
DATE=$(date +%Y-%m-%d)

cd "$PROJECT_ROOT"

mkdir -p "$DOCS_DIR"

echo "================================================"
echo " Detector de Doppelganger - Sistema de Agentes"
echo "================================================"
echo ""

run_compliance() {
    echo "[COMPLIANCE] Verificando regras do PROJECT_RULES.md..."
    echo ""

    echo "=== REGRA -1: Anonimato ==="
    violations=$(grep -rniE "claude|anthropic|openai|gpt-[0-9]" src/ --include="*.py" 2>/dev/null | grep -viE "api_key|provider|model|config|client|engine" || true)
    if [ -n "$violations" ]; then
        echo "VIOLACAO DETECTADA:"
        echo "$violations"
        echo ""
    else
        echo "[OK] Anonimato mantido"
    fi

    echo ""
    echo "=== REGRA 0: Estrutura ==="
    for f in main.py config.py requirements.txt .gitignore LICENSE README.md; do
        [ -f "$f" ] && echo "[OK] $f" || echo "[FALTA] $f"
    done

    echo ""
    echo "=== REGRA 1: Codigo ==="
    prints=$(grep -rn "print(" src/ --include="*.py" 2>/dev/null | grep -v "# debug\|test_" | wc -l)
    echo "Prints encontrados: $prints"

    excepts=$(grep -rn "except.*:.*pass" src/ --include="*.py" 2>/dev/null | wc -l)
    echo "except:pass encontrados: $excepts"

    echo ""
}

run_qa() {
    echo "[QA] Executando analise de qualidade..."
    echo ""

    echo "=== TESTES ==="
    pytest src/tests/ -v --tb=short 2>&1 || true

    echo ""
    echo "=== LINTER ==="
    ruff check src/ --statistics 2>&1 || true

    echo ""
}

run_audit() {
    echo "[AUDIT] Executando auditoria de codigo..."
    echo ""

    echo "=== SEGURANCA ==="
    echo "Secrets expostos:"
    grep -rniE "api_key|password|secret|token" src/ --include="*.py" 2>/dev/null | grep -v ".env" | head -10 || echo "Nenhum encontrado"

    echo ""
    echo "Hardcoded paths:"
    grep -rn "/home/\|/Users/" src/ --include="*.py" 2>/dev/null | head -5 || echo "Nenhum encontrado"

    echo ""
    echo "=== ARQUIVOS GRANDES ==="
    find src/ -name "*.py" -exec wc -l {} \; 2>/dev/null | sort -rn | head -10

    echo ""
    echo "=== EXCECOES SILENCIOSAS ==="
    grep -rn "except.*pass" src/ --include="*.py" 2>/dev/null || echo "Nenhuma encontrada"

    echo ""
}

run_scorecard() {
    echo "[SCORECARD] Gerando scorecard..."
    echo ""

    lines=$(find src/ -name "*.py" -exec cat {} \; 2>/dev/null | wc -l)
    files=$(find src/ -name "*.py" 2>/dev/null | wc -l)
    tests=$(pytest src/tests/ --collect-only -q 2>/dev/null | tail -1 || echo "0 tests")
    ruff_issues=$(ruff check src/ 2>/dev/null | wc -l || echo "0")

    echo "Linhas de codigo: $lines"
    echo "Arquivos Python: $files"
    echo "Testes: $tests"
    echo "Issues Ruff: $ruff_issues"

    echo ""
    echo "SCORECARD - Detector de Doppelganger"
    echo "======================================"
    echo ""

    # Calcular notas simples
    if [ "$ruff_issues" -eq 0 ]; then
        echo "QUALIDADE     ██████████  10/10"
    elif [ "$ruff_issues" -lt 10 ]; then
        echo "QUALIDADE     ████████░░  8/10"
    else
        echo "QUALIDADE     ██████░░░░  6/10"
    fi

    echo ""
}

run_build() {
    echo "[BUILD] Executando builds..."
    echo ""

    echo "=== BUILD .deb ==="
    chmod +x packaging/build_deb.sh
    ./packaging/build_deb.sh 2>&1

    echo ""
    echo "=== VERIFICANDO ==="
    ls -lh dist/*.deb 2>/dev/null || echo "Nenhum .deb encontrado"

    echo ""

    if command -v flatpak-builder &> /dev/null; then
        echo "=== BUILD Flatpak ==="
        chmod +x packaging/build_flatpak.sh
        ./packaging/build_flatpak.sh 2>&1
    else
        echo "[SKIP] flatpak-builder nao instalado"
    fi

    echo ""
}

run_all() {
    run_compliance
    echo "================================================"
    run_qa
    echo "================================================"
    run_audit
    echo "================================================"
    run_scorecard
    echo "================================================"
    run_build
}

case "${1:-all}" in
    compliance)
        run_compliance
        ;;
    qa)
        run_qa
        ;;
    audit)
        run_audit
        ;;
    scorecard)
        run_scorecard
        ;;
    build)
        run_build
        ;;
    all)
        run_all
        ;;
    *)
        echo "Uso: $0 [qa|audit|compliance|scorecard|build|all]"
        exit 1
        ;;
esac

echo ""
echo "================================================"
echo " Concluido: $(date)"
echo "================================================"
