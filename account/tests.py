from django.test import TestCase
from .models import AccountUser


# Create your tests here.
class AccountModelTest(TestCase):
	def test_email_is_lower(self):
		user=AccountUser(email="IIFEANYI570@GMAIL.COM")
		self.assertIs(user.clean_email(),True)