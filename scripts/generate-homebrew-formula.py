#!/usr/bin/env python3
"""
PyPI에 mulgogi를 올린 후 실행하여 Homebrew formula의 resource 블록을 생성합니다.

  pip install homebrew-pypi-poet
  python scripts/generate-homebrew-formula.py

출력된 내용을 homebrew-mulgogi/Formula/mulgogi.rb의 resource 영역에 붙여넣으세요.
"""

import subprocess
import sys


def main():
    try:
        output = subprocess.check_output(["poet", "mulgogi"], text=True)
    except FileNotFoundError:
        print("homebrew-pypi-poet가 설치되지 않았습니다.", file=sys.stderr)
        print("  pip install homebrew-pypi-poet", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"실패: {e}", file=sys.stderr)
        sys.exit(1)

    print(output)


if __name__ == "__main__":
    main()
