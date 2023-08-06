"""Entry point. Run the server and open a browser pointing to it."""
import time
import webbrowser
from threading import Thread

import requests

from .server import build_app, get_server_hostport, start_app


def main():
    app = build_app()
    host, port = get_server_hostport()
    addr = f"http://{host}:{port}"

    def check_server_started_loop():
        while True:
            try:
                req = requests.get(addr, headers={"User-Agent": "page-opener-thread"})
                if req.status_code == 200:
                    break
            except:
                pass
            time.sleep(0.1)
        print(f"Started server listening on {addr} ...")
        webbrowser.open(addr)

    thread = Thread(target=check_server_started_loop)
    thread.start()
    start_app(app)


if __name__ == "__main__":
    main()
