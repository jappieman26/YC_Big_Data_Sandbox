import pandas as pd
from http.server import HTTPServer, BaseHTTPRequestHandler

class abc(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("content-type","text/html")
        self.end_headers()
        with open(r'C:\Users\suzan\Documents\traineeship\data\Uitslag_alle_gemeenten_TK20210317.csv', 'r',
                  encoding='utf-8') as f:
            b = f.readline().split(';')
            a = ('\n<br>'.join(b))
            self.wfile.write(a.encode())

def main():
    PORT = 8000
    server = HTTPServer(('',PORT), abc)
    print('Server running 8000')
    server.serve_forever()

if __name__ =='__main__':
    main()





