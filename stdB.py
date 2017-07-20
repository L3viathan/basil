import sys
from collections import defaultdict


o_accumulate = defaultdict(dict)
u_accumulate = defaultdict(list)


def _stdlib(self, topic, body, ID):
    if topic % "cat":
        self.send(ID, "".join(body))
    elif topic % "print":
        print(body if body is not None else "")
    elif topic % "read":
        i = input(body if body is not None else "")
        self.send(ID, i)
    elif topic % "int":
        self.send(ID, int(body))
    elif topic % "float":
        self.send(ID, float(body))
    elif topic % "str":
        self.send(ID, float(body))
    elif topic % "<":
        self.send(ID, body[0] < body[1])
    elif topic % ">":
        self.send(ID, body[0] > body[1])
    elif topic % "==":
        self.send(ID, body[0] == body[1])
    elif topic % "!=":
        self.send(ID, body[0] != body[1])
    elif topic % "<=":
        self.send(ID, body[0] <= body[1])
    elif topic % ">=":
        self.send(ID, body[0] >= body[1])
    elif topic % "?":
        cond, one, two = body
        if cond:
            self.send(one, body)
        else:
            self.send(two, body)
    elif topic % "err":
        print("ERROR:", body, file=sys.stderr)
        sys.exit(1)
    elif topic % "+":
        self.send(ID, body[0] + body[1])
    elif topic % "-":
        self.send(ID, body[0] - body[1])
    elif topic % "*":
        self.send(ID, body[0] * body[1])
    elif topic % 'accu':
        """Summary, if order is not guaranteed, solutions:

        1. Send an index. accu caches even unknowns.
        2. Random order tuples. accu caches even unknowns.
        3. Do pairs. Effectively identical to 1, just implicitly

        1 and 2 need setup messages (that specify length), 3 sort of does, but
        that is obvious.

        Another solution to that problem would be that _every_ message contains
        the length, too. That is equivalent to only sending setup messages.
        This is applicable to both 1 and 2.

        The decision for now is:
        Both 1 and 2 are implemented. 3 is not implemented (but is
        user-definable in a straightforward way). There is no setup message,
        instead, every message contains the length. There is no different topic
        for 1 and 2, instead it is determined by tuple length:

        (element, length) vs. (element, length, index)
        """
        if len(body) == 2:  # unordered
            element, length = body
            u_accumulate[ID].append(element)
            if len(u_accumulate[ID]) >= length:
                self.send(ID, tuple(u_accumulate[ID]))
                u_accumulate[ID].clear()
        elif len(body) == 3:  # ordered
            element, length, index = body
            o_accumulate[ID][index] = element
            if len(o_accumulate[ID]) >= length:
                self.send(
                        ID,
                        (tuple(o_accumulate[ID][key] for key in
                            sorted(o_accumulate[ID]))),
                        )
                o_accumulate[ID].clear()


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
            "accu",
            ]:
        d[topic].append(_stdlib)
