import os
import socket
from struct import unpack

from _thread import start_new_thread

from response import FileResponse, Response, ACCEPT, DENY, UPLOAD, DOWNLOAD

HOST = '127.0.0.1'
PORT = 9999
STORAGE_DIR = os.path.join(os.path.dirname(__file__), 'storage')


class FileServer:

    def __init__(self) -> None:
        os.makedirs(STORAGE_DIR, exist_ok=True)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            print(STORAGE_DIR)
            print(f"Listening on port {PORT}...")

            while True:
                conn, addr = s.accept()
                print(f'Incoming Connection from {addr}')
                start_new_thread(file_thread, (conn, self))

    def upload_file(self, filename: str, data: bytes) -> bytes:
        fpath = os.path.join(STORAGE_DIR, filename)
        if not os.path.exists(fpath):
            with open(fpath, 'wb') as f:
                f.write(data)
            res = Response(ACCEPT)
        else:
            res = Response(DENY)
        return res.pack()

    def download_file(self, filename: str) -> bytes:
        fpath = os.path.join(STORAGE_DIR, filename)
        if os.path.exists(fpath):
            with open(fpath, 'rb') as f:
                res = FileResponse(f.read())
        else:
            res = Response(DENY)
        return res.pack()


def file_thread(conn: socket.socket, fs: FileServer) -> None:
    code = conn.recv(1)[0]   # Reads 1 byte
    str_len = unpack('>I', conn.recv(4))[0]
    filename = conn.recv(str_len).decode('utf8')
    print(code, str_len, filename)

    if code == UPLOAD:
        size = unpack('>I', conn.recv(4))[0]
        file = conn.recv(size)
        print(size, file)
        data = fs.upload_file(filename, file)
    elif code == DOWNLOAD:
        data = fs.download_file(filename)
    else:
        data = Response(DENY).pack()
    conn.sendall(data)
    conn.close()
