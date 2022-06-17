from struct import pack

ACCEPT = 0
DENY = UPLOAD = 1
DOWNLOAD = 2

class Response:
    def __init__(self, code) -> None:
        self.code = code
    
    def pack(self) -> bytearray:
        return bytes([self.code])


class FileResponse(Response):
    def __init__(self, data) -> None:
        super().__init__(ACCEPT)
        self.data = data
    
    def pack(self) -> bytearray:
        return super().pack() + pack("I", len(self.data)) + self.data