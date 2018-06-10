from model.constant import Constant
from model.variable import Variable
import inspect

class _Model:
    
    def __init__(self, name, max_t=1000, dt=0.1, infinite=False):
        if infinite:
            self.max_t = float("inf")
        else:
            self.max_t = max_t
        self.name = name
        self.vars = {}
        self.dt = 0.1
        self.t = 0
        self.stops = []
    
    def add_var(self, obj):
        self.vars[obj.name] = obj

    def add_vars(self, *objs):
        for i in objs:
            self.vars[i.name] = i
    
    def add_scope(self, scope):
        for key, i in scope.items():
            if isinstance(i, Constant) or isinstance(i, Variable):
                if i.name == "":
                    i.name = key
                    self.vars[key] = i
                else:
                    self.vars[i.name] = i

    def compose_environment(self):
        environment = {}
        for i in self.vars.values():
            environment[i.name] = i.value
        environment.update({
            "dt": self.dt,
            "t": self.t
        })
        return environment
    
    def init_save(self):
        self.save = {}
        for i in self.vars.keys():
            self.save[i] = []

    def do_save(self):
        for i in self.vars.values():
            self.save[i.name].append(i.value)
    
    def add_stop(self, formula):
        self.stops.append(formula)
    
    def stop(self, environment):
        for i in self.stops:
            if eval(i, environment):
                return True
        return False

    def initial_defines(self):
        environment = self.compose_environment()
        for i in self.vars.values():
            if isinstance(i, Variable):
                if i.defined:
                    self.vars[i.name].tick(environment)
    
    def loop(self, save=False):
        if save: self.init_save()
        while self.t < self.max_t:
            if save: self.do_save()
            environment = self.compose_environment()
            if self.stop(environment):
                return
            for i in self.vars.values():
                if hasattr(i, "tick"):
                    i.tick(environment)
            self.t += self.dt
    
    def import_matplotlib(self):
        try:
            from matplotlib import pyplot
            self.plt = pyplot
            return True
        except ImportError:
            return False
    
    def plot(self, var):
        if self.import_matplotlib():
           self.plt.plot(self.save[var], label=var)
    
    def show(self):
        if self.import_matplotlib():
            self.plt.legend()
        self.plt.show()
        

    def __repr__(self):
        base = f"Model {self.name}, duration: {self.max_t} s"
        for i in self.vars.values():
            base += f"\n{i}"
        return base



class Model(_Model):
    kwargs = {}
    def __init__(self,*args,**kwargs):
        super().__init__(self.kwargs)
        self.add_scope(self.__class__.__dict__)

    def __init_subclass__(cls,**kwargs):
        cls.kwargs = kwargs
        super().__init_subclass__()