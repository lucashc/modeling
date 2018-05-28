from model import Model
from model import Variable as V
from model import Constant as C
from model import Stream as S

# Define model
model = Model("Car", dt=0.1, max_t=300) # 300 seconds of modeling

# Constants
Froll = C(unit="N", value=1000) # Roll resistance
k = C(value=0.1) # Air resistance coefficient
m_base = C(unit="kg", value=1000) # Base mass
rch = C(unit="J/kg", value=46e6) # Combustion energy density
Fm = C(unit="N", value=1050) # Motor force

# Variabless

s = V(unit="m") # Distance
v = V(unit="m/s") # Velocity
a = V(unit="m/s^2") # Acceleration
a.define("Fnetto/m")

Pm = V(unit="J/s")
Pm.define("Fnetto*v")

m_fuel = V(unit="kg", start=10) # Fuel mass

m = V(unit="kg", start=m_base.value + m_fuel.value)
m.define("m_base+m_fuel")

Flw = V(unit="N")
Flw.define("k*v**2")

Fnetto = V(unit="N") # Netto force
Fnetto.define("Fm-Froll-Flw")

# Connections
s < S("v*dt") # Distance increases with speed
v < S("a*dt") # Velocity increases with acceleration
m_fuel > S("Pm*dt/rch") # Fuel decreases with motor power

# Start model
model.add_scope(locals())
model.add_stop("m_fuel <= 0")
model.loop(True)

# Show results

model.plot("s")
model.show()