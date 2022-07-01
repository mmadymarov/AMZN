"""
This class models the form on the AMZNScout Registration and Login  page
The form consists of input fields, a button
"""
from conf import locators_conf as locators
from utils.wrapit import Wrapit

class RegistrationLoginFormObject:
    """
        Blueprint for the Form of Registration and Login Form
    """
    # Retrieving locators ...
    sign_up_section = locators.sign_up
    sing_in_section = locators.sign_in
    email_field = locators.email_field
    password_filed = locators.password_field
    submit_button = locators.submit_button
    login_iframe = locators.login_iframe

    @Wrapit._exceptionHandler
    def set_email(self, email):
        """Set the email on Registration/Login Form"""
        login_iframe = self.get_element(self.login_iframe)
        self.switch_frame(name=login_iframe) # switch to iframe
        result_flag = self.set_text(self.email_field, email)
        self.switch_frame() # switch back to default content
        self.conditional_write(result_flag,
            positive='Set the email to: %s'%email,
            negative='Failed to set the email in the form',
            level='debug')

        return result_flag
    
    @Wrapit._exceptionHandler
    def set_password(self, password):
        """Set the password on Login Form"""
        login_iframe = self.get_element(self.login_iframe)
        self.switch_frame(name=login_iframe) # switch to iframe
        result_flag = self.set_text(self.password_filed, password)
        self.switch_frame() # switch back to default content
        self.conditional_write(result_flag,
            positive='Set the password to: %s'%password,
            negative='Failed to set the password in the form',
            level='debug')

        return result_flag
    

    @Wrapit._exceptionHandler
    def select_login(self):
        "Click on login section"
        login_iframe = self.get_element(self.login_iframe)
        self.switch_frame(name=login_iframe)   # swith to login iframe
        result_flag = self.click_element(self.sing_in_section)
        self.switch_frame() # swithc back to default content
        self.conditional_write(result_flag,
            positive='Clicked on the "Sign In" section',
            negative='Failed to click on "Sign In" button',
            level='debug')

        return result_flag
    
    @Wrapit._exceptionHandler
    def select_registration(self):
        "Click on registration section"
        login_iframe = self.get_element(self.login_iframe)
        self.switch_frame(name=login_iframe)   # swith to login iframe
        result_flag = self.click_element(self.sign_up_section)
        self.switch_frame() # swithc back to default content
        self.conditional_write(result_flag,
            positive='Clicked on the "Sign Up" section',
            negative='Failed to click on "Sign Up" button',
            level='debug')

        return result_flag
    
    @Wrapit._exceptionHandler
    def submit(self):
        "Click on Continue"
        login_iframe = self.get_element(self.login_iframe)
        self.switch_frame(name=login_iframe)   # swith to login iframe
        result_flag = self.click_element(self.submit_button)
        self.switch_frame() # swithc back to default content
        self.conditional_write(result_flag,
            positive='Clicked on the "Continue" button',
            negative='Failed to click on "Continue" button',
            level='debug')

        return result_flag
    
    


    


    
    


