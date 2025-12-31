#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


class Colors:
    OK = "\033[92m"
    FAIL = "\033[91m"
    WARN = "\033[93m"
    INFO = "\033[94m"
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"


def print_header() -> None:
    print(f"\n{Colors.INFO}{Colors.BOLD}")
    print("=" * 60)
    print("         DETECTOR DE DOPPELGANGER - TEST SUITE")
    print("=" * 60)
    print(f"{Colors.RESET}\n")


def run_test_module(path: str, name: str) -> bool:
    print(f"{Colors.INFO}[TEST]{Colors.RESET} {name}...", end=" ", flush=True)

    result = subprocess.run(
        [sys.executable, "-m", "pytest", path, "-v", "--tb=short", "-q"],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent,
    )

    if result.returncode == 0:
        print(f"{Colors.OK}[PASS]{Colors.RESET}")
        return True

    print(f"{Colors.FAIL}[FAIL]{Colors.RESET}")
    if result.stdout:
        lines = result.stdout.strip().split("\n")
        for line in lines[-20:]:
            print(f"  {Colors.DIM}{line}{Colors.RESET}")
    if result.stderr:
        print(f"  {Colors.FAIL}{result.stderr[-500:]}{Colors.RESET}")

    return False


def main() -> int:
    print_header()

    test_modules = [
        ("src/tests/test_detector.py", "Detector de IA"),
        ("src/tests/test_humanizador.py", "Humanizador"),
        ("src/tests/test_core.py", "Core (checkpoint, output, config_loader)"),
        ("src/tests/test_utils.py", "Utils (colors)"),
        ("src/tests/test_config.py", "Config"),
    ]

    results = []
    for path, name in test_modules:
        results.append(run_test_module(path, name))

    passed = sum(results)
    total = len(results)

    print(f"\n{Colors.BOLD}{'=' * 60}{Colors.RESET}")
    print(f"{Colors.BOLD}RESULTADO FINAL{Colors.RESET}")
    print(f"{'=' * 60}")

    if passed == total:
        print(f"{Colors.OK}[SUCCESS]{Colors.RESET} {passed}/{total} testes passaram")
    else:
        failed = total - passed
        print(f"{Colors.FAIL}[FAILED]{Colors.RESET} {failed}/{total} testes falharam")

    print(f"{'=' * 60}\n")

    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())


# "Testar e duvidar; duvidar e pensar." - Descartes
