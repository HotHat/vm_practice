from enum import Enum


class OpCode(Enum):
    NOP = 0
    MOVE = 1
    LOADK = 2
    LOADKX = 3
    LOADBOOL = 4
    LOADNIL = 5
    GETUPVAL = 6
    GETTABUP = 7
    GETTABLE = 8
    SETTABUP = 9
    SETUPVAL = 10
    SETTABLE = 11
    NEWTABLE = 12
    SELF = 13
    ADD = 14
    SUB = 15
    MUL = 16
    MOD = 17
    POW = 18
    DIV = 19
    IDIV = 20
    BAND = 21
    BOR = 22
    BXOR = 23
    SHL = 24
    SHR = 25
    UNM = 26
    BNOT = 27
    NOT = 28
    LEN = 29
    CONCAT = 30
    JMP = 31
    EQ = 32
    LT = 33
    LE = 34
    TEST = 35
    TESTSET = 36
    CALL = 37
    TAILCALL = 38
    RETURN = 39
    FORLOOP = 40
    FORPREP = 41
    TFORLOOP = 42
    TFORCALL = 43
    SETLIST = 44
    CLOSURE = 45
    VARARG = 46

