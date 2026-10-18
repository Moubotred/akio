from http.server import BaseHTTPRequestHandler, HTTPServer
import ssl

CERTFILE = "./Local/server.pem"
KEYFILE = "./Local/server.pem"

class MiServidor(BaseHTTPRequestHandler):
    def do_POST(self):
        # Mostrar la ruta solicitada
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length) if length else b""
        print(f"Ruta solicitada: {self.path}")
        print(f"Header: {self.headers}")
        print(f"Body: {body[:100]}")

        self.send_response(200)
        self.send_header("Content-type", "text/plain")

        self.end_headers()
        self.wfile.write(f"Has solicitado la ruta: {self.path}".encode())

    def do_GET(self):
       length = int(self.headers.get("Content-Length",0))
       body = self.rfile.read(length) if length else b""
       print("Ruta: ", self.path)
       #print("Header: ", {self.headers.keys()})
       for nombre_encabezado, valor in self.headers.items():
            print(f"{nombre_encabezado}: {valor}")

       print("Body: ",body)

       self.send_response(200)
       self.end_headers()

       #self.end_headers()
       self.wfile.write(f"has solicitado la ruta: {self.path}".encode())

      
if __name__ == "__main__":

   import sys
   import socket
   
   host = socket.gethostname()
   ip = sys.argv[2] if sys.argv[2] else socket.gethostbyname(host)
   port = sys.argv[1]

   servidor = HTTPServer((f'{ip}', int(port)), MiServidor)
   context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
   context.load_cert_chain(certfile=CERTFILE,keyfile=KEYFILE)
   servidor.socket = context.wrap_socket(servidor.socket,server_side=True)

   print("Servidor corriendo en http://{}:{}".format(ip,port))
   servidor.serve_forever()
