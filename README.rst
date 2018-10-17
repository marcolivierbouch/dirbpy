Dirbpy
--------

.. image:: https://img.shields.io/pypi/v/dirbpy.svg
    :target: https://pypi.org/project/dirbpy/
.. image:: https://img.shields.io/pypi/pyversions/dirbpy.svg
    :target: https://pypi.org/project/dirbpy/
.. image:: https://travis-ci.org/marcolivierbouch/dirbpy.svg?branch=master
    :target: https://travis-ci.org/marcolivierbouch/dirbpy
.. image:: https://codecov.io/gh/marcolivierbouch/dirbpy/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/marcolivierbouch/dirbpy

Description
-----------
Dirbpy - URL Bruteforcer

This is a new version of dirb but in python. This version is faster than the normal version in C because it uses thread. Dirbpy is a Web Content Scanner. It looks for hidden Web Objects. It basically works by launching a dictionary based attack against a web server and analizing the response.

Link to the real dirb: https://github.com/v0re/dirb

Install with pip
----------------
``pip install dirbpy``

Fish completions
----------------
``git clone https://github.com/marcolivierbouch/dirbpy.git``

``cd dirbpy``

``sudo cp dirbpy.fish /usr/share/fish/completions``

Dirbpy with Docker
------------------
Build the Docker

``docker build -t dirbpy .``

After you need to get inside the docker

``docker run -it dirbpy /bin/sh``

Command example

``./dirbpy -f /opt/Seclist/Discovery/Web-Content/common.txt -u https://[....].com``

Recommendations
---------------
I recommend using the SecLists: https://github.com/danielmiessler/SecLists
