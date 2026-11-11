#!/usr/bin/env python3
"""Servidor local do hub "Claude na Prática" — porta 8000.

Serve a pasta do projeto com:
- Cache-Control: no-store  -> o navegador nunca fica com página velha
- ThreadingHTTPServer + daemon threads -> uma conexão travada não derruba o servidor

Uso:  python3 server.py   (e abrir http://192.168.15.17:8000)
"""
import functools
import os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.abspath(__file__))


class Handler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        super().end_headers()

    def log_message(self, fmt, *args):
        pass


if __name__ == "__main__":
    handler = functools.partial(Handler, directory=ROOT)
    srv = ThreadingHTTPServer(("192.168.15.17", 8000), handler)
    srv.daemon_threads = True
    print("Hub rodando em http://192.168.15.17:8000  (pasta: %s)" % ROOT)
    srv.serve_forever()
