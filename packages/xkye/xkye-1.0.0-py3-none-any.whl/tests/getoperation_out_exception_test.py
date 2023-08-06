from xkye import IO as io
import pytest
import os

#To test if the entity is present in the given clutch
def test_get_1_method_success_1():

    xkyFile = "in/test.xky"

    dir_path = os.path.dirname(os.path.realpath(__file__))
    xkyFile = dir_path+"/"+xkyFile

    xkye = io(xkyFile)
    xkye.read()

    valued = xkye.get("key1")

    assert valued == "value"


#To test if the entity is not present in the given clutch
def test_get_1_method_failure_1():

    xkyFile = "in/test.xky"

    dir_path = os.path.dirname(os.path.realpath(__file__))
    xkyFile = dir_path+"/"+xkyFile

    xkye = io(xkyFile)
    xkye.read()

    with pytest.raises(Exception):
        valued = xkye.get("net")
        assert valued is None


#To test if the entity for the given clutch is present
def test_get_2_method_success_1():

    xkyFile = "in/test.xky"

    dir_path = os.path.dirname(os.path.realpath(__file__))
    xkyFile = dir_path+"/"+xkyFile

    xkye = io(xkyFile)
    xkye.read()

    valued = xkye.get("shardip","shard")

    assert str(valued) == "127.0.0.1"


#To test if the entity is not in the defined clutch
def test_get_2_method_failure_1():

    xkyFile = "in/test.xky"

    dir_path = os.path.dirname(os.path.realpath(__file__))
    xkyFile = dir_path+"/"+xkyFile

    xkye = io(xkyFile)
    xkye.read()

    with pytest.raises(Exception):
        valued = xkye.get("net","shard")
        assert valued is None


#To test if the cluth string is not defined
def test_get_2_method_failure_2():

    xkyFile = "in/test.xky"

    dir_path = os.path.dirname(os.path.realpath(__file__))
    xkyFile = dir_path+"/"+xkyFile

    xkye = io(xkyFile)
    xkye.read()

    with pytest.raises(Exception):
        valued = xkye.get("net","net")
        assert valued is None



#To test the output for the given clutch, clutchspan & entity
def test_get_3_method_success_1():

    xkyFile = "in/test.xky"

    dir_path = os.path.dirname(os.path.realpath(__file__))
    xkyFile = dir_path+"/"+xkyFile

    xkye = io(xkyFile)
    xkye.read()

    valued = xkye.get("shardsubnet","shard", 3)

    assert str(valued) == "192.168.0.0/24"


#To test the output for the given default clutch & entity
def test_get_3_method_success_2():

    xkyFile = "in/test.xky"

    dir_path = os.path.dirname(os.path.realpath(__file__))
    xkyFile = dir_path+"/"+xkyFile

    xkye = io(xkyFile)
    xkye.read()

    valued = xkye.get("shardip","shard", 3)

    assert str(valued) == "127.0.0.1"

#To test the output for the given default clutch & entity
def test_get_3_method_success_3():

    xkyFile = "in/test.xky"

    dir_path = os.path.dirname(os.path.realpath(__file__))
    xkyFile = dir_path+"/"+xkyFile

    xkye = io(xkyFile)
    xkye.read()

    valued = xkye.get("shardip","shard", 2)

    assert str(valued) == "127.0.0.1"


#To test if the clutch is not declared
def test_get_3_method_failure_1():

    xkyFile = "in/test.xky"

    dir_path = os.path.dirname(os.path.realpath(__file__))
    xkyFile = dir_path+"/"+xkyFile

    xkye = io(xkyFile)
    xkye.read()

    with pytest.raises(Exception):
        valued = xkye.get("shardip","net",3)
        assert valued is None


#To test if the clutch is not defined & entity is not in default clutch
def test_get_3_method_failure_2():

    xkyFile = "in/test.xky"

    dir_path = os.path.dirname(os.path.realpath(__file__))
    xkyFile = dir_path+"/"+xkyFile

    xkye = io(xkyFile)
    xkye.read()

    with pytest.raises(Exception):
        valued = xkye.get("net","shard",6)
        assert valued is None


#To test if the entity is not in clutch as well as default clutch
def test_get_3_method_failure_3():

    xkyFile = "in/test.xky"

    dir_path = os.path.dirname(os.path.realpath(__file__))
    xkyFile = dir_path+"/"+xkyFile

    xkye = io(xkyFile)
    xkye.read()

    with pytest.raises(Exception):
        valued = xkye.get("net","shard",3)
        assert valued is None
