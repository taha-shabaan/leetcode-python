#!/usr/bin/env python3
"""Import every solution under solutions/ and run its inline self-test."""

import importlib.util
import sys
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOLUTIONS = ROOT / "solutions"


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    files = sorted(
        p for p in SOLUTIONS.rglob("*.py") if not p.name.startswith("_")
    )
    passed = failed = skipped = 0

    for path in files:
        rel = path.relative_to(ROOT)
        try:
            module = load_module(path)
        except Exception:
            failed += 1
            print(f"FAIL  {rel}  (import error)")
            traceback.print_exc()
            continue

        test = getattr(module, "_self_test", None)
        if test is None:
            skipped += 1
            print(f"SKIP  {rel}  (no _self_test)")
            continue

        try:
            test()
        except Exception:
            failed += 1
            print(f"FAIL  {rel}")
            traceback.print_exc()
        else:
            passed += 1
            print(f"PASS  {rel}")

    print(f"\n{passed} passed, {failed} failed, {skipped} skipped, {len(files)} files")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
