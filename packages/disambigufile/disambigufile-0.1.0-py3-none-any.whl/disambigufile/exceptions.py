class Error(Exception):
    pass

class NoMatchError(Error):
    pass

class AmbiguousMatchError(Error):
    def __init__(self, found):
        self.found = found
        self.message = f"matches found: {found}"

