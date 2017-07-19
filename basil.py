import sys
from collections import deque, defaultdict
from parser import parse_file
from stdB import register as stdB

class Basil:
    def __init__(self):
        self.Q = set()
        self.listeners = defaultdict(list)
        stdB(self.listeners)

    def evaluate(self, ast_val, body):
        if type(ast_val) == str:
            return body
        type_ = [*ast_val.keys()][0]
        if type_ == 'int':
            return int(ast_val['int'])
        elif type_ == 'float':
            return float(ast_val['float'])
        elif type_ == 'string':
            return ast_val['string']
        elif type_ == 'tuple':
            return tuple([self.evaluate(element, body) for element in ast_val['tuple']])
        raise RuntimeError()

    def do(self, listener, topic, body, ID):
        """Process a non-native actor"""
        for out in listener:
            topic = out['topic']
            eval_body = self.evaluate(out['body'], body)
            reply = out['reply']
            self.send(topic, eval_body, reply)

    def send(self, topic, body, reply=None):
        self.Q.add((topic, body, reply))

    def run(self):
        self.Q.add(('main', None, None))
        while self.Q:
            topic, body, ID = self.Q.pop()
            for listener in self.listeners[topic]:
                if callable(listener):
                    listener(self, topic, body, ID)
                else:
                    self.do(listener, topic, body, ID)


bzl = Basil()
for topiclist, actor in parse_file(sys.argv[1]):
    for topic in topiclist:
        bzl.listeners[topic].append(actor)
bzl.run()
