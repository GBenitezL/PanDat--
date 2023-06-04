import sys
from compiler.lexer import LexerClass
from compiler.parser import ParserClass, scopes, quadruples, constants_table
from compiler.virtual_machine import start_vm

lexer = LexerClass()
parser = ParserClass()

def print_quadruples():
    print('Quadruples\n')
    for index, quad in enumerate(quadruples):
        print(index, end='') 
        quad.print()

def print_scopes():
    print('Scopes Directory\n')
    scopes.print_directory()

def print_constants():
    print('Constants Directory\n')
    for index, const in enumerate(constants_table):
        print(index, '\t\t', const, '\t\t', constants_table[const])


def main(argv):
    if len(argv) != 2:
        sys.exit("To run a program, type the following command structure: python main.py file_name.pdat")
    file = argv[1]

    if str(file)[-5:] != ".pdat":
        sys.exit("Only files with extension \".pdat\" can be executed")

    if len(sys.argv) > 1:
        file = sys.argv[1]
        try:
            with open(file, 'r') as f:
                data = f.read()
            if (parser.parse(lexer.tokenize(data))) == 'ok':
                print("Parsed Successfully")
        except EOFError:
            print("Error: Reached end of file reached unexpectedly")
        finally:
            f.close()
    else:
        print("No file was found")
    
    start_vm()

if __name__ == "__main__":
    main(sys.argv)
    # print_scopes()
    # print_quadruples()
    # print_constants()