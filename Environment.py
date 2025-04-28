class Environment: 
    def __init__(self, outer=None):
        self.variables = {}
        self.outer = outer
        
    def find(self, var):
        if var in self.variables:
            return self
        elif self.outer:
            return self.outer.find(var)
        else:
            raise NameError(f"Undefined variable: {var}")