======================
Configuration Settings
======================

In order to test your integration, first create a **PayU** Account. Once this has been created, you will be given the following...

* *Key (MerchantID)* – This ID is generated at the time of activation of your site and helps to uniquely identify you to PayU.
* *SALT* – This will be provided by PayU.in.

Add the following settings to the PAYU_INFO dictionary using the details from your PayU account::

    PAYU_MERCHANT_KEY = "Your MerchantID",

    PAYU_MERCHANT_SALT = "Your MerchantSALT",

    # And add the PAYU_MODE to 'TEST' for testing and 'LIVE' for production.
    PAYU_MODE = "TEST"

