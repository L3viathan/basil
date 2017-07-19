def _cat(self, topic, body, ID):
    self.send(ID, "".join(body))

def _io(self, topic, body, ID):
    if topic == "print":
        print(body)
    elif topic == "read":
        i = input(body)
        self.send(ID, i)

def _cast(self, topic, body, ID):
    if topic == "int":
        self.send(ID, int(body))
    elif topic == "float":
        self.send(ID, float(body))
    elif topic == "str":
        self.send(ID, float(body))

def _cmp(self, topic, body, ID):
    if topic == "<":
        self.send(ID, body[0]<body[1])
    elif topic == ">":
        self.send(ID, body[0]>body[1])
    elif topic == "==":
        self.send(ID, body[0]==body[1])
    elif topic == "!=":
        self.send(ID, body[0]!=body[1])
    elif topic == "<=":
        self.send(ID, body[0]<=body[1])
    elif topic == ">=":
        self.send(ID, body[0]>=body[1])

def _if(self, topic, body, ID):
    cond, one, two = body
    if cond:
        self.send(one, body)
    else:
        self.send(two, body)

def register(d):
    d['cat'].append(_cat)
    d['print'].append(_io)
    d['read'].append(_io)
    d['int'].append(_cast)
    d['<'].append(_cmp)
    d['>'].append(_cmp)
    d['=='].append(_cmp)
    d['!='].append(_cmp)
    d['>='].append(_cmp)
    d['<='].append(_cmp)
    d['?'].append(_if)
