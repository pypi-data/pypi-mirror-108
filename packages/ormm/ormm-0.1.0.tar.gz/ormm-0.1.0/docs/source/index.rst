.. ORMM documentation master file, created by
   sphinx-quickstart on Wed Jul 29 11:10:51 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

User Guide
================================
Operations Research Models & Methods (ORMM) is inspired by Paul A. Jensen's Excel Add-ins.
His Excel packages were last updated in 2011, and while I believe they do still work
(for the most part), his work may become outdated in a couple of ways:

- Excel is not as commonly used for OR, except in settings where security is of the
  utmost concern and/or modern languages like Python, R, Julia, C, C++, MATLAB, AMPL,
  or other modeling software are not available.
- From what I understand, Microsoft has been trying to phase out VBA and move to Javascript.
  If this happens, this could significantly impact whether or not his packages will work.
- His website and packages used to be available
  `here <https://www.me.utexas.edu/~jensen/ORMM/>`_, but currently I at least have not
  been able to load this webpage anymore - I'm not sure if UTexas took it down or not.

This python package aims to accomplish some of the same goals as Paul Jensen's website and
add-ins did, mainly to

1. Be an educational tool that shows how abstract models (linear programs, integer programs,
   nonlinear programs, etc.) can be applied to real-life scenarios to solve complex problems.
2. Help the practitioner by providing modeling frameworks, methods for solving these models,
   and problem classes so a user can more easily see how they may be able to frame
   their business problem/objective through the lens of Operations Research.

This repository contains subpackages for grouping the different types of OR Models & Methods.
Currently this subpackage list includes

1. :py:obj:`mathprog`: A subpackage for mathematical programs, including linear programs, mixed
   integer linear programs, nonlinear programs, and stochastic programs.  Note for this
   subpackage that models and methods are not necessarily implemented in their abstract
   form, like Paul Jensen did - there are many python libraries that accomplish this task
   far better than I could (Pyomo, PuLP, GLPK to name a few).  Thus, this subpackage here
   is dedicated to providing many problem classes, which show how these can be applied
   to real-life problems and provide an abstract/concrete model for that particular
   class of problems.  Note that the abstract models can be built upon based on a
   unique business problem that may have more or fewer constraints, or a more complex
   objective to maximize/minimize.
2. `markov`: A subpackage for discrete state markov analysis.  Currently this only
   has implementations for discrete time markov processes, but continous time will
   be added in the near future.  This includes the main function `markov_analysis`,
   which returns a dictionary of the results, as well as a `print_markov` function.
   The main method requires a transition matrix, but can then run simulations,
   analyze steady state and transient probabilities, and run cost analyses if
   additional arguments are passed.

Installation
------------
.. code:: console

   $ pip install ormm

Examples
--------
The :py:obj:`mathprog` subpackage has multiple problem classes, as well as functions for
printing the solution of a solved concrete model and for returning a pandas dataframe
containing information for sensitivity analysis. Following are some examples of a
few of these problem classes.

1. Resource Allocation: Optimize using scarce resources for valued activities.

.. code:: python

   from ormm.mathprog import resource_allocation
   model = resource_allocation()

2. Blending Problem: Optimize the mixing of ingredients to satisfy requirements
   while minimizing cost.

.. code:: python

   from ormm.mathprog import blending
   model = blending()

3. Employee Scheduling: Minimize the number of workers hired while meeting
   the minimum number of workers required for each period.

.. code:: python

   from ormm.mathprog import scheduling
   model = scheduling(prob_class="employee")

4. Rental Scheduling:  Minimize the cost of the plans purchased (which rent
   units for different amounts of time) while satisfying the number of units
   needed for each period.

.. code:: python

   from ormm.mathprog import scheduling
   model = scheduling(prob_class="rental")

For more details on optional parameters and usage, see the :ref:`api_reference`.
For more details on the MathProg problem descriptions, see the :ref:`math_prog`.

Developer Environment
---------------------

To use the same packages used in development (for creating additions / modifications),
you may use the bash command below to install the dev requirements \
(recommended to do this in your virtualenv).  This includes being able to run tests
and add to the documentation.

.. code:: console

   $ pip install -e .[dev]

.. toctree::
   :maxdepth: 2

   mathprog/index

.. toctree::
   :maxdepth: 2

   markov/index

.. toctree::
   :maxdepth: 2

   network/index

.. toctree::
   :maxdepth: 2

   api/index
.. Indices and tables
  ==================
  * :ref:`genindex`
  * :ref:`modindex`
  * :ref:`search`
