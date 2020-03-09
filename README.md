# pyGLLE

Python toolkit for simulating the propagation dynamics of dissipative solitons
in a variant of the Lugiato-Lefever equation (LLE) described in the manuscript 

"pyGLLE: A Python toolkit for solving the generalized Lugiato-Lefever equation"

O. Melchert (1,2), and A. Demircan (1,2)

1. Institute of Quantum Optics, Leibnitz Universität Hannover, Welfengarten 1, 30167 Hannover, Germany
2. Cluster of Excellence PhoenixD, Welfengarten 1, 30167, Hannover, Germany

This repository contains code and data analysis scripts for reproducing the
simulated data and replication of draft versions of Figures 1 and 2 of the
manuscript. 

The provided software implements a solver for a variant of the LLE including
dispersion terms of third and fourth order. It also includes the functionality
to solve for stationary solutions of the standard LLE, containing one or
several localized dissipative structures.

### Prerequisites

The tools provided by the `pyGLLE` package require the functionality of 

* numpy (>=1.8.0rc1)
* scipy (>=0.13.0b1)

Further, the figure generation scripts included with the examples require the
funcality of

* matplotlib (>=1.2.1)

## Included materials

The repository follows a modular structure:

```
pyGLLE/
├── LICENSE.md
├── README.md
├── numExp01_stationarySolution
│   ├── data_stationary_solution
│   ├── main_findStationarySolution.py
│   ├── pp_figure
│   │   ├── FIGS
│   │   ├── generateFigure.sh
│   │   └── main_figure_stationarySolution.py
│   └── run.sh
├── numExp02_propagationScenarios
│   ├── data
│   ├── data_stationary_solution
│   ├── main_findStationarySolution.py
│   ├── main_propagateInitialCondition.py
│   ├── pp_figure_propagationScenarios
│   │   ├── FIGS
│   │   ├── figure_base_propagationDynamics.py
│   │   ├── generateFigures.sh
│   │   └── main_figure_propagationDynamics_stationarySolution.py
│   └── run.sh
├── scripts
│   └── pyGLLE.py
└── src
    ├── data_handler.py
    ├── solver.py
    └── stationary_solution.py
```

Subfolder `/src` contains Python modules implementing the basic functionality of the software:
* `data_handler.py`: provides a class, handling data accumulation and data
* ouput. Output data is stored using the numpy native npz-format.
* `stationary_solution.py`:
    provides functions allowing to obtain stationary localized solution of the standard LLE.
* `solver.py`: implements a solver for the numerical integration of the generalized LLE using a Runge-Kutta method.

The folder `/scripts` contains the main Python module implementing the
interface between the user supplied code and the algorithms and data structures
contained in the modules in folder `\src`:
* `pyGLLE.py`: defines the main functions `findStationarySolution` and
    `propagateInitialCondition`.

Further, the folders `\numExp01_stationarySolution` and
`numExp02_propagationScenarios` contain scripts that implement example
workflows ranging from the specification of a propagation scenario to the
visualization of the generated raw data.

The repository further contains
* `LICENSE`, a license file.
* `Readme.md`, this file.

For a more detailed description of functions, defined in the above modules,
their parameters and return values we refer to the example cases and
documentation provided within the code.

## Links

The presented software has been extensively used in our research work,
including the study of resonant emission of multi-frequency radiation by
oscillating dissipative solitons in the LLE including third order dispersion

> O. Melchert, A. Demircan, A. Yulin, "Multi-frequency radiation of dissipative solitons in optical fiber cavities," submitted (2020) 

and the dynamics of LDSs in the GLLE with negative quartic group-velocity dispersion 

> O. Melchert, A. Yulin, A. Demircan, "Dynamics of localized dissipative structures in a generalized Lugiato-Lefever model with negative quartic group-velocity dispersion," submitted (2020) 

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

This work received funding from the Deutsche Forschungsgemeinschaft  (DFG) under
Germany’s Excellence Strategy within the Cluster of Excellence PhoenixD
(Photonics, Optics, and Engineering – Innovation Across Disciplines) (EXC 2122,
projectID 390833453).
