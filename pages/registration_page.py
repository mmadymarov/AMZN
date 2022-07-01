from nturl2path import url2pathname
from .base import BasePage
from .registration_form_object import RegistrationLoginFormObject

class RegistrationPage(BasePage, RegistrationLoginFormObject):
    """
        Page Object for Registration Page
    
    """

    def start(self):
        """
            Method to start the page
        """
        url = '/app/#/auth/login?redirect=%2Fdatabase'
        self.open(url)