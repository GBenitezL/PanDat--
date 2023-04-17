import sys
from compiler.lexer import LexerClass
from compiler.parser import ParserClass

lexer = LexerClass()
parser = ParserClass()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        file = sys.argv[1]
        try:
            with open(file, 'r') as f:
                data = f.read()
            if (parser.parse(lexer.tokenize(data))) == 'ok':
                print("Parsed Successfully")
        except EOFError:
            print("Error: end of file reached unexpectedly")
        finally:
            f.close()
    else:
        print("No file was found")