import sys
import os
from antlr4 import *
sys.path.append(os.path.dirname(__file__) + '/../')
# print(sys.path)
from antlr.LuaLexer import LuaLexer
from antlr.LuaParser import LuaParser
from antlr.MyLuaListener import MyLuaListener


def main(file):
    input = FileStream(file)
    lexer = LuaLexer(input)
    stream = CommonTokenStream(lexer)
    parser = LuaParser(stream)
    listener = MyLuaListener()
    parser.addParseListener(listener)
    tree = parser.chunk()
    print(tree.toStringTree(recog=parser))
    pass


if __name__ == '__main__':

    main(os.path.dirname(__file__) + '/hello.lua')
