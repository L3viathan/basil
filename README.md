# Basil

*Basil* is a message-based programming language. Its name is a reference to
both [Aceto](https://github.com/aceto/aceto) and
[OIL](https://github.com/L3viathan/OIL).

## Concept

Basil has something like a message queue, but it's called the message *bag*,
because the order elements are taken out is "random"; non-guaranteed. There is
rudimentary support for expressions and some operators, but for the most part,
all a basil program does is wait for messages and react to them by sending
other messages.

## Syntax

A basil file contains one or more *blocks*. A block consists of a *header*, and
a set of *statements* that get executed when a message is received. The header
is a space-seperated list of *topics* this block listens to.

A statement starts with an optional *condition*, followed by a `>` character,
followed by an *action*, optionally followed by another `>` character and
another action. A semicolon finalizes a statement:

    (condition) ">" (action) ">" (another action) ";"

A condition is an *expression*. An action is a triplet, seperated by spaces:
*topic*, *body*, and *reply-to*. Both topic and reply-to have to be *atoms*,
body can be an arbitrary expression. body and reply-to are optional, but when
reply-to is given, body has to be given too.

An expression is either:

- an integer
- a string (enclosed in double-quotes)
- a tuple of one or more values (in Python syntax)
- an atom; a alphanumerical string of characters.
- a complex expression consisting of an operator and one or more operands
  (prefix notation)

Apart from alphanumerical atoms, there are three special atoms: `@`, `&`, and
`$`. They refer to the current body, current reply-to and current topic,
respectively.

## Semantics

When a *message* (basically a triplet of topic, body, and reply-to) is being
sent, it is being pushed in the bag. When one is being popped, *every* block
that has the message's topic listed in its header gets executed with the
message. This may happen in any order.

For every statement, the condition is first evaluated. If it is truthy (not 0
or an empty string or an empty atom) or if it doesn't exist, the first action
gets evaluated and sent as a message. Otherwise, this happens with the second
action.

At the beginning of the execution of a basil program, a message with the topic
"main", an empty body and empty reply-to is pushed in the bag.

## Builtins:

Some topics are listened to by built-in blocks (that are not implemented in
basil). All built-in topics are lowercase, so it is recommended to choose
Titlecase topics in user code to avoid collision (unless collision is
intended).

A list of builtins can be seen in the file `stdB.py`.

## Example code

The typical Hello World program just sends a message with the `print` topic,
which the standard library picks up.

    main { print "Hello, World!"; }
