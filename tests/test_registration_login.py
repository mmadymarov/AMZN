import os,sys 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from factory.page_factory import PageFactory
import pytest
import conf.local_driver_options as l_driver_options
import conf.testing_data as test_data
from faker import Faker

def test_successive_login():

    """
        Test to check user successfull 
        login with correct credentials
    """

    try:
        #Initialize flags for counter
        expected_pass = 0
        actual_pass = -1

        
        test_obj = PageFactory.get_page_object("sign in")

        test_obj.register_driver(l_driver_options.remote_flag, l_driver_options.os_name, 
                                     l_driver_options.os_version, l_driver_options.browser, 
                                     l_driver_options.browser_options, l_driver_options.remote_project_name, 
                                     l_driver_options.remote_build_name)

        email = test_data.email
        password = test_data.password

        result_flag = test_obj.select_login()
        test_obj.log_result(result_flag,
                                positive="Successfully Selected 'Sign In' section\n",
                                negative="Failed to select Sign In section \nOn url: %s\n"%test_obj.get_current_url())

        result_flag = test_obj.set_email(email)
        test_obj.log_result(result_flag,
                                positive="Email was successfully set to: %s\n"%email,
                                negative="Failed to set name: %s \nOn url: %s\n"%(email,test_obj.get_current_url()))

        result_flag = test_obj.set_password(password)
        test_obj.log_result(result_flag,
                                positive="Password was successfully set to: %s\n"%password,
                                negative="Failed to set password: %s \nOn url: %s\n"%(email,test_obj.get_current_url()))

        result_flag = test_obj.submit()
        test_obj.log_result(result_flag,
                                positive="Login credentials successfully submitted",
                                negative="Failed to submit the login credentials \nOn url %s\n:"%(test_obj.get_current_url()))

        expected_pass = test_obj.result_counter
        actual_pass = test_obj.pass_counter
    
    except Exception as e:
        print("Exception when trying to run test: %s"%(__file__))
        print("Python says:%s"%str(e))
    
    test_obj.wait(3)
    test_obj.teardown()
    assert expected_pass == actual_pass, "Test Failed: %s"%(__file__)

def test_successive_registration():

    """
        Testcase to check user successfull 
        registration with correct email
    """

    try:
        #Initialize flags for counter
        expected_pass = 0
        actual_pass = -1

        
        test_obj = PageFactory.get_page_object("sign up")

        test_obj.register_driver(l_driver_options.remote_flag, l_driver_options.os_name, 
                                     l_driver_options.os_version, l_driver_options.browser, 
                                     l_driver_options.browser_options, l_driver_options.remote_project_name, 
                                     l_driver_options.remote_build_name)

        fake = Faker()
        email = fake.email()

        result_flag = test_obj.select_registration()
        test_obj.log_result(result_flag,
                                positive="Successfully Selected 'Sign Up' section\n",
                                negative="Failed to select Sign Up section \nOn url: %s\n"%test_obj.get_current_url())

        result_flag = test_obj.set_email(email)
        test_obj.log_result(result_flag,
                                positive="Email was successfully set to: %s\n"%email,
                                negative="Failed to set name: %s \nOn url: %s\n"%(email,test_obj.get_current_url()))

        result_flag = test_obj.submit()
        test_obj.log_result(result_flag,
                                positive="Registration email successfully submitted",
                                negative="Failed to submit the email \nOn url %s\n:"%(test_obj.get_current_url()))

        expected_pass = test_obj.result_counter
        actual_pass = test_obj.pass_counter
    
    except Exception as e:
        print("Exception when trying to run test: %s"%(__file__))
        print("Python says:%s"%str(e))
    
    test_obj.wait(3)
    test_obj.teardown()
    assert expected_pass == actual_pass, "Test Failed: %s"%(__file__)


  



