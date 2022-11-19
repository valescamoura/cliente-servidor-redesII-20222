class Request:
    def __init__(self, op, body):
        self.op: str = op
        self.body = body
