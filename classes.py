class Environment:
    """
    Environment class for storing and retrieving variables in a nested context.
    """
    def __init__(self, outer=None):
        """
        Initialize a new Environment.

        Parameters:
            outer (Environment, optional): The outer environment (parent scope). Defaults to None.
        """
        self.variables = {}
        self.outer = outer

    def find(self, var):
        """
        Find the innermost Environment where var appears.

        Parameters:
            var (str): The variable name to look up.

        Returns:
            Environment: The environment where the variable is defined.

        Raises:
            NameError: If the variable is not found in this environment or any outer environment.
        """
        if var in self.variables:
            return self
        elif self.outer:
            return self.outer.find(var)
        else:
            raise NameError(f"Undefined variable: {var}")


class Procedure(object):
    def __init__(self, params, body, env):
        self.params = params
        self.body = body
        self.env = env
    def __call__(self, *args):
        inner_env = Environment(outer=self.env)
        for param, arg in zip(self.params, args):
            inner_env.variables[param] = arg
        return (self.body, inner_env)
