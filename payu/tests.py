from django.test import TestCase


class Sample(TestCase):

    def test_addition(self):
        Sum = 5 + 4
        self.assertEqual(Sum, 9)
