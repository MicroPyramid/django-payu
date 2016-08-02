Django-PayU
==============
.. image:: http://travis-ci.org/MicroPyramid/django-payu.svg?branch=master
    :target: http://travis-ci.org/MicroPyramid/django-payu
.. image:: https://coveralls.io/repos/github/MicroPyramid/django-payu/badge.svg?branch=master
    :target: https://coveralls.io/github/MicroPyramid/django-payu?branch=master
.. image:: https://img.shields.io/github/license/micropyramid/django-payu.svg
    :target: https://pypi.python.org/pypi/django-payu/
.. image:: https://landscape.io/github/MicroPyramid/django-payu/master/landscape.svg?style=flat
   :target: https://landscape.io/github/MicroPyramid/django-payu/master
   :alt: Code Health


This package provides integration between `Django` and `PayU Payment Gateway`.


Quick start
------------

1. Install 'django-payu' using the following command::

    pip install django-payu

2. Add "payu" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ....
        ....
        'payu',
    ]

3. Add the following settings in the setting file using the details from your PayU account::

    PAYU_MERCHANT_KEY = "Your MerchantID",

    PAYU_MERCHANT_SALT = "Your MerchantSALT",

    # And add the PAYU_MODE to 'TEST' for testing and 'LIVE' for production.
    PAYU_MODE = "TEST"

4. Finally, run the following commands::

    python manage.py migrate


For additional help you can `Contact us here`_

.. _contact us here: https://micropyramid.com/contact-us/
