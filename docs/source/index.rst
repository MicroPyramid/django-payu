.. django_payu documentation master file, created by
   sphinx-quickstart on Sat Aug 22 16:31:28 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to django_payu's documentation!
=======================================

This package provides integration between django and PayU Payment Gateway.

Installation
------------

Install::

    pip install django-payu

Next, add ``payu`` to your ``INSTALLED_APPS`` setting like this::

    INSTALLED_APPS = [
        ....
        ....
        'payu',
    ]

Then, add the following settings in the setting file using the details from your PayU account::

    PAYU_MERCHANT_KEY = "Your MerchantID",

    PAYU_MERCHANT_SALT = "Your MerchantSALT",

    # Change the PAYU_MODE to 'LIVE' for production.
    PAYU_MODE = "TEST"

Finally, run the following command::

    python manage.py syncdb


Contents:

.. toctree::
   :maxdepth: 2



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

