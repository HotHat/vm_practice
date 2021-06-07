from enum import Enum


# class ExpKind(Enum):
#     """ kinds of variables/expressions """
#     VVOID = 1 # / *when 'expdesc' describes the last expression a list, this kind means an empty list(so, no expression) * /
#     VNIL = 2 #/ *constant nil * /
#     VTRUE = 3  # / *constant true * /
#     VFALSE = 4 # / *constant false * /
#     VK = 5 #/ *constant in 'k'; info = index of constant in 'k' * /
#     VKFLT = 6 # / *floating constant; nval = numerical float value * /
#     VKINT = 7 # / *integer constant; nval = numerical integer value * /
#     VNONRELOC = 8 # / *expression has its value in a fixed register; info = result register * /
#     VLOCAL = 9 # / *local variable; info = local register * /
#     VUPVAL = 10 # / *upvalue variable; info = index of upvalue in 'upvalues' * /
#     VINDEXED = 11 # / *indexed variable; ind.vt = whether 't' is register or upvalue; ind.t = table register or upvalue; ind.idx = key 's R/K index */
#     VJMP = 12 # / *expression is a test / comparison; info = pc of corresponding jump instruction * /
#     VRELOCABLE = 13 # / *expression can put result in any register; info = instruction pc * /
#     VCALL = 14 # / *expression is a function call; info = instruction pc * /
#     VVARARG = 15 #/ * vararg expression; info = instruction pc * /


class VarType(Enum):
    NIL = 1
    BOOL = 2
    INTEGER = 3
    FLOAT = 4
    STRING = 5
    CLOSURE = 6


class SymbolType(Enum):
    CONSTANT = 1
    VARIABLE = 2
    CLOSURE = 3
    TEMPORARY = 4



