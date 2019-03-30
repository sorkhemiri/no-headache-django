class EntryPointNotAvailable(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f"EntryPoint file Not Found" if not self.message else self.message


class RequirementsNotAvailable(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f"Requirements file Not Found" if not self.message else self.message


class ManageFileNotAvailable(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f"manage.py file Not Found" if not self.message else self.message


class WsgiFileNotAvailable(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f"wsgi.py file Not Found" if not self.message else self.message


