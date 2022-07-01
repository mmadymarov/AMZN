from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import unittest,time,logging,os,inspect,pytest
from factory.driver_factory import DriverFactory
from utils.base_logging import BaseLogging
import conf.base_url_conf

class Borg:
    #The borg design pattern is to share state
    __shared_state = {}
    def __init__(self):
        self.__dict__ = self.__shared_state

    def is_first_time(self):
        "Has the child class been invoked before?"
        result_flag = False
        if len(self.__dict__)==0:
            result_flag = True

        return result_flag


# Get the Base URL from the conf file
base_url = conf.base_url_conf

class BasePage(Borg,unittest.TestCase):
    "Base Page Class -- a class that all pages can inherit"

    def __init__(self,base_url):
        "Constructor"
        Borg.__init__(self)
        if self.is_first_time():
            # initialize if the page is created first time
            self.set_directory_structure()
            self.image_url_list = []
            self.msg_list = []
            self.current_console_log_errors = []
            self.window_structure = {}
            self.testrail_flag = False
            self.tesults_flag = False
            self.images = []
            self.browserstack_flag = False
            self.highlight_flag = False
            self.test_run_id = None
            self.reset()
        self.base_url = base_url
        #Initialize web driver
        self.driver_obj = DriverFactory()
        if self.driver is not None:
            self.start() #Visit and initialize xpaths for the appropriate page
    
    def reset(self):
        "Reset the base page object"
        self.driver = None
        self.calling_module = None
        self.result_counter = 0 #Increment whenever success or failure are called
        self.pass_counter = 0 #Increment everytime success is called
        self.mini_check_counter = 0 #Increment when conditional_write is called
        self.mini_check_pass_counter = 0 #Increment when conditional_write is called with True
        self.failure_message_list = []
        self.screenshot_counter = 1
        self.exceptions = []
        self.gif_file_name = None
        self.rp_logger = None
    
    def open(self, url, wait_time=5):
        """
            method to launch base_url + url
        """

        if self.base_url[-1] != '/' and url[0] != '/':
            url = '/' + url
        if self.base_url[-1] == '/' and url[0] != '/':
            url = url[1:]
        url = self.base_url + url
        if self.driver.current_url != url:
            self.driver.get(url)
        self.wait(wait_time)
    
    def register_driver(self,remote_flag,os_name,os_version,browser,browser_version,remote_project_name,remote_build_name):
        "Register the driver with Page."
        self.set_screenshot_dir(os_name,os_version,browser,browser_version) # Create screenshot directory
        self.set_log_file()
        self.driver = self.driver_obj.get_web_driver(remote_flag,os_name,os_version,browser,browser_version,remote_project_name,remote_build_name)
        self.driver.implicitly_wait(5)
        self.driver.maximize_window()

        self.start()
    
    def set_screenshot_dir(self,os_name,os_version,browser,browser_version):
        "Set the screenshot directory"
        try:
            self.screenshot_dir = self.get_screenshot_dir(os_name,os_version,browser,browser_version,overwrite_flag=True)
            if not os.path.exists(self.screenshot_dir):
                os.makedirs(self.screenshot_dir)
        except Exception as e:
            self.write("Exception when trying to set screenshot directory")
            self.write(str(e))
            self.exceptions.append("Error when setting up the screenshot directory")
    
    def wait(self, wait_seconds=5, locator=None):
        """
            Method to wait given amount seconds
        """
        if locator is not None:
            self.smart_wait(locator, wait_seconds=wait_seconds)
        else:
            time.sleep(wait_seconds)
    
    def smart_wait(self,locator,wait_seconds=5):
        "Performs an explicit wait for a particular element"
        result_flag = False
        try:
            path = self.split_locator(locator)
            WebDriverWait(self.driver, wait_seconds).until(EC.presence_of_element_located(path))
            result_flag = True
        except Exception:
            self.conditional_write(result_flag,
                                    positive='Located the element: %s'%locator,
                                    negative='Could not locate the element %s even after %.1f seconds'%(locator, wait_seconds))
        return result_flag
    

    def set_text(self, locator, value, clear_flag=True):
        "Set the value of the text field"
        text_field = None
        try:
            text_field = self.get_element(locator)
            if text_field is not None and clear_flag is True:
                try:
                    text_field.clear()
                except Exception as e:
                    self.write(str(e), 'debug')
                    self.exeptions.append("Could not clear the textfield- '%s' in the conf/locators.conf" %locator)
        except Exception as e:
            self.write("Check you locator-'%s,%s' in the conf/locators.conf file" %(locator[0], locator[1]))
        
        result_flag = False
        if text_field is not None:
            try:
                text_field.send_keys(value)
                result_flag = True
            except Exception as e:
                self.write('Could not write to text field: %s'%locator,'debug')
                self.write(str(e),'debug')
                self.exceptions.append("Could not write to text field- '%s' in the conf/locators.conf file"%locator)
        
        return result_flag


    def get_element(self, locator, verbose_flag=True):
        """Returns element by locator if exists, otherwise returns None"""
        dom_element = None
        try:
            locator = self.split_locator(locator)
            dom_element = self.driver.find_element(*locator)
        except Exception as e:
            if verbose_flag is True:
                self.write(str(e), 'debug')
                self.write("Check your locator - '%s, %s' in the conf/locators.conf file" %(locator[0], locator[1]))
            self.exceptions.append("Check your locator - '%s, %s' in the conf/locators.conf file" %(locator[0], locator[1]))

        return dom_element

    def split_locator(self, locator):
        """
            We import locatros in comma seperated 
            in order to use in find_element we 
            need to split locator and return tuple
        """
        result = ()
        try:
            self.write(locator,'debug')
            locator = locator.split(", ")
            result = (locator[0], locator[1])
        except Exception as e:
            self.write(str(e),'debug')
            self.write("Error while parsing locator")
            self.exceptions.append("Unable to split the locator-'%s' in the conf/locators.conf file"%(locator[0],locator[1]))

        return result
    
    def switch_frame(self,name=None,index=None,wait_time=2):
        "switch to iframe"
        self.wait(wait_time)
        self.driver.switch_to.default_content()
        if name is not None:
            self.driver.switch_to.frame(name)
        elif index is not None:
            self.driver.switch_to.frame(self.driver.find_elements_by_tag_name("iframe")[index])
        
    def click_element(self, locator, wait_time=3):
        """Click the button"""
        result_flag = False
        try:
            clickable_element = self.get_element(locator)
            if clickable_element is not None:
                clickable_element.click()
                result_flag = True
                self.wait(wait_time)
        except Exception as e:
            self.write(str(e),'debug')
            self.write('Exception when clicking link with path: %s'%locator)
            self.exceptions.append("Error when clicking the element with path,'%s' in the conf/locators.conf file"%locator)

        return result_flag
    
    def set_log_file(self):
        """Initialize the log file"""
        self.log_name = self.testname + '.log'
        self.log_obj = BaseLogging(log_file_name=self.log_name, level=logging.DEBUG)
    
    def set_rp_logger(self,rp_pytest_service):
        "Set the reportportal logger"
        self.rp_logger = self.log_obj.setup_rp_logging(rp_pytest_service)
    
    def set_calling_module(self,name):
        "Set the test name"
        self.calling_module = name

    def get_calling_module(self):
        "Get the name of the calling module"
        if self.calling_module is None:
            #Try to intelligently figure out name of test when not using pytest
            full_stack = inspect.stack()
            index = -1
            for stack_frame in full_stack:
                print(stack_frame[1],stack_frame[3])
                #stack_frame[1] -> file name
                #stack_frame[3] -> method
                if 'test_' in stack_frame[1]:
                    index = full_stack.index(stack_frame)
                    break
            test_file = full_stack[index][1]
            test_file = test_file.split(os.sep)[-1]
            testname = test_file.split('.py')[0]
            self.set_calling_module(testname)

        return self.calling_module
    
    def set_directory_structure(self):
        "Setup the required directory structure if it is not already present"
        try:
            self.screenshots_parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','screenshots'))
            if not os.path.exists(self.screenshots_parent_dir):
                os.makedirs(self.screenshots_parent_dir)
            self.logs_parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','log'))
            if not os.path.exists(self.logs_parent_dir):
                os.makedirs(self.logs_parent_dir)
        except Exception as e:
            self.write("Exception when trying to set directory structure")
            self.write(str(e))
            self.exceptions.append("Error when setting up the directory structure")
    
    def get_screenshot_dir(self,os_name,os_version,browser,browser_version,overwrite_flag=False):
        "Get the name of the test"
        if os_name == 'OS X':
            os_name = 'OS_X'
        if isinstance(os_name,list):
            windows_browser_combination = browser.lower()
        else:
            windows_browser_combination = os_name.lower() + '_' + str(os_version).lower() + '_' + browser.lower()+ '_' + str(browser_version)
        self.testname = self.get_calling_module()
        self.testname =self.testname.replace('<','')
        self.testname =self.testname.replace('>','')
        self.testname = self.testname + '[' + str(windows_browser_combination)+ ']'
        self.screenshot_dir = self.screenshots_parent_dir + os.sep + self.testname
        if os.path.exists(self.screenshot_dir) and overwrite_flag is True:
            for i in range(1,4096):
                if os.path.exists(self.screenshot_dir + '_'+str(i)):
                    continue
                else:
                    os.rename(self.screenshot_dir,self.screenshot_dir +'_'+str(i))
                    break

        return self.screenshot_dir
    

    def write(self, msg, level='info'):
        """Log the message"""
        msg = str(msg)
        self.msg_list.append('%-8s:  '%level.upper() + msg)
        self.log_obj.write(msg, level)
    
    def conditional_write(self,flag,positive,negative,level='info'):
        "Write out either the positive or the negative message based on flag"
        self.mini_check_counter += 1
        if level.lower() == "inverse":
            if flag is True:
                self.write(positive,level='error')
            else:
                self.write(negative,level='info')
                self.mini_check_pass_counter += 1
        else:
            if flag is True:
                self.write(positive,level='info')
                self.mini_check_pass_counter += 1
            else:
                self.write(negative,level='error')
    
    
    def success(self,msg,level='info',pre_format='PASS: '):
        "Write out a success message"
        if level.lower() == 'critical':
            level = 'info'
        self.log_obj.write(pre_format + msg,level)
        self.result_counter += 1
        self.pass_counter += 1


    def failure(self,msg,level='info',pre_format='FAIL: '):
        "Write out a failure message"
        self.log_obj.write(pre_format + msg,level)
        self.result_counter += 1
        self.failure_message_list.append(pre_format + msg)
        if level.lower() == 'critical':
            self.teardown()

    def get_current_url(self):
        "Get the current URL"
        return self.driver.current_url
            
    def log_result(self,flag,positive,negative,level='info'):
        "Write out the result of the test"
        if level.lower() == "inverse":
            if flag is True:
                self.failure(positive,level="error")
            else:
                self.success(negative,level="info")
        else:
            if flag is True:
                self.success(positive,level=level)
            else:
                self.failure(negative,level=level)
    
    def start(self):
        "Overwrite this method in your Page module if you want to visit a specific URL"
        pass
    
    def teardown(self):
        "Tears down the driver"
        self.driver.quit()
        self.reset()

    
    
    
                


