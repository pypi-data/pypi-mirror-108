##################
tox-recreate-hook
##################

.. start short_desc

**(experimental) Allows hooks to be defined which are called when recreating a tox testenv.**

.. end short_desc


.. start shields

.. list-table::
	:stub-columns: 1
	:widths: 10 90

	* - Docs
	  - |docs| |docs_check|
	* - Tests
	  - |actions_linux| |actions_windows| |actions_macos| |coveralls|
	* - PyPI
	  - |pypi-version| |supported-versions| |supported-implementations| |wheel|
	* - Activity
	  - |commits-latest| |commits-since| |maintained| |pypi-downloads|
	* - QA
	  - |codefactor| |actions_flake8| |actions_mypy|
	* - Other
	  - |license| |language| |requires|

.. |docs| image:: https://img.shields.io/readthedocs/tox-recreate-hook/latest?logo=read-the-docs
	:target: https://tox-recreate-hook.readthedocs.io/en/latest
	:alt: Documentation Build Status

.. |docs_check| image:: https://github.com/python-coincidence/tox-recreate-hook/workflows/Docs%20Check/badge.svg
	:target: https://github.com/python-coincidence/tox-recreate-hook/actions?query=workflow%3A%22Docs+Check%22
	:alt: Docs Check Status

.. |actions_linux| image:: https://github.com/python-coincidence/tox-recreate-hook/workflows/Linux/badge.svg
	:target: https://github.com/python-coincidence/tox-recreate-hook/actions?query=workflow%3A%22Linux%22
	:alt: Linux Test Status

.. |actions_windows| image:: https://github.com/python-coincidence/tox-recreate-hook/workflows/Windows/badge.svg
	:target: https://github.com/python-coincidence/tox-recreate-hook/actions?query=workflow%3A%22Windows%22
	:alt: Windows Test Status

.. |actions_macos| image:: https://github.com/python-coincidence/tox-recreate-hook/workflows/macOS/badge.svg
	:target: https://github.com/python-coincidence/tox-recreate-hook/actions?query=workflow%3A%22macOS%22
	:alt: macOS Test Status

.. |actions_flake8| image:: https://github.com/python-coincidence/tox-recreate-hook/workflows/Flake8/badge.svg
	:target: https://github.com/python-coincidence/tox-recreate-hook/actions?query=workflow%3A%22Flake8%22
	:alt: Flake8 Status

.. |actions_mypy| image:: https://github.com/python-coincidence/tox-recreate-hook/workflows/mypy/badge.svg
	:target: https://github.com/python-coincidence/tox-recreate-hook/actions?query=workflow%3A%22mypy%22
	:alt: mypy status

.. |requires| image:: https://requires.io/github/python-coincidence/tox-recreate-hook/requirements.svg?branch=master
	:target: https://requires.io/github/python-coincidence/tox-recreate-hook/requirements/?branch=master
	:alt: Requirements Status

.. |coveralls| image:: https://img.shields.io/coveralls/github/python-coincidence/tox-recreate-hook/master?logo=coveralls
	:target: https://coveralls.io/github/python-coincidence/tox-recreate-hook?branch=master
	:alt: Coverage

.. |codefactor| image:: https://img.shields.io/codefactor/grade/github/python-coincidence/tox-recreate-hook?logo=codefactor
	:target: https://www.codefactor.io/repository/github/python-coincidence/tox-recreate-hook
	:alt: CodeFactor Grade

.. |pypi-version| image:: https://img.shields.io/pypi/v/tox-recreate-hook
	:target: https://pypi.org/project/tox-recreate-hook/
	:alt: PyPI - Package Version

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/tox-recreate-hook?logo=python&logoColor=white
	:target: https://pypi.org/project/tox-recreate-hook/
	:alt: PyPI - Supported Python Versions

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/tox-recreate-hook
	:target: https://pypi.org/project/tox-recreate-hook/
	:alt: PyPI - Supported Implementations

.. |wheel| image:: https://img.shields.io/pypi/wheel/tox-recreate-hook
	:target: https://pypi.org/project/tox-recreate-hook/
	:alt: PyPI - Wheel

.. |license| image:: https://img.shields.io/github/license/python-coincidence/tox-recreate-hook
	:target: https://github.com/python-coincidence/tox-recreate-hook/blob/master/LICENSE
	:alt: License

.. |language| image:: https://img.shields.io/github/languages/top/python-coincidence/tox-recreate-hook
	:alt: GitHub top language

.. |commits-since| image:: https://img.shields.io/github/commits-since/python-coincidence/tox-recreate-hook/v0.1.1
	:target: https://github.com/python-coincidence/tox-recreate-hook/pulse
	:alt: GitHub commits since tagged version

.. |commits-latest| image:: https://img.shields.io/github/last-commit/python-coincidence/tox-recreate-hook
	:target: https://github.com/python-coincidence/tox-recreate-hook/commit/master
	:alt: GitHub last commit

.. |maintained| image:: https://img.shields.io/maintenance/yes/2021
	:alt: Maintenance

.. |pypi-downloads| image:: https://img.shields.io/pypi/dm/tox-recreate-hook
	:target: https://pypi.org/project/tox-recreate-hook/
	:alt: PyPI - Downloads

.. end shields

Installation
--------------

.. start installation

``tox-recreate-hook`` can be installed from PyPI.

To install with ``pip``:

.. code-block:: bash

	$ python -m pip install tox-recreate-hook

.. end installation


Example configuration

.. code-block:: ini

	[testenv:docs]
	setenv = SHOW_TODOS = 1
	basepython = python3.8
	changedir = {toxinidir}/doc-source
	deps =
	    -r{toxinidir}/requirements.txt
	    -r{toxinidir}/doc-source/requirements.txt
	commands = sphinx-build -M html . ./build {posargs}
	recreate_hook = builtin.rmdir("{toxinidir}/doc-source/build")
