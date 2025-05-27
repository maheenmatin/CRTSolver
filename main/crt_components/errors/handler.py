import crt_components.errors.error as error

def timeout_handler(signum, frame):
    raise error.TimeoutException("Timed out while solving file")
