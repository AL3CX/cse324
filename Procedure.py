import Environment

class Procedure(object):
    def __init__(self, params, body, env):
        self.params = params
        self.body = body
        self.env = env
    def __call__(self, *args):
        inner_env = Environment(outer=self.env)
        for param, arg in zip(self.params, args):
            inner_env.variables[param] = arg
        return eval(self.body, inner_env)