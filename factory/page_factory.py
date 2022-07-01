from pages.registration_page import RegistrationPage
from pages.login_page import LoginPage

import conf.base_url_conf


class PageFactory():
    """
    Uses page factory design pattern
    
    """
    def get_page_object(page_name, base_url=conf.base_url_conf.base_url):
        """
            Returns the appropriate page object 
        """
        test_obj = None
        page_name = page_name.lower()
        if page_name in ["registration", "sign up"]:
            test_obj = RegistrationPage(base_url=base_url)
        elif page_name in ["login", "sign in"]:
            test_obj = LoginPage(base_url=base_url)
        return test_obj
    
    get_page_object = staticmethod(get_page_object)
