# Type Definitions
SYMBOL = str
NUMBER = (int, float)     # int or float
LIST   = list
ATOM   = (SYMBOL, NUMBER) # symbol or number
EXP    = (ATOM, LIST)     # Expression will either be atom or list
