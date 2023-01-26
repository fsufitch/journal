import argparse

parser = argparse.ArgumentParser(description='Perform calculations on two numbers')
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
