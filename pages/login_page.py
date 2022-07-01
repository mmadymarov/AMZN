from .base import BasePage
from .registration_form_object import RegistrationLoginFormObject

class LoginPage(BasePage, RegistrationLoginFormObject):
    """
        Page Object for Login Page
    
    """

    def start(self):
        """
            Method to start the page
        """
        url = '/app/#/auth/login?redirect=%2Fdatabase'
        self.open(url)