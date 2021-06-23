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

        print(pool.get(TermNil()))
        print(pool.get(TermFalse()))
        print(pool.get(TermTrue()))
        print(pool.get(TermNumber(123)))
        print(pool.get(TermNumber(455)))
        print(pool.get(TermString("string")))
        print(pool.get(TermString("not match")))
