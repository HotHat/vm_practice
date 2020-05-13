import unittest
from my_opcode import *
import vm


class TestVM(unittest.TestCase):

    def setUp(self) -> None:
        self.vm = vm.VM()

    def test_return(self):
        self.vm.add_opcode(OpReturn())
        self.assertEqual(self.vm.run(), vm.VM.VM_OK)

    def test_add(self):
        self.vm.add_opcode(OpConstant(self.vm.add_constant(10)))
        self.vm.add_opcode(OpConstant(self.vm.add_constant(200)))
        self.vm.add_opcode(OpAdd())
        self.vm.add_opcode(OpConstant(self.vm.add_constant(20)))
        self.vm.add_opcode(OpMUL())
        self.vm.add_opcode(OpConstant(self.vm.add_constant(100)))
        self.vm.add_opcode(OpDiv())
        self.vm.add_opcode(OpEcho())
        self.vm.add_opcode(OpReturn())

        self.vm.run()
        # self.assertEqual(self.vm.run(), vm.VM.VM_OK)


if __name__ == '__main__':
    unittest.main()
