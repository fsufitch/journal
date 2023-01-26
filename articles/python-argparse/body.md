:::alert info
**Note:** This post is merely an admonition/reminder that tools to make your code cleaner and
better when handling command line arguments _exist_. It is not a tutorial. There's already plenty
of good ones out there, like the [official one](https://docs.python.org/3/howto/argparse.html).
:::

Suppose you need to write a `calculator.py` script which can add, subtract, multiply, or divide two numbers.
It needs to let the user manipulate the behavior using CLI flags, and have a useful `--help`
message. Does that sound scary? Does it sound like you need to write something like this?

```python
import sys
from typing import List

show_help: bool = False
operands: List[str] = []
operation: str = ''

args_iter = iter(sys.args)
for current_arg in args_iter:
    if current_arg in ['-h', '--help']:
        show_help = True
	break
    if current_arg in ['-o', '--operation']:
        operation = next(args_iter)
        continue
    operands.append(current_arg)

if show_help:
   print('''
   SOME BIG HELP MESSAGE HERE
   ''')
   sys.exit(1)

if operation not in ['+', '-', '*', '/']:
   raise ValueError('Invalid operation', operation)

if len(operands) != 2:
   raise ValueError('Expected two operands, but got: ' + str(operands))

op1 = float(operands[0])
op2 = float(operands[1])

### Actual math starts here

operations = {
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '*': lambda x, y: x * y,
    '/': lambda x, y: x / y,
}

result = operations[operation](op1, op2)

print(result)
```

All that to just achieve...

```
$ python calculator.py 1 -o + 2
3
```

:::imagecard center argparse-meme.jpg
:::

Doesn't it suck to have that much space dedicated to parsing/handling input arguments?
Wouldn't it be cool if Python could help out there? Isn't it supposed to be super clean and
convenient?

## Python can help you, if you let it!

Parsing arguments is a nasty bit of code, and in their neverending wisdom, the creators of Python
anticipated that it would be a common use case for programmers who use the language. Thus, they
included the excellent `argparse` library.

How excellent is it? Well, let's use it for the code from above:

```python
import argparse

parser = argparse.Parser(description='Perform calculations on two numbers')
parser.add_argument('-o', '--operation', choices=['+', '-', '*', '/'], required=True,
    help='Which operation to perform')
parser.add_argument('op1', type=float, help='The first number')
parser.add_argument('op2', type=float, help='The second number')
args = parser.parse_args()

### Actual math starts here

operations = {
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '*': lambda x, y: x * y,
    '/': lambda x, y: x / y,
}

result = operations[args.operation](args.op1, args.op2)

print(result)
```

Isn't that so much neater? Here are some (honestly, huge!) advantages that this approach has:

* Validity checking of the arguments is done automatically; the operation *will* be one of the
  specified choices, there won't be more than one operation specified, there will only be two
  operands, and so forth.
* The operands get converted into floats by the parser, so there's no need for you to do it yourself
  (and possibly get it wrong).
* It supports multiple styles of specifying arguments! `-o+`, `-o '+'`, and `--operation=+` all work!
* The second approach is far shorter.
* It generates the help message for you! Check this out:

```
$ python calculator.py --help
usage: calculator.py [-h] -o {+,-,*,/} op1 op2

Perform calculations on two numbers

positional arguments:
  op1                   The first number
  op2                   The second number

optional arguments:
  -h, --help            show this help message and exit
  -o {+,-,*,/}, --operation {+,-,*,/}
                        Which operation to perform
```

`argparse` has many other features which I did not go into above. Defaults, subcommands, mutually
exclusive arguments (think if your script had `--verbose` and `--silent`)... It is quite comprehensive.
For myself, it has actually been a huge motivation to use Python instead of plain Bash scripts
in the past. It is seriously one of the best parts of Python being a "batteries included" language.

So what are you waiting for? Go out and make awesome scripts!

:::alert info
This admonition and "call to action" applies to every other language out there&mdash;be it another built-in library like Go's [`flag`](https://pkg.go.dev/flag), or a 3rd party tool like [Apache Commons CLI](https://commons.apache.org/proper/commons-cli/index.html) for Java. Someone has likely already done the hard work of making a clean, feature-ful CLI parser; why not make use of it?
:::
