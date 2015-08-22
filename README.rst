Django-PayU
==============

This package provides integration between `Django` and `PayU Payment Gateway`.

Quick start
------------

1. Install 'django-payu' using the following command.

    .. code-block:: python

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

4. Finally, run the following command.

    .. code-block:: python

        python manage.py syncdb
