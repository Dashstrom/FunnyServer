import os
import socket
from struct import unpack
from string import ascii_letters, digits
from _thread import start_new_thread

from .response import (
    FileResponse, Response, ACCEPT, DENY, UPLOAD, DOWNLOAD, LIST, DELETE
)

HOST = '127.0.0.1'
PORT = 9999
STORAGE_DIR = os.path.join(os.path.dirname(__file__), 'storage')
ALPHA = ascii_letters + digits + "_.-"


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
        if not os.path.exists(fpath):
            res = Response(DENY)
        else:
            with open(fpath, 'rb') as f:
                res = FileResponse(f.read())
        return res.pack()

    def list_files(self, pattern: str) -> bytes:
        stored_files = os.listdir(STORAGE_DIR)
        matching_files = []
        for file in stored_files:
            if file.startswith(pattern):
                matching_files.append(file)
        res = FileResponse("\n".join(matching_files).encode())
        return res.pack()
    
    def delete_file(self, filename: str) -> bytes:
        fpath = os.path.join(STORAGE_DIR, filename)
        if not os.path.exists(fpath):
            res = Response(DENY)
        else:
            os.remove(fpath)
            res = Response(ACCEPT)
        return res.pack()


def file_thread(conn: socket.socket, fs: FileServer) -> None:
    code = conn.recv(1)[0]   # Reads 1 byte
    str_len: int = unpack('>I', conn.recv(4))[0]  # type: ignore
    filename = conn.recv(str_len).decode('utf8')
    data = Response(DENY).pack()
    print(code, str_len, filename)
    if all(c in ALPHA for c in filename):
        if code == UPLOAD:
            size: int = unpack('>I', conn.recv(4))[0]  # type: ignore
            file = conn.recv(size)
            data = fs.upload_file(filename, file)
        elif code == DOWNLOAD:
            data = fs.download_file(filename)
        elif code == LIST:
            data = fs.list_files(filename)
        elif code == DELETE:
            data = fs.delete_file(filename)
    conn.sendall(data)
    conn.close()
