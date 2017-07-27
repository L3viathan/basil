import sys
import random
from collections import defaultdict
from parseit import parse_file
from datastructures import Bag, Atom, Message
from stdB import register


class Basil:
    def __init__(self, filename):
        self.Q = Bag()
        self.listeners = defaultdict(list)
        register(self.listeners)
        for block in parse_file(filename):
            for trigger in block['triggers']:
                self.listeners[trigger].append(block['statements'])

    def do(self, listener, cmessage):
        """Process a non-native actor"""
        for statement in listener:
            msg = statement.message(cmessage)
            if msg is not None:
                self.Q.append(msg)

    def send(self, topic, body, reply=Atom("")):
        msg = Message(topic, body, reply)
        self.Q.append(msg)

    def run(self):
        self.Q.append(Message.make_main())
        while self.Q:
            msg = self.Q.pop()
            for listener in self.listeners[msg.topic]:
                if callable(listener):
                    listener(self, msg)
                else:
                    self.do(listener, msg)


bzl = Basil(sys.argv[1])
bzl.run()
