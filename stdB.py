import sys


def _stdlib(self, topic, body, ID):
    if topic == "cat":
        self.send(ID, "".join(body))
    elif topic == "print":
        print(body)
    elif topic == "read":
        i = input(body)
        self.send(ID, i)
    elif topic == "int":
        self.send(ID, int(body))
    elif topic == "float":
        self.send(ID, float(body))
    elif topic == "str":
        self.send(ID, float(body))
    elif topic == "<":
        self.send(ID, body[0] < body[1])
    elif topic == ">":
        self.send(ID, body[0] > body[1])
    elif topic == "==":
        self.send(ID, body[0] == body[1])
    elif topic == "!=":
        self.send(ID, body[0] != body[1])
    elif topic == "<=":
        self.send(ID, body[0] <= body[1])
    elif topic == ">=":
        self.send(ID, body[0] >= body[1])
    elif topic == "?":
        cond, one, two = body
        if cond:
            self.send(one, body)
        else:
            self.send(two, body)
    elif topic == "err":
        print("ERROR:", body, file=sys.stderr)
        sys.exit(1)
    elif topic == "+":
        self.send(ID, body[0] + body[1])
    elif topic == "-":
        self.send(ID, body[0] - body[1])
    elif topic == "*":
        self.send(ID, body[0] * body[1])


def register(d):
    for topic in [
            "cat",
            "print",
            "read",
            "int",
            "<",
            ">",
            "==",
            "!=",
            "<=",
            ">=",
            "?",
            "+",
            "-",
            "*",
            "err",
            ]:
        d[topic].append(_stdlib)
