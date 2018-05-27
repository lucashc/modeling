from model.streams import Stream

class Variable:
    def __init__(self, name, unit="",start_value=0):
        self.value = start_value
        self.streams = []
        self.name = name
        self.definition = ""
        self.unit = unit
        self.defined = False

    def addstream(self, stream):
        self.streams.append(stream)
    
    def tick(self, environment):
        if self.definition != "":
            self.value = eval(self.definition, environment)
        for i in self.streams:
            self.value += i.value(environment)
    
    def define(self, definition):
        self.definition = definition
        self.defined = True
    
    def __lt__(self, stream):
        if isinstance(stream, Stream):
            self.streams.append(stream)
        else:
            raise TypeError("Must be of type Stream")
    
    def __gt__(self, stream):
        if isinstance(stream, Stream):
            stream.formula = "-(" + stream.formula + ")"
            self.streams.append(stream)
        else:
            raise TypeError("Must be of type Stream")
    
    def __repr__(self):
        base = f"Variable {self.name}, with value: {self.value} {self.unit}\n"
        if self.definition != "":
            return base + f"  Defined as: {self.definition}"
        else:
            return base + f"  Streams: {self.streams}"
    
    