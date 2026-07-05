def addup(a, b):
    return a + b


def area_of_circle(radius):
    import math

    return math.pi * radius**2


def test_addup():
    assert addup(1, 2) == 3


def test_multiply():
    assert multiply(3, 4) == 12


def test_area_of_circle():
    radius = 10
    assert area_of_circle(radius) == 314.1592653589793
