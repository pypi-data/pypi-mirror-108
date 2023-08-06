from xkye import IO as io
import pytest
import os


#To test if clutch span and clutch is not defined & the entity is not in the defined clutch
def test_read_file_out_exception_1():
    xkyFile = "in/read_out_exception_1.xky"

    dir_path = os.path.dirname(os.path.realpath(__file__))
    xkyFile = dir_path+"/"+xkyFile

    with pytest.raises(Exception):
        xkye = io(xkyFile)
        dictionary = xkye.read()
        assert dictionary is None


#To test if clutch span is not defined & the entity is not in the defined clutch
def test_read_file_out_exception_2():
    xkyFile = "in/read_out_exception_2.xky"

    dir_path = os.path.dirname(os.path.realpath(__file__))
    xkyFile = dir_path+"/"+xkyFile

    with pytest.raises(Exception):
        xkye = io(xkyFile)
        dictionary = xkye.read()
        assert dictionary is None


#To test if clutch span is not defined & the defined clutch is none
def test_read_file_out_exception_3():
    xkyFile = "in/read_out_exception_3.xky"

    dir_path = os.path.dirname(os.path.realpath(__file__))
    xkyFile = dir_path+"/"+xkyFile

    with pytest.raises(Exception):
        xkye = io(xkyFile)
        dictionary = xkye.read()
        assert dictionary is None


#To test if clutch(shard3) is none and entity not in default clutch(shard)
def test_read_file_out_exception_4():
    xkyFile = "in/read_out_exception_4.xky"

    dir_path = os.path.dirname(os.path.realpath(__file__))
    xkyFile = dir_path+"/"+xkyFile

    with pytest.raises(Exception):
        xkye = io(xkyFile)
        dictionary = xkye.read()
        assert dictionary is None


#To test the scenario when the resquested clutch and its default clutch is none
def test_read_file_out_exception_5():
    xkyFile = "in/read_out_exception_5.xky"

    dir_path = os.path.dirname(os.path.realpath(__file__))
    xkyFile = dir_path+"/"+xkyFile

    with pytest.raises(Exception):
        xkye = io(xkyFile)
        dictionary = xkye.read()
        assert dictionary is None


#To test if entity not in both clutch(shard3) and default clutch(shard)
def test_read_file_out_exception_6():
    xkyFile = "in/read_out_exception_6.xky"

    dir_path = os.path.dirname(os.path.realpath(__file__))
    xkyFile = dir_path+"/"+xkyFile

    with pytest.raises(Exception):
        xkye = io(xkyFile)
        dictionary = xkye.read()
        assert dictionary is None
