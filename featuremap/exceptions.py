class MapException(Exception):
    def __init__(self, message, file=None, line=None):
        self.message = message
        self.file = file
        self.line = line
        super(MapException, self).__init__()

    def __str__(self):
        ref = ""
        if self.file is not None:
            ref = self.file
            if self.line is not None:
                ref += "#L" + str(self.line)
        return "{msg} {ref}".format(msg=self.message, ref=ref)