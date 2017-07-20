import sys
import random
from collections import defaultdict
from parser import parse_file
from stdB import register as stdB
from datastructures import Literal, Queue


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


class Basil:
    def __init__(self):
        self.Q = Queue()
        self.listeners = defaultdict(list)
        stdB(self.listeners)

    def do(self, listener, topic, body, ID):
        """Process a non-native actor"""
        for out in listener:
            topic = evaluate(out['topic'], body, ID)
            eval_body = evaluate(out['body'], body, ID)
            reply = evaluate(out['reply'], body, ID)
            self.send(topic, eval_body, reply)

    def send(self, topic, body, reply=None):
        self.Q.append((topic, body, reply))

    def run(self):
        self.Q.append((Literal('main'), None, None))
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
        bzl.listeners[Literal(topic)].append(actor)
bzl.run()
