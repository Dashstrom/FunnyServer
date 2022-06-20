
from typing import List
from . import utils

ACCEPT = 0
DENY = UPLOAD = 1
DOWNLOAD = 2
LIST = 3
DELETE = 4


class Response:

    def __init__(self, code: int) -> None:
        self.code = code

    def pack(self) -> bytes:
        print("OUT", self.code)
        return bytes([self.code])


class FileResponse(Response):

    def __init__(self, data: bytes) -> None:
        super().__init__(ACCEPT)
        self.data = data

    def pack(self) -> bytes:
        return super().pack() + utils.bytes_to_bytes(self.data)


class ArrayResponse(Response):

    def __init__(self, array: List[str]) -> None:
        super().__init__(ACCEPT)
        self.array = array

    def pack(self) -> bytes:
        return super().pack() + b"".join(map(utils.utf_to_bytes, self.array))
