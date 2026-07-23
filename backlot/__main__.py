"""Backlot 命令行工具（CLI）。

    python -m backlot open [project-id]   # 如需要则启动服务器，并打开浏览器
    python -m backlot serve [--port N]    # 在前台运行服务器

``open`` 在设计上具有幂等性且失败不致命：智能体会在管线初始化时
调用它，即使调用失败也必须继续后续的制作流程。
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
import urllib.request
import webbrowser

from backlot import DEFAULT_PORT


def _port() -> int:
    try:
        return int(os.environ.get("BACKLOT_PORT", DEFAULT_PORT))
    except ValueError:
        return DEFAULT_PORT


def _server_alive(port: int) -> bool:
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/api/health", timeout=1.5) as resp:
            return resp.status == 200
    except Exception:
        return False


def _spawn_server(port: int) -> None:
    """Start the server as a detached background process."""
    cmd = [sys.executable, "-m", "backlot", "serve", "--port", str(port)]
    kwargs: dict = {
        "stdout": subprocess.DEVNULL,
        "stderr": subprocess.DEVNULL,
        "stdin": subprocess.DEVNULL,
    }
    if os.name == "nt":
        kwargs["creationflags"] = (
            subprocess.CREATE_NEW_PROCESS_GROUP | getattr(subprocess, "DETACHED_PROCESS", 0x00000008)
        )
    else:
        kwargs["start_new_session"] = True
    subprocess.Popen(cmd, **kwargs)


def cmd_open(project_id: str | None) -> int:
    port = _port()
    if not _server_alive(port):
        try:
            _spawn_server(port)
        except Exception as exc:
            print(f"backlot: 无法启动服务器（{exc}）——将在没有看板的情况下继续")
            return 1
        deadline = time.time() + 15
        while time.time() < deadline:
            if _server_alive(port):
                break
            time.sleep(0.4)
        else:
            print("backlot: 服务器未能及时启动——将在没有看板的情况下继续")
            return 1
    url = f"http://127.0.0.1:{port}/"
    if project_id:
        url = f"http://127.0.0.1:{port}/p/{project_id}"
    try:
        webbrowser.open(url)
    except Exception:
        pass
    print(f"backlot: {url}")
    return 0


def cmd_serve(port: int) -> int:
    import uvicorn

    uvicorn.run("backlot.server:app", host="127.0.0.1", port=port, log_level="warning")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="backlot", description=__doc__)
    sub = parser.add_subparsers(dest="command")

    p_open = sub.add_parser("open", help="在浏览器中打开看板（如需要会自动启动服务器）")
    p_open.add_argument("project_id", nargs="?", default=None)

    p_serve = sub.add_parser("serve", help="在前台运行 Backlot 服务器")
    p_serve.add_argument("--port", type=int, default=_port())

    args = parser.parse_args(argv)
    if args.command == "open":
        return cmd_open(args.project_id)
    if args.command == "serve":
        return cmd_serve(args.port)
    parser.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
