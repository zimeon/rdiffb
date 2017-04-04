=======================
Updating rdiffb on pypi
=======================

Notes to remind @zimeon...

rdiffb is at <https://pypi.python.org/pypi/rdiffb>

Putting up a new version
------------------------

  1. Check/bump version number working branch in rdiffb/__init__.py
  2. Check out master and merge in working branch
  3. Check branches are as expected (git branch -a)
  4. Check all tests good (python setup.py test; py.test)
  5. Check local build and version reported OK (python setup.py install)
  6. Upload new version to pypi:

    ```
    python setup.py sdist upload
    ```

  7. Check on PyPI at <https://pypi.python.org/pypi/rdiffb>
  8. On working branch bump version number in `rdiffb/__init__.py`
