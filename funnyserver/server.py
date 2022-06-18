import os
import socket
from string import ascii_letters, digits
from _thread import start_new_thread

from .response import (
    ArrayResponse, FileResponse, Response, ACCEPT, DENY, UPLOAD, DOWNLOAD,
    LIST, DELETE
)

from . import utils

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

    def upload_file(self, filename: str, data: bytes) -> Response:
        fpath = os.path.join(STORAGE_DIR, filename)
        if not os.path.exists(fpath):
            with open(fpath, 'wb') as f:
                f.write(data)
            return Response(ACCEPT)
        else:
            return Response(DENY)

    def download_file(self, filename: str) -> Response:
        fpath = os.path.join(STORAGE_DIR, filename)
        if not os.path.exists(fpath):
            return Response(DENY)
        else:
            with open(fpath, 'rb') as f:
                return FileResponse(f.read())

    def list_files(self, pattern: str) -> Response:
        matching_files = [file for file in os.listdir(STORAGE_DIR)
                          if file.startswith(pattern)]
        return ArrayResponse(matching_files)

    def delete_file(self, filename: str) -> Response:
        path = os.path.join(STORAGE_DIR, filename)
        if not os.path.exists(path):
            return Response(DENY)
        else:
            os.remove(path)
            return Response(ACCEPT)


def file_thread(conn: socket.socket, fs: FileServer) -> None:
    code = utils.read_byte(conn)
    filename = utils.read_utf(conn)
    res = Response(DENY)
    if all(c in ALPHA for c in filename):
        if code == UPLOAD:
            file = utils.read_bytes(conn)
            res = fs.upload_file(filename, file)
        elif code == DOWNLOAD:
            res = fs.download_file(filename)
        elif code == LIST:
            res = fs.list_files(filename)
        elif code == DELETE:
            res = fs.delete_file(filename)
    elif code == UPLOAD:
        file = utils.read_bytes(conn)  # must flush
    conn.sendall(res.pack())
    conn.close()
