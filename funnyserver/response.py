from struct import pack

ACCEPT = 0
DENY = UPLOAD = 1
DOWNLOAD = 2


class Response:
    
    def __init__(self, code: int) -> None:
        self.code = code
    
    def pack(self) -> bytes:
        return bytes([self.code])


class FileResponse(Response):

    def __init__(self, data: bytes) -> None:
        super().__init__(ACCEPT)
        self.data = data
    
    def pack(self) -> bytes:
        return super().pack() + pack("I", len(self.data)) + self.data
