import sys


class Logger(object):
    def __init__(self, log_file="Print_result.txt", mode="w", encoding="utf8"):
        self.terminal = sys.stdout
        try:
            self.log = open(log_file, mode, encoding=encoding)
        except IOError as e:
            self.terminal.write(f"Failed to open log file: {e}\n")
            self.log = None

    def write(self, message):
        try:
            self.terminal.write(message)
            if self.log:
                self.log.write(message)
                self.log.flush()  # Ensure each write is flushed
        except Exception as e:
            self.terminal.write(f"Failed to write to log file: {e}\n")

    def flush(self):
        try:
            self.terminal.flush()
            if self.log:
                self.log.flush()
        except Exception as e:
            self.terminal.write(f"Failed to flush log file: {e}\n")

    def close(self):
        if self.log:
            try:
                self.log.close()
            except Exception as e:
                self.terminal.write(f"Failed to close log file: {e}\n")


# Uncomment to activate the Logger
# sys.stdout = Logger()
