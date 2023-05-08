import sys


# 将控制台的输出，保存到log文件中
class Logger(object):
    def __init__(self, filename='result.log', stream=sys.stdout):
        self.terminal = stream
        self.log = open(filename, 'a')

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass

