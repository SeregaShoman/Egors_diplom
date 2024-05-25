import traceback

class CustomError(Exception):
    def __init__(
        self, message: str, status_code: int
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.traceback = traceback.format_exc()

