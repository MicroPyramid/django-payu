from payu.models import Transaction, CancelRefundCaptureRequests
from django.core.exceptions import ObjectDoesNotExist
from django.utils.http import urlencode
from django.conf import settings
from hashlib import sha512
from uuid import uuid4
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
import json


KEYS = ('txnid', 'amount', 'productinfo', 'firstname', 'email',
        'udf1', 'udf2', 'udf3', 'udf4', 'udf5', 'udf6', 'udf7', 'udf8',
        'udf9', 'udf10')

Webservicekeys = ('key', 'command', 'var1')


def get_hash(data):
    # Generate hash sequence before posting the transaction to PayU:
    # sha512(key|txnid|amount|productinfo|firstname|email|udf1|udf2|udf3|udf4|udf5||||||SALT)

    hash_value = sha512(str(getattr(settings, 'PAYU_MERCHANT_KEY', None)).encode('utf-8'))

    for key in KEYS:
        if data.get(key) == None:
            hash_value.update((("%s%s" % ('|', str('')))).encode("utf-8"))
        else:
            hash_value.update(("%s%s" % ('|', str(data.get(key, '')))).encode("utf-8"))

    hash_value.update(("%s%s".format('|', getattr(settings, 'PAYU_MERCHANT_SALT', None))).encode('utf-8'))

    # Create transaction record
    Transaction.objects.create(
        transaction_id=data.get('txnid'), amount=data.get('amount'))
    return hash_value.hexdigest().lower()


def check_hash(data):
    # Generate hash sequence and verify it with the hash sent by PayU in the Post Response

    Reversedkeys = reversed(KEYS)
    if data.get('additionalCharges'):
        # if the additionalCharges parameter is posted in the transaction response,then hash formula is:
        # sha512(additionalCharges|SALT|status||||||udf5|udf4|udf3|udf2|udf1|email|firstname|productinfo|amount|txnid|key)

        hash_value = sha512(str(data.get('additionalCharges')).encode('utf-8'))
        hash_value.update(("%s%s" % ('|', getattr(settings, 'PAYU_MERCHANT_SALT', None))).encode('utf-8'))
    else:
        # If additionalCharges parameter is not posted in the transaction response, then hash formula is the generic reverse hash formula
        # sha512(SALT|status||||||udf5|udf4|udf3|udf2|udf1|email|firstname|productinfo|amount|txnid|key)

        hash_value = sha512(getattr(settings, 'PAYU_MERCHANT_SALT', None))

    hash_value.update(("%s%s" % ('|', str(data.get('status', '')))).encode('utf-8'))

    for key in Reversedkeys:
        hash_value.update(("%s%s" % ('|', str(data.get(key, '')))).encode('utf-8'))

    hash_value.update(("%s%s" % ('|', getattr(settings, 'PAYU_MERCHANT_KEY', None))).encode('utf-8'))

    # Updating the transaction
    transaction = Transaction.objects.get(transaction_id=data.get('txnid'))
    transaction.payment_gateway_type = data.get('PG_TYPE')
    transaction.transaction_date_time = data.get('addedon')
    transaction.mode = data.get('mode')
    transaction.status = data.get('status')
    transaction.amount = data.get('amount')
    transaction.mihpayid = data.get('mihpayid')
    transaction.bankcode = data.get('bankcode')
    transaction.bank_ref_num = data.get('bank_ref_num')
    transaction.discount = data.get('discount')
    transaction.additional_charges = data.get('additionalCharges', 0)
    transaction.txn_status_on_payu = data.get('unmappedstatus')
    transaction.hash_status = "Success" if hash_value.hexdigest().lower() == data.get('hash') else "Failed"
    transaction.save()

    return (hash_value.hexdigest().lower() == data.get('hash'))


def get_webservice_hash(data):
    # Generate hash sequence using the string sha512(key|command|var1|salt)
    hash_value = sha512(''.encode("utf-8"))
    for key in Webservicekeys:
        hash_value.update(("%s%s" % (str(data.get(key, '')), '|')).encode("utf-8"))

    hash_value.update(getattr(settings, 'PAYU_MERCHANT_SALT', None).encode("utf-8"))
    return hash_value.hexdigest().lower()


def payu_url():
    # Return the url based on mode of the environment.
    if getattr(settings, 'PAYU_MODE', 'TEST').lower() == "test":
        return 'https://test.payu.in/_payment'
    elif getattr(settings, 'PAYU_MODE', 'TEST').lower() == "live":
        return 'https://secure.payu.in/_payment'
    else:
        return None


def post(params):
    if not params['command'] == "check_action_status" or "verify_payment":
        try:
            # Check whether the transaction exists or not
            Transaction.objects.get(mihpayid=params['var1'])
        except ObjectDoesNotExist:
            # if not return error message
            error_message = "Transaction with this mihpayid does not exist."
            return error_message

    params = params
    params['key'] = getattr(settings, 'PAYU_MERCHANT_KEY', None)

    # Generate the hash value
    params['hash'] = get_webservice_hash(params)

    if getattr(settings, 'PAYU_MODE', 'TEST').lower() == "test":
        url = 'https://test.payu.in/merchant/postservice.php?form=2'
    elif getattr(settings, 'PAYU_MODE', 'TEST').lower() == "live":
        url = 'https://info.payu.in/merchant/postservice.php?form=2'
    else:
        return None

    payload = urlencode(params)

    request = urllib2.Request(url)
    request.add_data(payload)
    response = (urllib2.urlopen(request))

    response = json.loads(response.read())

    return response


# This command is used to verify the transaction with PayU.
def verify_payment(txnid):
    params = {}
    params['command'] = "verify_payment"

    # Put all the txnid(Your transaction ID/order ID) values in a pipe separated form. Ex:100123|100124|100125|100126
    # Ex: params['var1'] = "316a5043e00c46aab55f94dfae1dd2d9|239de01417164b1898550e07f83fccff"
    params['var1'] = txnid

    return post(params)


# This command is used to check payment after transaction.
def check_payment(mihpayid):
    params = {}
    params['command'] = "check_payment"
    # Pass the Payu id (mihpayid) of the transaction to check.
    params['var1'] = mihpayid

    return post(params)


# API is applicable only for transactions in auth status and nothing else.
def capture_transaction(mihpayid):
    params = {}
    params['command'] = "capture_transaction"
    params['var1'] = mihpayid      # Pass the Payu id (mihpayid) of the transaction to capture.
    params['var2'] = uuid4().hex   # token ID(unique token from merchant)

    response = post(params)

    if type(response) == type(dict()) and 'request_id' in response.keys():
        CancelRefundCaptureRequests.objects.create(
            request_id=response['request_id'],
            request_type="Capture",
            transaction=Transaction.objects.get(mihpayid=mihpayid),
            status=response['status'],
            message=response['msg'],
            mihpayid=response['mihpayid'] if response['mihpayid'] else mihpayid,
            bank_ref_num=response['bank_ref_num'],
            error_code=response['error_code'] if response['error_code'] else "")
    return response


# This command is used to refund a captured transaction. Refund can occur only after one day of capture.
def refund_transaction(mihpayid, amount):
    params = {}
    params['command'] = "refund_transaction"
    params['var1'] = mihpayid      # Pass the Payu id (mihpayid) of the transaction to capture.
    params['var2'] = uuid4().hex   # token ID(unique token from merchant)
    params['var3'] = amount

    response = post(params)

    if type(response) == type(dict()) and 'request_id' in response.keys():
        CancelRefundCaptureRequests.objects.create(
            request_id=response['request_id'],
            request_type="Refund",
            transaction=Transaction.objects.get(mihpayid=mihpayid),
            status=response['status'],
            message=response['msg'],
            amount=amount,
            mihpayid=response['mihpayid'] if response['mihpayid'] else mihpayid,
            bank_ref_num=response['bank_ref_num'],
            error_code=response['error_code'] if response['error_code'] else "")
    return response


# This command is used to cancel an auth transaction.
def cancel_transaction(mihpayid, amount):
    params = {}
    params['command'] = "cancel_transaction"
    params['var1'] = mihpayid      # Pass the Payu id (mihpayid) of the transaction to capture.
    params['var2'] = uuid4().hex   # token ID(unique token from merchant)
    params['var3'] = amount

    response = post(params)
    if type(response) == type(dict()) and 'request_id' or 'txn_update_id' in response.keys():
        CancelRefundCaptureRequests.objects.create(
            request_id=response['request_id'] if response['request_id'] else response['txn_update_id'],
            request_type="Cancel",
            transaction=Transaction.objects.get(mihpayid=mihpayid),
            status=response['status'],
            message=response['msg'],
            amount=amount,
            mihpayid=response['mihpayid'] if response['mihpayid'] else mihpayid,
            bank_ref_num=response['bank_ref_num'],
            error_code=response['error_code'] if response['error_code'] else "")
    return response


# This command can be used for 2 different purposes:
#  1.To cancel a transaction which is in auth state at the moment
#  2.To refund a transaction which is in captured state at the moment
def cancel_refund_transaction(mihpayid, amount):
    params = {}
    params['command'] = "cancel_refund_transaction"
    params['var1'] = mihpayid      # Pass the Payu id (mihpayid) of the transaction to cancel/ Refund.
    params['var2'] = uuid4().hex   # token ID(unique token from merchant) for only the refund request.

    # Amount which needs to be refunded. Please note that both partial and full refunds are allowed.
    params['var3'] = amount

    response = post(params)

    if type(response) == type(dict()) and 'request_id' in response.keys():
        CancelRefundCaptureRequests.objects.create(
            request_id=response['request_id'],
            request_type="Cancel/Refund",
            transaction=Transaction.objects.get(mihpayid=mihpayid),
            status=response['status'],
            message=response['msg'],
            amount=amount,
            mihpayid=response['mihpayid'] if response['mihpayid'] else mihpayid,
            bank_ref_num=response['bank_ref_num'],
            error_code=response['error_code'])
    return response


# This API is used to check the status of refund/cancel requests
def check_action_status(request_id):
    params = {}
    params['command'] = "check_action_status"
    params['var1'] = request_id    # Pass the Cancel Refund Request ID.

    return post(params)
