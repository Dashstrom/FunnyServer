import socket
from struct import unpack

from _thread import start_new_thread
import threading

HOST = '127.0.0.1'
PORT = 9999

lock_state = threading.Lock()

class FileServer:
    def __init__(self) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            print(f"Listening on port {PORT}...")
            conn, addr = s.accept()
            with conn:
                print(f'Incoming Connection from {addr}')
                while True:
                    # lock acquired by incoming connection
                    lock_state.acquire()
                    start_new_thread(file_thread, (conn, self))
                

    def init_writer_buffer(self) -> None:
        return
    
    def init_reader_buffer(self) -> None:
        return
    
    def upload_file(self, write_buffer, filename) -> None:
        return

    def download_file(self, reading_buffer, filename) -> None:
        return 


def file_thread(conn: socket.socket, fs: FileServer) -> None:
    while True:
        code = unpack('I', conn.recv(1))   # Reads 1 byte
        str_len = unpack('', conn.recv(1))
        filename = unpack('', conn.recv(str_len))
        size = unpack('', conn.recv(4))
        file = unpack('', conn.recv(size))

        if not data:
            # lock released at the end of the work
            lock_state.release()
            break
        conn.sendall(data)  # echo



if __name__ == '__main__':
    fs = FileServer()    