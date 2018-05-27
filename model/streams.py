class Stream:
    def __init__(self, formula, name=""):
        self.formula = formula
        self.name = name
    
    def value(self, environment):
        return eval(self.formula, environment)
    
    def __repr__(self):
        return f"Stream {self.name} with formula: {self.formula}"