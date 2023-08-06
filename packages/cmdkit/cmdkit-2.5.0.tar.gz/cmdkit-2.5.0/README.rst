CmdKit
======

A library for developing command-line applications in Python.

.. image:: https://img.shields.io/badge/license-Apache-blue.svg?style=flat
    :target: https://www.apache.org/licenses/LICENSE-2.0
    :alt: License

.. image:: https://img.shields.io/pypi/v/cmdkit.svg?style=flat&color=blue
    :target: https://pypi.org/project/cmdkit
    :alt: PyPI Version

.. image:: https://img.shields.io/pypi/pyversions/cmdkit.svg?logo=python&logoColor=white&style=flat
    :target: https://pypi.org/project/cmdkit
    :alt: Python Versions

.. image:: https://readthedocs.org/projects/cmdkit/badge/?version=latest&style=flat
    :target: https://cmdkit.readthedocs.io
    :alt: Documentation

.. image:: https://pepy.tech/badge/cmdkit
    :target: https://pepy.tech/badge/cmdkit
    :alt: Downloads

|

The *cmdkit* library implements a few common patterns needed by well-formed command-line
applications in Python. It only touches a few concepts but it implements them well.
The idea is to reduce the boilerplate needed to get a full featured CLI off the ground.
Applications developed using *cmdkit* are easy to implement, easy to maintain, and easy to
understand.

|

Features
--------

An `Application <https://cmdkit.readthedocs.io/en/latest/api/app.html#cmdkit.app.Application>`_
class provides the boilerplate for a good entry-point.
Building your command-line application in layers with
`ApplicationGroup <https://cmdkit.readthedocs.io/en/latest/api/app.html#cmdkit.app.ApplicationGroup>`_
let's you develop simple structures and modules that mirror your CLI.

An `Interface <https://cmdkit.readthedocs.io/en/latest/api/cli.html#cmdkit.cli.Interface>`_ class
modifies the behavior of the standard ``argparse.ArgumentParser`` class to raise simple exceptions
instead of exiting.

.. code-block:: python

    class Add(Application):
        """Application class for adding routine."""

        interface = Interface('add', USAGE_TEXT, HELP_TEXT)
        interface.add_argument('-v', '--version', action='version', '0.0.1')

        lhs: int
        rhs: int
        interface.add_argument('lhs', type=float)
        interface.add_argument('rhs', type=float)

        def run(self) -> None:
            """Business logic of the application."""
            print(self.lhs + self.rhs)

|

A
`Configuration <https://cmdkit.readthedocs.io/en/latest/api/config.html#cmdkit.config.Configuration>`_
class makes it basically a one-liner to pull in
a configuration with a dictionary-like interface from a cascade of files as well as
expanding environment variables into a hierarchy and merged.

The standard behavior for any `good` application is for a configuration to allow for
system-level, user-level, and local configuration to overlap. Merging these should not
clobber the same section in a lower-priority source. The
`Namespace <https://cmdkit.readthedocs.io/en/latest/api/config.html#cmdkit.config.Namespace>`_
class extends the behavior of a standard Python `dict` to have a depth-first merge for its
`update` implementation.

.. code-block:: python

    config = Configuration.from_local(env=True, prefix='MYAPP', default=default, **paths)

The underlying
`Namespace <https://cmdkit.readthedocs.io/en/latest/api/config.html#cmdkit.config.Namespace>`_
also supports the convention of having
parameters with ``_env`` and ``_eval`` automatically expanded.

.. code-block:: toml

    [database]
    password_eval = "gpg ..."

Accessing the parameter with dot-notation, i.e., ``config.database.password`` would execute
``"gpg ..."`` as a shell command and return the output.

|

Installation
------------

*CmdKit* is tested on Python 3.7+ for `Windows`, `macOS`, and `Linux`, and can be installed
from the `Python Package Index` using `Pip`.

::

    $ pip install cmdkit

|

Getting Started
---------------

Checkout the `Tutorial <https://cmdkit.readthedocs.io/en/latest/tutorial/>`_ for examples.

You can also checkout how `CmdKit` is being used by other projects, e.g.,
`REFITT <https://github.com/refitt/refitt>`_ and `HyperShell <https://github.com/glentner/hyper-shell>`_.

|

Documentation
-------------

Documentation for getting started, the API, and common recipes are available at
`cmdkit.readthedocs.io <https://cmdkit.readthedocs.io>`_.

|

Contributions
-------------

Contributions are welcome in the form of suggestions for additional features, pull requests with
new features or bug fixes, etc. If you find bugs or have questions, open an *Issue* here. If and
when the project grows, a code of conduct will be provided along side a more comprehensive set of
guidelines for contributing; until then, just be nice.
