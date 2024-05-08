from project_functions import get_whole_map, validate_guess, convert
import numpy as np


def test_vlidate_guess():
    assert validate_guess("-sA1") == True
    assert validate_guess("-f A10") == True
    assert validate_guess("-a A6") == False
    assert validate_guess("-s A0") == False
    assert validate_guess("-s A11") == False


def test_get_whole_map():
    m = np.zeros((10,10))
    m[0,0] = 9
    mw = np.zeros((10,10))
    mw[0:2,0:2] = 1
    mw[0,0] = 9
    assert np.all(get_whole_map(m) == mw)
    m[5,5] = 9
    mw[4:7,4:7] = 1
    mw[5,5] = 9
    assert np.all(get_whole_map(m) == mw)


def test_convert():
    assert convert("-s A6") == ["s", [1,6]]
    assert convert("-f A10") == ["f", [1,10]]
    assert convert("-f J7") == ["f", [10,7]]
    assert convert("-fJ7") == ["f", [10,7]]
    assert convert("-fj7") == ["f", [10,7]]