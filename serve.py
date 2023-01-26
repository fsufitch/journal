import argparse
import http.server
import os


class CORSRequestHandler(http.server.SimpleHTTPRequestHandler):
    # https://stackoverflow.com/a/21957017
    def end_headers (self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.description = "Run a simple HTTP server allowing all CORS, to preview blog posts"
    parser.add_argument("-p", "--port", default=8000, type=int)
    parser.add_argument("dir", default=os.curdir)
    return parser.parse_args()

def main():
    args = parse_args()
    os.chdir(args.dir)
    addr = ('0.0.0.0', args.port)
    server = http.server.HTTPServer(addr, CORSRequestHandler)
    print(f'serving... addr={repr(addr)} dir={os.curdir}')
    server.serve_forever()

if __name__ == '__main__':
    main()