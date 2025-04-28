from definitions import SYMBOL

def tokenize(string: str) -> list:
    """
    Convert a string into a list of tokens.

    Parameters:
    string (str): target string to turn into a list of tokens separated by space.

    Returns:
    list: the list of tokens.
    """
    # Add spaces to paranthesis and quote so that it is a separate token
    return string.replace('(',' ( ').replace(')', ' ) ').replace("'", " ' ").split()



def structure_tokens(tokens: list):
    """
    Convert list of tokens into lisp expressions recursively

    Parameters:
    tokens (list): list of tokens to convert

    Returns:
    EXP: lisp expression
    """
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF')
    token = tokens.pop(0)
    if token == '(':
        L = []
        while tokens[0] != ')':
            L.append(structure_tokens(tokens))
        tokens.pop(0) # tokens[0] is ) so pop it
        return L
    elif token == ')':
        raise SyntaxError('unexpected )')
    elif token == "'":
        return ['quote', structure_tokens(tokens)]
    else:
        return to_atom(token)


def to_atom(token: str):
    """
    Convert token to a lisp atom

    Parameters:
    token (str): target token to convert

    Returns:
    ATOM: lisp atom
    """
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return SYMBOL(token)


def parse(raw_expression: str):
    """
    Convert a string into a lisp expression

    Parameters:
    raw_expression (str): raw expression as a string to convert into a lisp expression

    Returns:
    EXP: lisp expression
    """
    return structure_tokens(tokenize(raw_expression))
