def test_smoke():
    assert True

def test_smoke1():
    assert True

from calculator import calculate_expression


def test_calculate_addition():
    assert calculate_expression('22+18') == '40'


def test_calculate_subtraction():
    assert calculate_expression('50-25') == '25'


def test_calculate_multiplication():
    assert calculate_expression('6*7') == '42'


def test_calculate_division():
    assert calculate_expression('100/4') == '25.0'


def test_calculate_with_spaces():
    assert calculate_expression('10 + 5') == '15'


def test_calculate_with_parentheses():
    assert calculate_expression('(10+5)*2') == '30'


def test_calculate_decimal():
    assert calculate_expression('3.5+2.5') == '6.0'


def test_calculate_complex_expression():
    assert calculate_expression('10+5*2') == '20'


def test_calculate_invalid_characters():
    assert calculate_expression('10+abc') is None


def test_calculate_empty_string():
    assert calculate_expression('') is None

