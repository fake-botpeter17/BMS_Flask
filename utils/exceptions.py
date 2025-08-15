class DatabaseInitializationError(ConnectionError):
    def __init__(self, msg) -> None:
        super.__init__(msg)


