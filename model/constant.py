class Constant:
    def __init__(self, name, unit="", value=0):
        self.value = value
        self.name = name
        self.unit = unit
    
    def __repr__(self):
        return f"Constant {self.name} with value: {self.value} {self.unit}"