from xkye import IO as io
import pytest
import os

#To test the missing file
def test_missing_input_file():
    xkyFile = "../test/test.xky"
    with pytest.raises(Exception):
        m = io(xkyFile)
        assert m.read() is None


#To test the read operation
def test_input_file_success():
    xkyFile = "in/test.xky"

    dir_path = os.path.dirname(os.path.realpath(__file__))
    xkyFile = dir_path+"/"+xkyFile

    xkye = io(xkyFile)
    dictionary = xkye.read()
    assert dictionary is True
