|travis| |lgtm| |coveralls| |libraries|

.. |travis| image:: https://img.shields.io/badge/python%20-%2314354C.svg?&style=flat&logo=python&logoColor=white
  :target: https://travis-ci.org/cdown/srt
  :alt: Tests

.. |lgtm| image::  https://img.shields.io/badge/plotly%20-%233B4D98.svg?&style=flat&logo=plotly&logoColor=white
  :target: https://lgtm.com/projects/g/cdown/srt/overview/
  :alt: LGTM

.. |coveralls| image:: https://img.shields.io/badge/numpy%20-%230095D5.svg?&style=flat&logo=numpy&logoColor=white
  :target: https://coveralls.io/github/cdown/srt?branch=develop
  :alt: Coverage

.. |libraries| image:: https://img.shields.io/badge/SymPy%20-%23239120.svg?&style=flat&logo=sympy&logoColor=white
  :target: https://libraries.io/github/cdown/srt
  :alt: Dependencies

Descripción general
-------------------

Este módulo contiene algunas herramientas para la representación gráfica de vectores en el plano y en 
el espacio, diseñado para un curso de álgebra lineal con aplicaciones, contiene funciones para graficar
vectores con punto inicial y punto final dado, o anclados en el origen, para su realización se utilizó 
la librería de graficación interactiva **Plotly** y la librería de arreglos multidimensionales **NumPy**,
es compatible con vectores construidos como matriz columna en la librería **SymPy**. Puede servir como 
herramienta de visualización, para validar el conocimiento por parte de los estudiantes y para la 
resolución de problemas relacionados con conceptos vectoriales.

Instalación
-----------

Para utilizar el módulo de graficación **plotvectors** debe importarlo de la siguiente manera:

.. code::

    pip install PlotLinearAlgebra

.. code::

    from PlotLinearAlgebra.plotvectors import *