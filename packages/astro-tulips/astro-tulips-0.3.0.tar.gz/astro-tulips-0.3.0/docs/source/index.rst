.. image:: ../../tulips/logo/Tulips_acronym_text_transparent.png

Important notice
================
This is an alpha version and is not meant for use by external parties.

Documentation
=============

Welcome to the ``tulips`` documentation! The ``tulips`` python package creates visualizations of stars
based on output from the `MESA <http://mesa.sourceforge.net/>`_ stellar evolution code. TULIPS represents stars as
circles with varying size and color. Click the links below to learn more about TULIPS through examples,
tutorials, and detailed documentation.


.. image:: figures/first_animation.gif
    :align: center

.. toctree::
    :maxdepth: 1
    :caption: Contents
    :hidden:

    installation
    getting_started
    The TULIPS repository <https://bitbucket.org/elaplace/tulips/src/master/>
    api

.. toctree::
    :maxdepth: 1
    :caption: Tulips diagrams
    :hidden:

    perceived_color_diagram
    energy_and_mixing_diagram
    property_profile_diagram
    chemical_profile_diagram

.. toctree::
    :maxdepth: 1
    :caption: Additional options
    :hidden:

    timestep_options
    customize

.. raw:: html

    <div class="nav-container" style="margin-bottom:30px;">
        <div class="box" data-href="installation.html">Installation</div>
        <div class="box" data-href="getting_started.html">Getting Started</div>
    </div>

Tulips diagrams
===============

.. raw:: html

    <div class="nav-container" style="margin-bottom:30px;">
        <div class="box" href="perceived_color_diagram.html">Perceived color diagram</div>
        <div class="box" data-href="energy_and_mixing_diagram.html">Energy and mixing diagram</div>
    </div>

    <div class="nav-container" style="margin-bottom:30px;">
        <div class="box" data-href="property_profile_diagram.html">Property profile diagram</div>
        <div class="box" data-href="chemical_profile_diagram.html">Chemical profile diagram</div>
    </div>

Additional options
==================

.. raw:: html

    <div class="nav-container">
        <div class="box" data-href="timestep_options.html">Timestep options</div>
        <div class="box" data-href="customize.html">Customize options</div>
    </div>

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Contributing
============
If you wish to submit a new feature or bug fix please send a pull request.

Acknowledgments
===============
tulips makes use of the open-source python modules mesaPlot by Rob Farmer, colorpy by Mark Kness, numpy, and matplotlib.
Logo design: A. Faber. Documentation: I. de Langen
