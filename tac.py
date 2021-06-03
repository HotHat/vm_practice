from lua_opcode import OpCode


class Tac:
    """
    Three Address code
    """
    def __init__(self, op: OpCode, ra, rb, rc=None):
        self.op = op
        self.ra = ra
        self.rb = rb
        self.rc = rc


def opcode_ra(tac: Tac):
    return tac.ra


def opcode_rb(tac: Tac):
    return tac.rb


def opcode_rc(tac: Tac):
    return tac.rc
