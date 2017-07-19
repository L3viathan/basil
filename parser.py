from tatsu import compile as tco

with open("grammar") as f:
    g = f.read()

model = tco(g)

def parse_file(filename):
    with open(filename) as f:
        code = f.read()
    for section in code.split("\n\n"):
        ast = model.parse(section)
        yield (ast['in'], ast['out'])
