from lua_opcode import OpCode


class Instruction:
    """
    Three Address code
    """
    def __init__(self, op: OpCode, ra, rb, rc=None):
        self.op = op
        self.ra = ra
        self.rb = rb
        self.rc = rc

    def __str__(self):
        c = '' if self.rc is None else self.rc
        return f"{self.op:<15}{'':>8}{self.ra:>5}{'':>8}{self.rb:>5}{'':>8}{c}"


def opcode_ra(tac: Instruction):
    return tac.ra


def opcode_rb(tac: Instruction):
    return tac.rb


def opcode_rc(tac: Instruction):
    return tac.rc
