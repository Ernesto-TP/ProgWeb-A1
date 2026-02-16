from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qsl, urlparse
import os

class WebRequestHandler(BaseHTTPRequestHandler):
    pages = {
        "/": "home.html",
        "/proyecto/1": "1.html",
        "/proyecto/2": "2.html",
        "/proyecto/3": "3.html",
    }
    
    def url(self):
        return urlparse(self.path)

    def query_data(self):
        return dict(parse_qsl(self.url().query))

     def load_html_file(self, filename):
        """Load HTML file from disk"""
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(script_dir, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return f"<h1>Error: {filename} not found</h1>"

    def do_GET(self):
       path = self.url().path
        
        if path in self.pages:
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            content = self.load_html_file(self.pages[path])
            self.wfile.write(content.encode("utf-8"))
        else:
            self.send_response(404)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(self.get_404_error().encode("utf-8"))

    def get_404_error(self):
        return f"""
   <!DOCTYPE html>
<html>
<head>
    <title>404 - Página no encontrada</title>
</head>
<body>
    <h1>404 - Página no encontrada</h1>
    <p>La ruta '{self.path}' no existe.</p>
    <p><a href="/">Volver a la página de inicio</a></p>
</body>
</html>
"""


if __name__ == "__main__":
    print("Starting server")
    server = HTTPServer(("localhost", 8080), WebRequestHandler)
    server.serve_forever()
