from xkye import IO as io
import pytest
import os

#To test if the span for the clutch is already declared
def test_read_file_in_exception_1():
    xkyFile = "in/read_in_exception_1.xky"

    dir_path = os.path.dirname(os.path.realpath(__file__))
    xkyFile = dir_path+"/"+xkyFile

    with pytest.raises(Exception):
        xkye = io(xkyFile)
        dictionary = xkye.read()
        assert dictionary is None


#To test if the key is already declared for the clutch
def test_read_file_in_exception_2():
    xkyFile = "in/read_in_exception_2.xky"

    dir_path = os.path.dirname(os.path.realpath(__file__))
    xkyFile = dir_path+"/"+xkyFile

    with pytest.raises(Exception):
        xkye = io(xkyFile)
        dictionary = xkye.read()
        assert dictionary is None


#To test if clutchset span is greater than the declared span limit
def test_read_file_in_exception_3():
    xkyFile = "in/read_in_exception_3.xky"

    dir_path = os.path.dirname(os.path.realpath(__file__))
    xkyFile = dir_path+"/"+xkyFile

    with pytest.raises(Exception):
        xkye = io(xkyFile)
        dictionary = xkye.read()
        assert dictionary is None


#To test if clutchset is not declared with the span limit
def test_read_file_in_exception_4():
    xkyFile = "in/read_in_exception_4.xky"

    dir_path = os.path.dirname(os.path.realpath(__file__))
    xkyFile = dir_path+"/"+xkyFile

    with pytest.raises(Exception):
        xkye = io(xkyFile)
        dictionary = xkye.read()
        assert dictionary is None


#To test if subclutch is not defined before this call
def test_read_file_in_exception_5():
    xkyFile = "in/read_in_exception_5.xky"

    dir_path = os.path.dirname(os.path.realpath(__file__))
    xkyFile = dir_path+"/"+xkyFile

    with pytest.raises(Exception):
        xkye = io(xkyFile)
        dictionary = xkye.read()
        assert dictionary is None


#To test if the defined subclutch span is exceeding declared span limit
def test_read_file_in_exception_6():
    xkyFile = "in/read_in_exception_6.xky"

    dir_path = os.path.dirname(os.path.realpath(__file__))
    xkyFile = dir_path+"/"+xkyFile

    with pytest.raises(Exception):
        xkye = io(xkyFile)
        dictionary = xkye.read()
        assert dictionary is None
