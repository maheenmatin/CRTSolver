class AbortFileException(Exception):
    def __init__(self, num):
        super().__init__(
            f"Aborting file due to OverflowError: value {num} too large to convert to int")

class TimeoutException(Exception):
    pass
