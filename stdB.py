import sys
from collections import defaultdict
from datastructures import Atom, Message


o_accumulate = defaultdict(dict)
u_accumulate = defaultdict(list)
holds = dict()
releases = set()


def _stdlib(self, msg):
    if msg.topic % "cat":
        self.send(msg.reply, "".join(msg.body))
    elif msg.topic % "print":
        print(msg.body)
        self.send(msg.reply, Atom(""))
    elif msg.topic % "read":
        i = input(msg.body)
        self.send(msg.reply, i)
    elif msg.topic % "int":
        self.send(msg.reply, int(msg.body))
    elif msg.topic % "float":
        self.send(msg.reply, float(msg.body))
    elif msg.topic % "str":
        self.send(msg.reply, float(msg.body))
    elif msg.topic % "err":
        print("ERROR:", msg.body, file=sys.stderr)
        sys.exit(1)
    elif msg.topic % "hold":
        holds[msg.reply] = msg.body
        if msg.reply in releases:
            releases.remove(msg.reply)
            self.send(*holds[msg.reply])
    elif msg.topic % "release":
        if msg.body in holds:
            self.send(*holds[msg.reply])
            del holds[msg.reply]
        else:
            releases.add(msg.body)
    elif msg.topic % 'order':
        ...
    elif msg.topic % 'accu':
        if len(msg.body) == 2:  # unordered
            element, length = msg.body
            u_accumulate[msg.reply].append(element)
            if len(u_accumulate[msg.reply]) >= length:
                self.send(msg.reply, tuple(u_accumulate[ID]))
                u_accumulate[msg.reply].clear()
        elif len(msg.body) == 3:  # ordered
            element, length, index = msg.body
            o_accumulate[msg.reply][index] = element
            if len(o_accumulate[msg.reply]) >= length:
                self.send(
                        msg.reply,
                        (tuple(o_accumulate[msg.reply][key] for key in
                            sorted(o_accumulate[msg.reply]))),
                        )
                o_accumulate[msg.reply].clear()


def register(d):
    for topic in [
            "cat",
            "print",
            "read",
            "int",
            "err",
            "accu",
            "hold",
            "release",
            ]:
        d[Atom(topic)].append(_stdlib)
