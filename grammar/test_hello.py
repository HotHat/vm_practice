import sys
import os
from antlr4 import *
sys.path.append(os.path.dirname(__file__) + '/../')
# print(sys.path)
from grammar.LuaLexer import LuaLexer
from grammar.LuaParser import LuaParser
from grammar.MyLuaListener import MyLuaListener
from graphviz import Source


def pp(s, is_source=False):
    s = f"digraph G {{{s}}}"
    if is_source:
        print(s)
    else:
        Source(s, filename="test.gv", format="png").view()

def main(file):
    input = FileStream(file)
    lexer = LuaLexer(input)
    stream = CommonTokenStream(lexer)
    parser = LuaParser(stream)
    listener = MyLuaListener()
    parser.addParseListener(listener)
    tree = parser.chunk()
    a = listener.get_chuck()
    # pp(a )
    print(tree.toStringTree(recog=parser))
    pass


if __name__ == '__main__':

    main(os.path.dirname(__file__) + '/hello.lua')
