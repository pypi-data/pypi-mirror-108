class HttpError(Exception):
    code: int = None
    data: dict = None

    def __init__(self, code: int = None, data: dict = None):
        self.code = code or 520
        self.data = data or dict()

    def __str__(self):
        return f"[Error {self.code}]: {self.message}"

    @property
    def message(self) -> str:
        return self.data.get('message', 'Unknown error')
