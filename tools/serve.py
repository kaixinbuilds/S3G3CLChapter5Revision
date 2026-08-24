"""
本机预览用的小伺服器 ｜ A tiny local preview server.
只是为了在浏览器里看落地页 —— 相对路径的 CSS/JS 要靠真的 HTTP 才载得到。
Just for previewing the site locally: the relative CSS/JS paths need real HTTP.

用法 ｜ Usage:  python3 tools/serve.py [port]
"""
import functools, http.server, os, socketserver, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8731

handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=ROOT)
socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("127.0.0.1", PORT), handler) as httpd:
    print(f"serving {ROOT} at http://127.0.0.1:{PORT}/")
    httpd.serve_forever()
