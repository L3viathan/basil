import re
from datastructures import Atom, Statement, Message, Expression

r_token = '"[^"]+"|\\w+|\\d+|\\S'
r_topic = '(\\w+|\$|@|&)$'
ops2 = "+*-="
ops1 = "!"

s = """
main {
>foo bar;
= 2 2 > bar ($,&,@) wat;
= 1 1 > bar (2, 4) no > bat;
}"""

def parse_tuple(tokens, index):
    expressions = []
    while tokens[index] != ')':
        # either beginning parenthesis or comma
        assert tokens[index] in "(,"
        expression, index = parse_expression(tokens, index+1)
        expressions.append(expression)
    return tuple(expressions), index+1

def parse_string(tokens, index):
    # for now:
    return tokens[index][1:-1], index+1

def parse_int(tokens, index):
    return int(tokens[index]), index+1

def parse_value(tokens, index):
    # tuple, string, int, float, atom
    # tuple can contain _expressions_, not values
    if tokens[index] == '(':  # tuple
        value, index = parse_tuple(tokens, index)
    elif tokens[index].startswith('"'):
        value, index = parse_string(tokens, index)
    elif tokens[index].isnumeric():
        value, index = parse_int(tokens, index)
    else:  # atom
        value, index = parse_topic(tokens, index)
    return value, index

def parse_expression(tokens, index):
    # print("Parsing expression...", tokens[index:index+5])
    if tokens[index] in ops2:
        op = tokens[index]
        e1, index = parse_expression(tokens, index+1)
        e2, index = parse_expression(tokens, index)
        expression = Expression(op, e1, e2)
    elif tokens[index] in ops1:
        op = tokens[index]
        e, index = parse_expression(tokens, index+1)
        expression = Expression(op, e)
    else:
        expression, index = parse_value(tokens, index)
    return expression, index

def parse_topic(tokens, index):
    # print("Parsing topic:", tokens[index:index+5], index)
    assert re.match(r_topic, tokens[index])
    return Atom(tokens[index]), index+1

def parse_head(tokens, index):
    triggers = []
    while tokens[index] != '{':
        triggers.append(Atom(tokens[index]))
        index += 1
    return triggers, index+1

def parse_action(tokens, index):
    # print("Parsing action:", tokens[index:index+5])
    topic, index = parse_topic(tokens, index)
    if tokens[index] not in (';', '>'):
        body, index = parse_expression(tokens, index)
    else:
        body = Atom("")
    if tokens[index] not in (';', '>'):
        # reply-value
        reply, index = parse_topic(tokens, index)
    else:
        reply = Atom("")
    return {'topic': topic, 'body': body, 'reply': reply}, index

def parse_statement(tokens, index):
    if tokens[index] != '>':
        condition, index = parse_expression(tokens, index)
    else:
        condition = Atom("")
    # print("Condition:", condition, ", @", tokens[index:index+3])
    index += 1
    action1, index = parse_action(tokens, index)
    if tokens[index] == '>':
        action2, index = parse_action(tokens, index+1)
    else:
        action2 = Atom("")
    assert tokens[index] == ';'
    # print("Parsed statement:", (condition, action1, action2))
    return Statement(condition, action1, action2), index+1

def parse_block(tokens, index):
    triggers, index = parse_head(tokens, index)
    statements = []
    while tokens[index] != '}':
        statement, index = parse_statement(tokens, index)
        statements.append(statement)
    return {'triggers': triggers, 'statements': statements}, index+1

def parse(text):
    tokens = re.findall(r_token, text)
    blocks = []
    index = 0
    while index < len(tokens):
        block, index = parse_block(tokens, index)
        blocks.append(block)
    return blocks


def parse_file(filename):
    with open(filename) as f:
        return parse(f.read())


if __name__ == '__main__':
    tree = parse(s)
    print(tree)
    m = Message({'body':"foo", 'topic':Atom("hi"), 'reply':Atom("reply")})
    print(tree[0]['statements'][1].message(m))
