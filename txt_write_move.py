import sys


class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        self.log = open("Print_result.txt", "w", encoding="utf8")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        # this flush method is needed for python 3 compatibility.
        # this handles the flush command by doing nothing.
        # you might want to specify some extra behavior here.
        pass


# Call out class so it runs when imported
# sys.stdout = Logger()
