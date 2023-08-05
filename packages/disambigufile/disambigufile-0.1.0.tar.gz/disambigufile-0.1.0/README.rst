=============
disambigufile
=============


.. image:: https://img.shields.io/pypi/v/disambigufile.svg
        :target: https://pypi.python.org/pypi/disambigufile

.. image:: https://img.shields.io/travis/datagazing/disambigufile.svg
        :target: https://travis-ci.com/datagazing/disambigufile

.. image:: https://readthedocs.org/projects/disambigufile/badge/?version=latest
        :target: https://disambigufile.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status




Class with file-like interface to a file found in provided search path


* Free software: MIT license
* Documentation: https://disambigufile.readthedocs.io.

Features
--------

- Search a path for a file that matches a pattern
- Search a path for a file inside directories that match a pattern

Examples
--------

.. code-block:: python

  from disambigufile import Disambigufile
  import disambigufile.exceptions
  path = '/bin:/usr/bin:/usr/local/bin'
  try:
      print(Disambigufile('^ls', path=path))
  except disambigufile.exceptions.Error as e:
      print(f"unable to disambiguate file; exception: {e}")

  path = 'path1:path2'
  try:
      with Disambigufile(r'^asdf', path=path).open() as f:
          print(f.read())
  except disambigufile.exceptions.Error as e:
      print(f"unable to disambiguate file; exception: {e}")

  # search for unique file matching ~/Datasets/*2019-08-19*/data*
  path='~/Datasets'
  try:
      hit = Disambigufile(
          pattern='2019-08-19',
          path=path,
          dir=True,
          subpattern='^data',
      )
      print(hit)
  except disambigufile.exceptions.Error as e:
      print(f"unable to disambiguate file; exception: {e}")

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
