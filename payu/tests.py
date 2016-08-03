from django.test import TestCase
from django.conf import settings
from payu.models import *
from payu.gateway import (
    get_hash,
    check_hash,
    get_webservice_hash,
    payu_url,
    post,
    verify_payment,
    check_payment,
    capture_transaction,
    refund_transaction,
    cancel_transaction,
    check_action_status,
    cancel_refund_transaction,
)


setattr(settings, 'PAYU_MERCHANT_KEY', 'JBZaLc')
setattr(settings, 'PAYU_MERCHANT_SALT', 'GQs7yium')


class Sample(TestCase):

    def test_addition(self):
        Sum = 5 + 4
        self.assertEqual(Sum, 9)


class GetHash(TestCase):

    def test_get_hash(self):
        data = {'email': 'hello@micropyramid.com',
                'txnid': 123456,
                'amount': 300}
        response = get_hash(data)
        self.assertTrue(response)
        data['email'] = None
        response = get_hash(data)
        self.assertTrue(response)


class CheckHash(TestCase):

    def setUp(self):
        self.transaction = Transaction.objects.create(transaction_id=123456,
                                                      amount=300)

    def test_check_hash(self):
        data = {'additionalCharges': 220,
                'txnid': 123456,
                'amount': 500,
                'discount': 50}
        response = check_hash(data)
        self.assertFalse(response)


class GetWebServiceHash(TestCase):

    def test_get_webservice_hash(self):
        data = {'key': 12345}
        response = get_webservice_hash(data)
        self.assertTrue(response)


class PayuUrl(TestCase):

    def test_payu_url(self):
        setattr(settings, 'PAYU_MODE', 'TEST')
        reslut = payu_url()
        setattr(settings, 'PAYU_MODE', 'LIVE')
        reslut = payu_url()
        self.assertTrue(reslut)
        setattr(settings, 'PAYU_MODE', 'None')
        reslut = payu_url()
        self.assertFalse(reslut)


class Post(TestCase):

    def get_trans(self):
        self.transaction = Transaction.objects.create(transaction_id=123456,
                                                      amount=300,
                                                      mihpayid=123)

    def test_post(self):
        params = {'command': 'check_action_status',
                  'key': 'dummy11',
                  'hash': '12355',
                  'var1': 55}
        response = post(params)
        self.assertTrue(response)
        self.get_trans()
        params['var1'] = 123
        response = post(params)
        self.assertFalse(response)

    def tearDown(self):
        if hasattr(self, 'transaction'):
            self.transaction.delete()


class VerifyPayment(TestCase):

    def setUp(self):
        Transaction.objects.create(transaction_id=123456,
                                   amount=300,
                                   mihpayid=123)
        # setattr(settings, 'PAYU_MODE', 'TEST')

    def test_verify_payment(self):
        r = verify_payment(txnid=123)
        self.assertFalse(r)

    def test_check_payment(self):
        r = check_payment(123)
        self.assertFalse(r)

    def test_capture_transaction(self):
        capture_transaction(123)

    def test_refund_transaction(self):
        refund_transaction(123, 123)

    def test_check_action_status(self):
        check_action_status(123)

    def test_cancel_refund_transaction(self):
        cancel_refund_transaction(123, 10)
