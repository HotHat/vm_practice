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
        return f"{self.op}     {self.ra}    {self.rb}    {self.rc}"


def opcode_ra(tac: Instruction):
    return tac.ra


def opcode_rb(tac: Instruction):
    return tac.rb


def opcode_rc(tac: Instruction):
    return tac.rc
