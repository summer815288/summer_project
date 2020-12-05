class MyException(Exception):

    def __init__(self, message="", type='', path="", error=''):
        # super().__init__()
        self.message = message
        self.type = type
        self.path = path
        self.error = error

    def message(self):
        return self.message

    def type(self):
        return self.type

    def path(self):
        return self.path

    def error(self):
        return self.error


a = MyException('nihao', 'type', 'path', 'error')
print(a.message)
try:
    raise MyException('nihao', 'type', 'path', 'error')
except MyException as e:
    print(e.message)
    print(e.type)
    print(e.path)
    print(e.error)
