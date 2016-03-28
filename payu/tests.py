from django.test import TestCase

# Create your tests here.


class Sample(TestCase):

    def test_addition(self):
        Sum = 5+4
        self.assertEqual(Sum, 9)
