import unittest
from constant_pool import *
from ast import *


class TestCommon(unittest.TestCase):
    def test_constant_pool(self):
        pool = ConstantPool.instance()
        pool.add(TermNil())
        pool.add(TermFalse())
        pool.add(TermTrue())
        pool.add(TermNumber(123))
        pool.add(TermString("string"))

        print(pool.index(TermNil()))
        print(pool.index(TermFalse()))
        print(pool.index(TermTrue()))
        print(pool.index(TermNumber(123)))
        print(pool.index(TermNumber(455)))
        print(pool.index(TermString("string")))
        print(pool.index(TermString("not match")))
