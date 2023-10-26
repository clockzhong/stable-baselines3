import importlib.util
import os
import sys
import time
import pytest


class MimicClass():
    test_int: int
    test_float: float
    test_string: str = "test_string............"
    def __init__(self):
        self.test_int = 323234
        self.test_float = 2.335235

def test_TestClass():
    test_obj1 = MimicClass()
    test_obj2 = MimicClass()
    print(test_obj1.test_float, test_obj2.test_float)
    print(test_obj1.test_int, test_obj2.test_int)
    print(test_obj1.test_string, test_obj2.test_string)
    test_obj1.test_int = 1
    assert test_obj1.test_int != test_obj2.test_int
    test_obj2.test_float = 0.332
    assert test_obj1.test_float != test_obj2.test_float
    test_obj2.test_string = "234asfasdfasfas"

    #test_string is not shared for all instances from MimicClass, it's also instance variables
    #assert test_obj1.test_string == test_obj2.test_string

    assert test_obj1.test_string != test_obj2.test_string

    print(test_obj1.test_float, test_obj2.test_float)
    print(test_obj1.test_int, test_obj2.test_int)
    print(test_obj1.test_string, test_obj2.test_string)

    #This is right, because test_string is initted from class level, so could be access through class
    assert MimicClass.test_string == test_obj1.test_string

    #print(MimicClass.test_int) #this is wrong because test_int is not initted in class level, so can't be used as class variables.

