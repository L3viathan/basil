import sys
from collections import deque, defaultdict
from parser import parse_file
from stdB import register as stdB


def evaluate(ast_val, body, ID):
    # constant:
    if type(ast_val) == str:
        if ast_val == '@':
            return body
        elif ast_val == '&':
            return ID
        else:  # literal
            return Literal(ast_val)
    elif ast_val is None:
        return None
    type_ = [*ast_val.keys()][0]
    if type_ == 'int':
        return int(ast_val['int'])
    elif type_ == 'float':
        return float(ast_val['float'])
    elif type_ == 'string':
        return ast_val['string']
    elif type_ == 'tuple':
        return tuple([evaluate(element, body, ID) for element in ast_val['tuple']])
    raise RuntimeError()

class Literal:
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return '<' + self.name + '>'
    def __mod__(self, other):
        return self.name == other


class Basil:
    def __init__(self):
        self.Q = set()
        self.listeners = defaultdict(list)
        stdB(self.listeners)

    def do(self, listener, topic, body, ID):
        """Process a non-native actor"""
        for out in listener:
            topic = Literal(out['topic'])
            eval_body = evaluate(out['body'], body, ID)
            reply = Literal(out['reply'])
            self.send(topic, eval_body, reply)

    def send(self, topic, body, reply=None):
        self.Q.add((topic, body, reply))

    def run(self):
        self.Q.add((Literal('main'), None, None))
        while self.Q:
            topic, body, ID = self.Q.pop()
            for listener in self.listeners[topic.name]:
                if callable(listener):
                    listener(self, topic, body, ID)
                else:
                    self.do(listener, topic, body, ID)


bzl = Basil()
for topiclist, actor in parse_file(sys.argv[1]):
    for topic in topiclist:
        bzl.listeners[topic].append(actor)
bzl.run()
