"""Backlot 桌面版 sidecar 入口。

PyInstaller 打包为独立二进制，由 Tauri 外壳拉起：
    backlot-server --port 4750
"""

from __future__ import annotations

import sys


def main() -> int:
    sys.argv = ["backlot", "serve", *sys.argv[1:]]
    from backlot.__main__ import main as backlot_main

    return backlot_main()


if __name__ == "__main__":
    raise SystemExit(main())
