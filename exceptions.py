class Exit(Exception):
    """
    Exception to allow a clean exit from any point in execution
    """
    KeyFailedToSave = 1
    DirectoryNotFound = 2

    def __init__(self, exitcode):
        self.exitcode = exitcode
