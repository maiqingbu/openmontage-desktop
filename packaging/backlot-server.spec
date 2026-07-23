# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec: 将 Backlot 服务打包为独立 sidecar 二进制。"""

from PyInstaller.utils.hooks import collect_all

block_cipher = None

datas = [("../backlot/ui", "backlot/ui")]
hiddenimports = []

for pkg in ("uvicorn", "fastapi", "starlette", "anyio", "pydantic", "pydantic_core"):
    d, b, h = collect_all(pkg)
    datas += d
    hiddenimports += h

a = Analysis(
    ["backlot_server.py"],
    pathex=[".."],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports + [
        "backlot.server",
        "backlot.state",
        "lib.events",
        "lib.paths",
        "uvicorn.logging",
        "uvicorn.loops.auto",
        "uvicorn.protocols.http.auto",
        "uvicorn.protocols.websockets.auto",
        "uvicorn.lifespan.on",
        "email_validator",
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=["numpy", "PIL", "torch", "transformers", "onnxruntime", "pytest"],
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="backlot-server",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=True,
)
