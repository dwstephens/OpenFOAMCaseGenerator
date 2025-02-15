from input import GlobalVariables as Parameters

from math import sqrt, pow, log10, floor, sin, cos, pi
import os
import json


class CaseProperties:
    def __init__(self):
        self.properties = {
            'file_properties': {
                # name of the case to use (will be used for the folder name)
                'case_name': 'taylor_green_vortex20',

                # specify how the mesh should be incorporated into the case directory
                #   The following types are supported
                #   NO_MESH:                                Don't do anything, leave mesh treatment up to user
                #   BLOCK_MESH_DICT:                        Copy blockMeshDict file into case, requires the path to the
                #                                           file
                #   BLOCK_MESH_AND_SNAPPY_HEX_MESH_DICT:    Copy both blockMeshDict and snappyHexMeshDict to directory,
                #                                           requires the path to both files
                #   POLY_MESH:                              Specify a polyMesh directory and copy it into the case setup
                'mesh_treatment': Parameters.BLOCK_MESH_DICT,

                # directory where the blockMeshDict file is located (needs to be named blockMeshDict)
                'blockmeshdict_directory': os.path.join('examples', 'mesh', 'TaylorGreenVortex'),

                # directory where the snappyHexMeshDict file is located (needs to be named snappyHexMeshDict)
                'snappyhexmeshdict_directory': os.path.join(''),

                # directory where the polyMesh is located (the specified directory needs to contain a folder called
                # polyMesh which in turn contains the boundary, cellZones, faces, faceZones, neighbour, owner and points
                # files)
                'polymesh_directory': os.path.join(''),

                # path to where the currently generated case should be copied to (parent directory)
                # if left empty, the case will be written into the current directory
                'run_directory': os.path.join(''),

                # version of openfoam to use (does not have an influence on the case setup, but will be used in headers)
                'version': 'v2006',
            },

            # setting up simulation for parallel processing
            'parallel_properties': {
                # flag indicating if simulation will be run in parallel. If true, additional information for domain
                # decomposition will be written (and Allrun script modified, accordingly)
                'run_in_parallel': True,

                # number of processors that will be used to run case in parallel
                'number_of_processors': 4,
            },

            # properties imposed at boundaries / freestream
            'boundary_properties': {
                # define boundary conditions
                #   first  entry: name of boundary condition (specified in mesh generator)
                #   second entry: type of boundary condition (see below)
                #
                #   The following types are supported
                #   INLET:            Standard inlet condition, dirichlet for velocity + turbulence, neumann for
                #                     pressure
                #   DFSEM_INLET:      Divergence Free Synthetic Eddy Method (DFSEM) Inlet, use for Large-Eddy Simulation
                #                     to artificially create turbulent fluctuations at the inlet.
                #   FREESTREAM:       Specify freestream condition globally (can be inlet and outlet)
                #   OUTLET:           Standard outlet, fixed pressure and Neumann for velocity + turbulence
                #                     (Reflective outlet)
                #   BACKFLOW_OUTLET:  Same as outlet, but allows for flow to re-enter the domain (backflow at outlet)
                #   ADVECTIVE_OUTLET: Quantities are forced / advected outside domain (Non-reflective outlet)
                #   WALL:             Standard wall condition (ensure that the mesh has the type wall boundary assigned
                #                     instead of patch)
                #   EMPTY:            Used for essentially 2D simulations on the symmetry plane
                #   SYMMETRY:         Symmetry plane condition, i.e. wall with slip condition
                #                     (Neumann condition for all quantities)
                #   CYCLIC:           Use for periodic flows (mesh needs to have CYCLIC conditions defined)
                'boundary_conditions': {
                    'top': Parameters.CYCLIC,
                    'bottom': Parameters.CYCLIC,
                    'left': Parameters.CYCLIC,
                    'right': Parameters.CYCLIC,
                    'front': Parameters.CYCLIC,
                    'back': Parameters.CYCLIC,
                },

                # specify if custom inlet boundary conditions should be used for this case setup. If set to true, this
                # will require the dictionary entry for custom_inlet_boundary_conditions_setup
                'custom_inlet_boundary_conditions': False,

                # if custom inlet boundary conditions should be used, this dictionary provides a mapping where the key
                # is used to identify for which variable custom inlet boundary conditions should be written. The value
                # is a path to the c++ script which should be used as the custom inlet boundary condition
                'custom_inlet_boundary_conditions_setup': {
                    'p': os.path.join('examples', 'scripts', 'boundaryConditions', 'generic', 'scalarField'),
                    'U': os.path.join('examples', 'scripts', 'boundaryConditions', 'generic', 'vectorField'),
                },

                # start DFSEM Inlet only section -----------------------------------------------------------------------
                # the below options are for the special DFSEM Inlet only. Use with caution. Before using, see remarks at
                # https://www.cfd-online.com/Forums/openfoam-solving/177711-turbulentdfseminlet.html

                # specify whether custom inlet or freestream conditions should be set
                'custom_DFSEM_conditions': False,

                # if custom DFSEM conditions should be set, specify the path which the custom conditions are stored
                'custom_DFSEM_conditions_setup': {
                    'R': os.path.join('examples', 'scripts', 'boundaryConditions', 'generic', 'tensorField'),
                    'U': os.path.join('examples', 'scripts', 'boundaryConditions', 'generic', 'vectorField'),
                    'L': os.path.join('examples', 'scripts', 'boundaryConditions', 'generic', 'scalarField'),
                },

                # specify the reynold stresses at the inlet, ignored if custom_DFSEM_conditions is set to True and R is
                # specified in custom_DFSEM_conditions_setup. The order is R_uu, R_uv, R_uw, R_vv, R_vw, R_ww
                'reynolds_stresses': [1, 0, 0, 0, 0, 0],

                # set turbulent length scale at inlet? If true, the turbulent length scale needs to be provided, if
                # false, we need to specify how many cells we want to use to resolve turbulent eddies (dynamically
                # adjust to the mesh size and controls the dissipation, use this option of no length scale information
                # is available). If custom_DFSEM_conditions is set to true and L is specified in
                # custom_DFSEM_conditions_setup, then this choice will have no effect
                'set_turbulent_length_scale_at_inlet': False,

                # turbulent length scale
                'turbulent_length_scale': 0.004,

                # number of cells to use to resolve turbulent eddies if no turbulent length scale is given. Typical
                # values should be between 1 - 5, where values closer to 1 are more dissipative and values closer to 5
                # sustain eddies for longer. Only used if both custom_DFSEM_conditions and
                # set_turbulent_length_scale_at_inlet are set to false.
                'number_of_cells_per_eddy': 1,
                # end DFSEM Inlet only section -------------------------------------------------------------------------
            },

            # physical properties of solver set-up
            'flow_properties': {
                # specify if custom initial conditions should be used for this case setup. If set to true, this will
                # require the dictionary entry for custom_initial_conditions_setup
                'custom_initial_conditions': True,

                # if custom initial conditions should be used, this dictionary provides a mapping where the key is
                # used to identify for which variable custom initial conditions should be written. The value is a
                # path to the c++ script which should be used as the custom initial condition
                'custom_initial_conditions_setup': {
                    'p': os.path.join('examples', 'scripts', 'initialConditions', 'taylorGreenVortex', 'incompressible',
                                      'p'),
                    'U': os.path.join('examples', 'scripts', 'initialConditions', 'taylorGreenVortex', 'incompressible',
                                      'U'),
                },

                # specify how the initial field should be set for non-custom initial conditions
                #   BOUNDARY_CONDITIONED_BASED: set the initial field based on inlet conditions (where applicable)
                #   ZERO_VELOCITY:              set the initial field to a zero velocity field
                'initial_conditions': Parameters.BOUNDARY_CONDITIONED_BASED,

                # type of the flow to solve
                #   The following types are supported:
                #     incompressible:   Solve the flow using a constant density approach
                #     compressible:     Solve the flow using a variable density approach
                'flow_type': Parameters.incompressible,

                # flag indicating whether viscosity should be constant or variable (only applicable to compressible
                # flows, in which case sutherland's law will be used to compute it)
                'const_viscosity': True,

                # specify whether input parameters should be specified using dimensional or non-dimensional parameters
                #   DIMENSIONAL:        Use dimensional quantities. Properties from the dimensional_properties
                #                       dictionary will be used
                #   NON_DIMENSIONAL:    Use non-dimensional quantities. Properties from the non_dimensional_properties
                #                       dictionary will be used
                'input_parameters_specification_mode': Parameters.DIMENSIONAL,

                # properties used when input parameters are specified using dimensional properties
                'non_dimensional_properties': {
                    # Reynolds number
                    'Re': 6000000,

                    # Mach number (only used for compressible flows)
                    'Ma': 0.15,
                },

                # properties used when input parameters are specified using dimensional properties
                'dimensional_properties': {
                    # specify the inlet velocity magnitude. The vector components will be constructed using the
                    # axis_aligned_flow_direction properties.
                    'velocity_magnitude': 1.0,

                    # specify density at inlet / freestream (only used for compressible calculations)
                    'rho': 1.0,

                    # specify the laminar viscosity (used for incompressible flows or compressible, if viscosity is set
                    # to const)
                    'nu': 6.25e-4,

                    # specify total pressure at inlet / freestream (ignored for incompressible flows, here,
                    # static pressure will be used and will be set to 0 by default)
                    'p': 0,

                    # specify temperature at inlet / freestream
                    'T': 300,
                },

                # specify the direction of the inflow velocity vector. Will be used to construct a 3D vector based on
                # the velocity magnitude. The tangential flow direction is aligned with the flow while the the normal
                # direction is perpendicular to it. To alter the direction within the plane that these two directions
                # span, use the angle_of_attack property. The property specified here will also be used to set up the
                # force coefficient calculation if required.
                'axis_aligned_flow_direction': {
                    'tangential': Parameters.X,
                    'normal': Parameters.Y,
                    'angle_of_attack': 0,
                },
            },

            'solver_properties': {
                # name of solver to use for solving the Navier-Stokes equations
                #   incompressible:
                #     simpleFoam:       steady state, turbulent (RANS) solver based on the SIMPLE algorithm
                #     icoFoam:          unsteady, non-turbulent (only laminar) solver based on the PISO algorithm
                #     pisoFoam:         unsteady, turbulent (RANS, LES) solver based on the PISO algorithm
                #     pimpleFoam:       unsteady, turbulent (RANS, LES) solver based on the SIMPLE + PISO algorithm.
                #                       May use higher CFL numbers than pisoFoam while being more stable.
                #                       Recommended in general
                #
                #   compressible:
                #     rhoCentralFoam:   Density-based compressible flow solver based on central-upwind schemes of
                #                       Kurganov and Tadmor
                #     rhoSimpleFoam:    Steady-state solver for compressible turbulent flow
                #     rhoPimpleFoam:    Transient solver for turbulent flow of compressible fluids for Heating,
                #                       ventilation, and air conditioning (HVAC) and similar applications, with optional
                #                       mesh motion and mesh topology changes
                #     sonicFoam:        Transient solver for trans-sonic/supersonic, turbulent flow of a compressible
                #                       gas
                'solver': Parameters.pimpleFoam,

                # name of the solver to use to solve the implicit system of equations for the pressure
                #   MULTI_GRID:     Use OpenFOAM's geometric agglomerated algebraic multigrid (GAMG). May be less
                #                   efficient for parallel computations and non-elliptic flow problems
                #                   (e.g. compressible flows)
                #   KRYLOV:         Use OpenFOAM's Krylov subspace solver (Conjugate Gradient) with preconditioning.
                #                   Recommended to use for compressible and parallel computations
                'pressure_solver': Parameters.KRYLOV,

                # start time
                'startTime': 0,

                # end time
                'endTime': 20,

                # specify from which time directory to start from
                #   START_TIME:  Start from the folder that is defined in the startTime variable
                #   FIRST_TIME:  Start from the first available (lowest time) directory
                #   LATEST_TIME: Start from the latest available (highest time) directory. Use to restart a simulation
                #                from the last calculated solution
                'startFrom': Parameters.START_TIME,

                # flag indicating whether to dynamically calculate time step based on CFL criterion
                'CFLBasedTimeStepping': False,

                # CFL number
                'CFL': 1.0,

                # time step to be used (will be ignored if CFL-based time stepping is chosen)
                # WARNING: solver needs to support adjustable deltaT calculation
                'deltaT': 1e-2,

                # largest allowable time step
                'maxDeltaT': 1,

                # frequency at which to write output files. Behaviour controlled through write control entry below.
                'write_frequency': 100,

                # write control, specify when to output results, the options are listed below
                #   TIME_STEP:           write every 'write_frequency' time steps
                #   RUN_TIME:            write data every 'write_frequency' seconds of simulated time
                #   ADJUSTABLE_RUN_TIME: same as RUN_TIME, but may adjust time step for nice values
                #                        (use with 'CFLBasedTimeStepping' = True)
                #   CPU_TIME:            write data every 'write_frequency' seconds of CPU time
                #   CLOCK_TIME:          write data every 'write_frequency' seconds of real time
                'write_control': Parameters.TIME_STEP,

                # specify how many solutions to keep (specify 0 to keep all)
                'purge_write': 0,

                # under-relaxation to be used by all fields and equations
                'under_relaxation_default': 0.7,

                # field-specific under-relaxation factors dictionary (leave empty if none) the key needs to be the
                # variable name such as p, U, T, rho, etc. and the value its under-relaxation factor
                'under_relaxation_fields': {
                },

                # equation-specific under-relaxation factors dictionary (leave empty if none) the key needs to be the
                # variable name such as p, U, T, rho, etc. and the value its under-relaxation factor
                'under_relaxation_equations': {
                },
            },

            'numerical_discretisation': {
                # time integration scheme, options are listed below
                #   STEADY_STATE: Do not integrate in time, i.e. dU / dt = 0
                #   UNSTEADY:     Integrate in time and resolve  dU / dt
                'time_integration': Parameters.UNSTEADY,

                # Choose preset of numerical schemes based on accuracy and robustness requirements
                #   DEFAULT:    Optimal trade-off between accuracy and stability. Recommended for most cases. Tries to
                #               achieve second-order accuracy.
                #   TVD:        Same as DEFAULT, but use bounded Total Variation Diminishing (TVD) schemes instead of
                #               upwind schemes
                #   ROBUSTNESS: Use this option if your simulation does not converge or your mesh has bad mesh quality
                #               metrics. First-order accurate in space and time
                #   ACCURACY:   Recommended for accuracy and scale resolved simulations (LES, DES, SAS). May be used
                #               after running a simulation with DEFAULT or ROBUSTNESS to increase accuracy. Second-order
                #               accurate with less limiting compared to DEFAULT and TVD.
                'numerical_schemes_correction': Parameters.ACCURACY,

                # flag to indicate if first order discretisation should be used for turbulent quantities
                'use_first_order_for_turbulence': True,
            },

            'turbulence_properties': {
                # turbulence treatment type
                #   LAMINAR: Use this to run simulations without turbulence model (laminar or DNS)
                #   LES:     Use this for scale resolved simulations (LES, DES, SAS)
                #   RANS:    Use this for scale modelled / averaged simulations (RANS)
                'turbulence_type': Parameters.LES,

                # for RANS only, describe fidelity of wall modelling (i.e. usage of wall functions)
                #   LOW_RE  : first cell-height near wall is of order y+ <= 1
                #   HIGH_RE : first cell-height near wall is of order y+ >  30
                'wall_modelling': Parameters.LOW_RE,

                # select how to calculate turbulent quantities at inlet
                #   INTERNAL:    Internal flow assumes the turbulent length scale to be limited by the channel /
                #                wind tunnel height or diameter, expressed through the reference_length parameter.
                #                It is calculated as 0.07 * reference length
                #   EXTERNAL:    External flow assumes the turbulent length scale to be limited by the scales within the
                #                fully turbulent boundary layer and approximately equal to 40% of the boundary layer
                #                thickness
                #   RATIO:       Alternatively, the turbulent to laminar viscosity ratio may be prescribed
                #   RATIO_AUTO:  In absence of any turbulent quantities, we may instead base the approximation of the
                #                turbulent to laminar viscosity ratio entirely on the freestream turbulence intensity.
                #                Use this option if any of the above are not suitable
                'turbulent_quantities_at_inlet': Parameters.EXTERNAL,

                # turbulent to laminar viscosity ratio. Only used when turbulent_quantities_at_inlet is set to RATIO
                'turbulent_to_laminar_ratio': 10,

                # freestream turbulent intensity (between 0 - 1), used for RANS initial and boundary conditions
                'freestream_turbulent_intensity': 0.05,

                # RANS turbulence model (will be ignored if turbulence_type != RANS)
                #   Based on linear eddy viscosity:
                #     kEpsilon:        standard k-epsilon model
                #     realizableKE:    realizable version of the k-epsilon model
                #     RNGkEpsilon:     renormalised group version of the k-epsilon model
                #     LienLeschziner:  Lien-Leschziner k-epsilon model (incompressible only)
                #     LamBremhorstKE:  Lam-Bremhorst k-epsilon model
                #     LaunderSharmaKE: Launder-Sharma k-epsilon model
                #
                #     kOmega:          standard k-omega model
                #     kOmegaSST:       standard k-omega SST model
                #
                #     qZeta:           q-zeta model (incompressible only, no wall functions)
                #
                #     SpalartAllmaras: standard Spalart-Allmaras model
                #
                #   Transition modelling
                #     kOmegaSSTLM:     gamma-Re,theta,t k-omega SST correlation-based transition model
                #     kkLOmega:        k_laminar, k_turbulent, omega physics-based transition model
                #
                #   Scale-Adaptive modelling
                #     kOmegaSSTSAS:    Scale-adaptive version of the k-omega SST model
                #
                #   Based on non-linear eddy viscosity:
                #     LienCubicKE:     Lien's k-epsilon model (incompressible only)
                #     ShihQuadraticKE: Shih's k-epsilon model (incompressible only)
                #
                #   Based on Reynolds Stresses
                #     LRR:             Reynolds stress model of Launder, Reece and Rodi
                #     SSG:             Reynolds stress model of Speziale, Sarkar and Gatski
                'RANS_model': Parameters.kOmegaSST,

                # LES / DES model
                #   LES:
                #     Smagorinsky:          Large Eddy Simulation based on classical Smagorinsky approach (fixed C_s)
                #     kEqn:                 One equation eddy-viscosity model
                #                           Eddy viscosity SGS model using a modeled balance equation to simulate the
                #                           behaviour of k.
                #     dynamicKEqn:          Dynamic one equation eddy-viscosity model
                #                           Eddy viscosity SGS model using a modeled balance equation to simulate
                #                           the behaviour of k in which a dynamic procedure is applied to evaluate the
                #                           coefficients
                #     dynamicLagrangian:    Dynamic SGS model with Lagrangian averaging
                #     DeardorffDiffStress:  Differential SGS Stress Equation Model for incompressible and
                #                           compressible flows
                #     WALE:                 The Wall-adapting local eddy-viscosity (WALE) SGS model
                #
                #   DES:
                #     SpalartAllmarasDES:   Detached Eddy Simulation based on the Spalart-Allmaras model
                #     SpalartAllmarasDDES:  Delayed Detached Eddy Simulation based on the Spalart-llmaras model
                #     SpalartAllmarasIDDES: Improved Delayed Detached Eddy Simulation based on the Spalart-Allmaras
                #                           model
                #     kOmegaSSTDES:         Detached Eddy Simulation based on the k-omega SST model
                #     kOmegaSSTDDES:        Delayed Detached Eddy Simulation based on the k-omega SST model
                #     kOmegaSSTIDDES:       Improved Delayed Detached Eddy Simulation based on the k-omega SST model
                'LES_model': Parameters.kEqn,

                # filter for spatial LES filtering, used for dynamic subgrid-scale models
                #   SIMPLE_FILTER:      Simple top-hat filter used in dynamic LES models
                #   ANISOTROPIC_FILTER: Anisotropic filter
                #   LAPLACE_FILTER:     Laplace filter
                'LES_filter': Parameters.SIMPLE_FILTER,

                # model to calculate delta coefficient in LES / DES model
                #   smooth:                 Smoothed delta which takes a given simple geometric delta and applies
                #                           smoothing to it such that the ratio of deltas between two cells is no
                #                           larger than a specified amount, typically 1.15
                #   Prandtl:                Apply Prandtl mixing-length based damping function to the specified
                #                           geometric delta to improve near-wall behavior or LES models
                #   maxDeltaxyz:            Delta calculated by taking the maximum distance between the cell centre
                #                           and any face centre.  For a regular hex cell, the computed delta will
                #                           equate to half of the cell width; accordingly, the deltaCoeff model
                #                           coefficient should be set to 2 for this case
                #   cubeRootVol:            Simple cube-root of cell volume delta used in LES models
                #   maxDeltaxyzCubeRoot:    Maximum delta between maxDeltaxyz and cubeRootVolDelta
                #   vanDriest:              Simple cube-root of cell volume delta used in incompressible LES models
                #   IDDESDelta:             IDDESDelta used by the IDDES (improved low Re Spalart-Allmaras DES model)
                #                           The min and max delta are calculated using the face to face distance of
                #                           the cell
                'delta_model': Parameters.cubeRootVol,
            },

            'convergence_control': {
                # convergence criterion for residuals (used to judge if a simulation has converged to a steady state)
                'convergence_threshold': 0,

                # absolute convergence criterion for implicit solvers (used to judge if the current iteration has
                # converged)
                'absolute_convergence_criterion': 1e-14,

                # relative convergence criterion for implicit solvers (used to judge if the current iteration has
                # converged)
                'relative_convergence_criterion': 0.01,

                # check if an integral quantity has converged instead of just checking the residuals
                # recommended if such a integral quantity can be easily defined for the current simulation
                #   NONE:                 Don't write any force coefficient based stopping criterion
                #   C_D:                  Convergence criterion based on the drag force coefficient
                #   C_L:                  Convergence criterion based on the lift force coefficient
                #   C_S:                  Convergence criterion based on the side force coefficient
                #   C_M_YAW:              Convergence criterion based on the yaw momentum coefficient
                #   C_M_ROLL:             Convergence criterion based on the roll momentum coefficient
                #   C_M_PITCH:            Convergence criterion based on the pitch momentum coefficient
                'integral_convergence_criterion': [Parameters.NONE],

                # if integral quantities are checked for convergence, specify for how many timesteps their average
                # should be calculated to check if, on average, the quantity has converged
                'averaging_time_steps': 20,

                # specify the convergence threshold for the integral quantities
                'integral_quantities_convergence_threshold': 1e-5,

                # specify how many iterations to wait before checking convergence criterion
                'time_steps_to_wait_before_checking_convergence': 100,
            },

            'dimensionless_coefficients': {
                # reference length (used for RANS initial and boundary conditions)
                'reference_length': 1.0,

                # reference area (used to non-dimensionalise force coefficients)
                'reference_area': 1.0,

                # center of rotation for momentum coefficient
                'center_of_rotation': [0.25, 0, 0],

                # group of wall boundaries, which should be used to calculate force coefficients on (enter as list)
                'wall_boundaries': [''],

                # write force coefficients to file
                'write_force_coefficients': False,

                # write pressure coefficient (cp) to file
                'write_pressure_coefficient': False,

                # write wall shear stresses (can be used to obtain skin friction coefficient) to file
                'write_wall_shear_stresses': False,
            },

            # write out additional fields of interest
            'additional_fields': {
                # flag indicating if additional fields should be active (written to file). Will be written with all
                # other variables to file at the same time. If set to false, ignore the rest of this dictionary.
                'write_additional_fields': True,

                # list of additional fields to write, can be more than 1 (Mach number will be automatically written for
                # compressible flow cases)
                #   Q:         Write out the Q-criterion, useful for isoSurfaces to visualise turbulence structures
                #   VORTICITY: Write out vorticity field
                #   LAMBDA_2:  Write out the Lambda-2 criterion, useful for vortex core detection
                #   ENSTROPHY: Write out enstrophy field
                'fields': [Parameters.Q, Parameters.VORTICITY],
            },

            # specify 0-D point probes to which will output flow variables at each timestep at a given location x,
            # y and z
            'point_probes': {
                # flag indicating if point probes should be active (written to file). If set to false, ignore the
                # rest of this dictionary.
                'write_point_probes': False,

                # specify the location at which to output information, can be more than 1
                'location': [
                    [1, 0.01, 0],
                    [2, 0, 0],
                ],

                # specify variables that should be monitored at the specified point
                'variables_to_monitor': ['U', 'p'],

                # if flag is set to true, solution will be written at every time step. Otherwise, the probe will only
                # be written according to the settings in the controlDict (i.e. every time a new time directory is
                # generated)
                'output_probe_at_every_timestep': True,
            },

            # specify 1-D line probes
            'line_probes': {
                # flag indicating if point probes should be active (written to file). If set to false, ignore the
                # rest of this dictionary.
                'write_line_probes': False,

                # specify the start and end point where line should be placed, can be more than 1
                'location': [
                    {
                        'name': 'x=2',
                        'start': [2, 1, 0.5],
                        'end': [2, -1, 0.5],
                    },
                    {
                        'name': 'x=5',
                        'start': [5, 1, 0.5],
                        'end': [5, -1, 0.5],
                    },
                ],

                # number of points along line
                'number_of_samples_on_line': 100,

                # specify variables that should be monitored along line
                'variables_to_monitor': ['U', 'p'],

                # if flag is set to true, solution will be written at every time step. Otherwise, the probe will only
                # be written according to the settings in the controlDict (i.e. every time a new time directory is
                # generated)
                'output_probe_at_every_timestep': False,
            },

            # specify 2-D cutting planes
            'cutting_planes': {
                # flag indicating if point probes should be active (written to file). If set to false, ignore the
                # rest of this dictionary.
                'write_cutting_planes': True,

                # specify the origin and normal vector of cutting plane, can be more than 1
                'location': [
                    {
                        'name': 'plane_x=0',
                        'origin': [0, 0, 0],
                        'normal': [1, 0, 0],
                    },
                    {
                        'name': 'plane_y=0',
                        'origin': [0, 0, 0],
                        'normal': [0, 1, 0],
                    },
                    {
                        'name': 'plane_z=0',
                        'origin': [0, 0, 0],
                        'normal': [0, 0, 1],
                    },
                ],

                # specify variables that should be monitored along line
                'variables_to_monitor': ['U', 'p', 'vorticity'],

                # if flag is set to true, solution will be written at every time step. Otherwise, the cutting plane will
                # only be written according to the settings in the controlDict (i.e. every time a new time directory is
                # generated)
                'output_cutting_plane_at_every_timestep': False,
            },

            # write iso surfaces of variables during calculation
            'iso_surfaces': {
                # flag indicating if iso-surfaces should be active (written to file). If set to false, ignore the
                # rest of this dictionary.
                'write_iso_surfaces': True,

                # variables of which to write iso surfaces
                'flow_variable': ['Q'],

                # iso value at which point the surface should be written. List entry correspond to order specified in
                # flow_variable list
                'iso_value': [0.1],

                # additional fields to write (can be more than 1, can be used to colour iso-surface in post-processing)
                'additional_field_to_write': ['p'],

                # if flag is set to true, iso-surfaces will be written at every time step. Otherwise,
                # the iso surfaces will only be written according to the settings in the controlDict (i.e. every time
                # a new time directory is generated)
                'output_iso_surfaces_at_every_timestep': False,
            },

            # user-defined function objects that will get executed after all other function objects have run
            'post_processing': {
                # execute user-defined function object?
                'execute_function_object': True,

                # path to user-defined function object as a key value pair (dictionary). The key is used as the name of
                # the file and the value is the path to the function object that should be executed
                'function_objects': {
                    'integratedKineticEnergy': os.path.join('examples', 'scripts', 'userDefined', 'functionObjects',
                                                            'taylorGreenVortex')
                },

                # execute user-defined post processing routines?
                'execute_python_scrip': True,

                # list of user defined python scripts to copy and execute after the simulation is done
                # each list entry contains a dictionary with 2 key-value pairs. The first key is named "script" and
                # needs to point to the location of the python script. The second is the "requires" key which is a list
                # of files requires by the script, for example, reference solution data that is read by the script
                'python_script': [
                    {
                        'script': os.path.join('examples', 'scripts', 'userDefined', 'postProcessing',
                                               'taylorGreenVortex', 'plotTaylorGreenVortex.py'),
                        'requires': [
                            os.path.join('examples', 'scripts', 'userDefined', 'postProcessing',
                                         'taylorGreenVortex', 'taylor_green_vortex_512_ref.dat'),
                        ],
                    },
                ],
            },
        }

    def get_case_properties(self, command_line_arguments):
        self.__add_default_properties()
        self.properties = self.__handle_command_line_arguments(command_line_arguments, self.properties)
        return self.properties

    def __handle_command_line_arguments(self, command_line_arguments, properties):
        # process properties dictionary (read and write if necessary)
        if command_line_arguments.option_exists('input'):
            with open(command_line_arguments['input'], 'r') as json_file:
                properties = json.load(json_file)
        elif command_line_arguments.option_exists('output'):
            with open(command_line_arguments['output'], 'w') as json_file:
                json.dump(self.properties, json_file, indent=4)
        elif command_line_arguments.option_exists('write-json-only'):
            with open(command_line_arguments['write-json-only'], 'w') as json_file:
                json.dump(self.properties, json_file, indent=4)
            exit(0)
        return properties

    def __add_default_properties(self):
        # absolute path of text case location
        self.properties['file_properties']['path'] = os.path.join(self.properties['file_properties']['run_directory'],
                                                                  self.properties['file_properties']['case_name'])

        # check how quantities are specified and calculate the missing properties
        if self.properties['flow_properties']['input_parameters_specification_mode'] == Parameters.NON_DIMENSIONAL:
            if self.properties['flow_properties']['flow_type'] == Parameters.incompressible:
                self.__calculate_dimensional_properties_from_Re_incompressible()
            elif self.properties['flow_properties']['flow_type'] == Parameters.compressible:
                self.__calculate_dimensional_properties_from_Ma_compressible()
        if self.properties['flow_properties']['input_parameters_specification_mode'] == Parameters.DIMENSIONAL:
            self.__calculate_Re_incompressible_from_dimensional_properties()
            if self.properties['flow_properties']['flow_type'] == Parameters.compressible:
                self.__calculate_Ma_compressible_from_dimensional_properties()

        self.__add_dynamic_viscosity()
        self.__create_inlet_velocity_vector_from_velocity_magnitude_and_direction()
        self.__set_correct_gradient_reconstruction_scheme_for_RANS()

    def __calculate_dimensional_properties_from_Re_incompressible(self):
        Re = self.properties['flow_properties']['non_dimensional_properties']['Re']
        order_of_magnitude = floor(log10(Re))
        nu = 1.0 / pow(10, order_of_magnitude)
        u_mag = Re / pow(10, order_of_magnitude)

        self.properties['flow_properties']['dimensional_properties']['nu'] = nu
        self.properties['flow_properties']['dimensional_properties']['rho'] = 1.0
        self.properties['flow_properties']['dimensional_properties']['p'] = 0
        self.properties['flow_properties']['dimensional_properties']['velocity_magnitude'] = u_mag

    def __calculate_dimensional_properties_from_Ma_compressible(self):
        T = 298
        Ma = self.properties['flow_properties']['non_dimensional_properties']['Ma']
        c = sqrt(1.4 * 287 * T)
        self.properties['flow_properties']['non_dimensional_properties']['speed_of_sound'] = c
        u_mag = Ma * c
        Re = self.properties['flow_properties']['non_dimensional_properties']['Re']
        l_ref = self.properties['dimensionless_coefficients']['reference_length']
        nu = u_mag * l_ref / Re

        self.properties['flow_properties']['dimensional_properties']['nu'] = nu
        self.properties['flow_properties']['dimensional_properties']['rho'] = 1.225
        self.properties['flow_properties']['dimensional_properties']['T'] = T
        self.properties['flow_properties']['dimensional_properties']['p'] = 1e5
        self.properties['flow_properties']['dimensional_properties']['velocity_magnitude'] = u_mag

    def __calculate_Re_incompressible_from_dimensional_properties(self):
        # calculate reynolds number
        u_mag = self.properties['flow_properties']['dimensional_properties']['velocity_magnitude']
        nu = self.properties['flow_properties']['dimensional_properties']['nu']
        l_ref = self.properties['dimensionless_coefficients']['reference_length']
        self.properties['flow_properties']['non_dimensional_properties']['Re'] = u_mag * l_ref / nu

    def __calculate_Ma_compressible_from_dimensional_properties(self):
        u_mag = self.properties['flow_properties']['dimensional_properties']['velocity_magnitude']
        T = self.properties['flow_properties']['dimensional_properties']['T']
        c = sqrt(1.4 * 287 * T)
        self.properties['flow_properties']['non_dimensional_properties']['speed_of_sound'] = c
        self.properties['flow_properties']['non_dimensional_properties']['Ma'] = u_mag / c

    def __add_dynamic_viscosity(self):
        nu = self.properties['flow_properties']['dimensional_properties']['nu']
        rho = self.properties['flow_properties']['dimensional_properties']['rho']
        self.properties['flow_properties']['dimensional_properties']['mu'] = nu * rho

    def __create_inlet_velocity_vector_from_velocity_magnitude_and_direction(self):
        velocity_vector = [0, 0, 0]
        RAD_TO_DEG = pi / 180

        tangential = self.properties['flow_properties']['axis_aligned_flow_direction']['tangential']
        normal = self.properties['flow_properties']['axis_aligned_flow_direction']['normal']
        aoa = self.properties['flow_properties']['axis_aligned_flow_direction']['angle_of_attack']
        u_mag = self.properties['flow_properties']['dimensional_properties']['velocity_magnitude']

        velocity_vector[tangential] = cos(aoa * RAD_TO_DEG) * u_mag
        velocity_vector[normal] = sin(aoa * RAD_TO_DEG) * u_mag

        self.properties['flow_properties']['dimensional_properties']['velocity_vector'] = velocity_vector

    def __set_correct_gradient_reconstruction_scheme_for_RANS(self):
        self.properties['turbulence_properties']['use_phi_instead_of_grad_U'] = False,
        if (self.properties['turbulence_properties']['RANS_model'] == Parameters.LienCubicKE or
                self.properties['turbulence_properties']['RANS_model'] == Parameters.ShihQuadraticKE or
                self.properties['turbulence_properties']['RANS_model'] == Parameters.LRR or
                self.properties['turbulence_properties']['RANS_model'] == Parameters.SSG):
            self.properties['turbulence_properties']['use_phi_instead_of_grad_U'] = True
