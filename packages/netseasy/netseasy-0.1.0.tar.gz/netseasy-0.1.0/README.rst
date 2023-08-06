netseasy - Django gateway for the payment solution 'Easy' from Nets
===================================================================

.. image:: https://gitlab.com/norsktest/netseasy/badges/master/pipeline.svg
   :target: https://gitlab.com/norsktest/netseasy/commits/master
   :alt: pipeline status

.. image:: https://img.shields.io/badge/docs-darkgreen.svg
   :target: https://norsktest.gitlab.io/netseasy

.. image:: https://gitlab.com/norsktest/netseasy/badges/master/coverage.svg
   :target: https://norsktest.gitlab.io/netseasy/coverage
   :alt: coverage report


This is a django gateway for the 'Easy' payment solution from Nets.
The EasyAPI is a REST-API and supports webhooks to send updates back to Django.


Installation
------------

For the current stable version::

    pip install netseasy

For the development version::

    pip install -e git+git@gitlab.com:norsktest/netseasy.git
