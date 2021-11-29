Changelog
=========

Verson 1.3.0 [2021-11-29]
-------------------------

- [change] Allow possibility to point swappable dependency to specific migration number
  (instead of only to ``__latest__``)

Version 1.2.0 [2021-11-12]
--------------------------

- [feature] Add possibility to point swappable dependency to ``__latest__``
- [change] Added support for Python 3.9
- [change] Added support for Django 3.2 and Django 4.0a1
- [change] Dropped support for old Django versions (<2.2)
- [change] Dropped support for old Python versions (<3.7)
- [feature] Added optional ``require_ready`` argument to ``load_model`` function

Version 1.1.2 [2020-01-15]
--------------------------

- [deps] Verified support for python 3.8
- [deps] Added support for Django 3.0 and Django Rest Framework 3.11

Version 1.1.1 [2019-07-23]
--------------------------

- [deps] Drop python<3.3 support
- [deps] Added support for python 3.7
- [deps] Django 2 support added

Version 1.1.0 [2017-05-11]
--------------------------

- [test] Added tests for swapper.split
- `#13 <https://github.com/openwisp/django-swappable-models/pull/13>`_ [fix] Handle contrib apps and apps with dot in app_label.

Version 1.0.0 [2016-08-26]
--------------------------

- [docs] Improved usuability docs
- `86e238 <https://github.com/openwisp/django-swappable-models/commit/86e238>`_:
  [deps] Compatibility with django 1.10 added

Version 0.3.0 [2015-11-17]
--------------------------

- `#9 <https://github.com/openwisp/django-swappable-models/pull/9>`_ [deps] Added support for django 1.9

Version 0.2.2 [2015-06-16]
--------------------------

- [deps] Added support for django~=1.6.0
- [deps] Added support for Python 3.3
- [docs] Fix model reference in README
- [docs] Notes for load_model initialization (`for more info see #2 <https://github.com/openwisp/django-swappable-models/issues/2>`_)

Version 0.2.1 [2014-11-18]
--------------------------

- [docs] Added examples for migration scripts
- [docs] Documented use of Functions
- [fix] Fixed Lookup Error in load_model

Version 0.2.0 [2014-09-13]
--------------------------

- [deps] Added support for Django 1.7
- [feature] Added `swapper.dependency` function.
- [tests] Added tests

Version 0.1.1 [2014-01-09]
--------------------------

- [docs] Added References

Version 0.1.0 [2014-01-09]
--------------------------

- Added base functions for swapping models
