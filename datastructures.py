import random


class Expression:
    def __init__(self, op, e1, e2=None):
        self.op = op
        self.e1 = e1
        self.e2 = e2

    def __repr__(self):
        if self.e2:
            return f"<op{self.op} {self.e1!r} {self.e2!r}>"
        else:
            return f"<op{self.op} {self.e1!r}>"


def evaluate(something, cmessage):
    """Evaluate something for a message."""
    if isinstance(something, Expression):
        e1 = evaluate(something.e1, cmessage)
        e2 = evaluate(something.e2, cmessage)
        op = something.op
        if op == '+':
            return e1 + e2
        elif op == '-':
            return e1 - e2
        elif op == '*':
            return e1 * e2
        elif op == '!':
            return int(not e1)
        elif op == '=':
            return int(e1 == e2)
        elif op == '<':
            return int(e1 < e2)
        else:
            raise RuntimeError("Unknown operation:", op)
    elif isinstance(something, Atom):
        if something.name == '@':
            return cmessage.body
        elif something.name == '&':
            return cmessage.reply
        elif something.name == '$':
            return cmessage.topic
        else:
            return something
    elif isinstance(something, tuple):
        return tuple(evaluate(x, cmessage) for x in something)
    else:
        return something


class Message:
    def __init__(self, action, cmessage=None):
        self.topic = evaluate(action['topic'], cmessage)
        self.reply = evaluate(action['reply'], cmessage)
        self.body = evaluate(action['body'], cmessage)
    def __repr__(self):
        return f"<{self.topic} {self.body} {self.reply}>"
    @classmethod
    def make_main(cls):
        return Message({'topic': Atom('main'), 'reply': Atom(''), 'body': Atom('')})
    @classmethod
    def make_manually(cls, topic, body, reply):
        return Message({'topic': topic, 'reply': reply, 'body': body})


class Statement:
    def __init__(self, condition, action1, action2):
        self.condition = condition
        self.action1 = action1
        self.action2 = action2
    def message(self, cmessage=None):
        # evaluate
        # print("Evaluating", self)
        if self.condition == Atom("") or evaluate(self.condition, cmessage):
            return Message(self.action1, cmessage)
        elif self.action2:
            return Message(self.action2, cmessage)
    def __repr__(self):
        return f"<stmt {self.condition} ? {self.action1} : {self.action2}"


class Atom:
    def __init__(self, name):
        self.name = str(name)
    def __repr__(self):
        return '<' + self.name + '>'
    def __mod__(self, other):
        return self.name == other
    def __hash__(self):
        return hash(self.name) ^ hash("literal")
    def __eq__(self, other):
        if isinstance(other, Atom):
            return other.name == self.name
        return False
    def __bool__(self):
        return self.name != ""


class Bag(list):
    """Self-shuffling list"""
    def __init__(self):
        self.i = 0
        self.c = 0
    def append(self, element):
        # print("Adding", element)
        if element is None:
            assert False
        super().append(element)
        self.i += 1
        self.c += 1
        if self.i > self.c and len(self)>2:
            # print("Shuffled")
            random.shuffle(self)
            self.i = 0
    def pop(self):
        self.c -= 1
        self.i += 1
        if self.i > self.c and len(self)>2:
            # print("Shuffled")
            random.shuffle(self)
            self.i = 0
        return super().pop()
