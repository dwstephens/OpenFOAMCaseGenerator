# boundary condition ID
INLET = 0
FREESTREAM = 1
OUTLET = 2
BACKFLOW_OUTLET = 3
ADVECTIVE_OUTLET = 4
WALL = 5
EMPTY = 6
SYMMETRY = 7
CYCLIC = 8

# outlet boundary condition ID
NEUMANN = 0
ADVECTIVE = 1
INLET_OUTLET = 2

# turbulence constant
C_MU = 0.09

# simulation type
LAMINAR = 0
RANS = 1
LES = 2

# wall modelling type
LOW_RE = 0
HIGH_RE = 1

# calculation of turbulent length scale
INTERNAL = 0
EXTERNAL = 1
RATIO = 2
RATIO_AUTO = 3

# output write control
TIME_STEP = 0
RUN_TIME = 1
ADJUSTABLE_RUN_TIME = 2
CPU_TIME = 3
CLOCK_TIME = 4

# numerical schemes
STEADY_STATE = 0
UNSTEADY = 1

# stability controlling parameter for gradient schemes
DEFAULT = 0
TVD = 1
ROBUSTNESS = 2
ACCURACY = 3