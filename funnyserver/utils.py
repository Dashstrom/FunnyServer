import struct
import socket


def read_utf(stream: socket.socket) -> str:
    size: int = struct.unpack('>H', stream.recv(2))[0]  # type: ignore
    return stream.recv(size).decode("utf8")


def utf_to_bytes(name: str) -> bytes:
    return struct.pack('>H', len(name)) + name.encode("utf8")


def read_byte(stream: socket.socket) -> int:
    return stream.recv(1)[0]


def byte_to_bytes(value: int) -> bytes:
    return bytes([value])


def read_unsigned_long(stream: socket.socket) -> int:
    return struct.unpack('>Q', stream.recv(8))[0]  # type: ignore


def unsigned_long_to_bytes(value: int) -> bytes:
    return struct.pack('>Q', value)


def read_bytes(stream: socket.socket) -> bytes:
    size = read_unsigned_long(stream)
    data = bytearray()
    while len(data) < size:
        packet = stream.recv(size - len(data))
        data.extend(packet)
    return data


def bytes_to_bytes(data: bytes) -> bytes:
    return unsigned_long_to_bytes(len(data)) + data
