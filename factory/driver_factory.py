import os
import sys
from selenium import webdriver
from drivers.local_drivers import LocalBrowsers

class DriverFactory(LocalBrowsers):
    """ Driver Factory class contains web drivers on which tests 
        will run agains
    """
    def __init__(self, browser='ff', browser_version=None, os_name=None):
        """
            Initializing the driver
        
        """
        self.browser = browser
        self.browser_version = browser_version
        self.os_name = os_name
    
    def get_web_driver(self, remote_flag, os_name, os_version, browser,
                       browser_version, remote_project_name, remote_build_name):
        """Return the appropriate driver."""
        if remote_flag.lower() == 'y':
            web_driver = self.select_remote_platform(remote_flag, os_name, os_version,
                                                     browser, browser_version, remote_project_name,
                                                     remote_build_name)

        elif remote_flag.lower() == 'n':
            web_driver = self.run_local(browser)

        return web_driver
    
    def run_local(self, browser):
        """Run the test on local machine, with local drivers"""
        local_driver = None
        if browser.lower() == 'ff' or browser.lower() == 'firefox':
            local_driver = self.firefox_local()
        elif browser.lower() == 'ie':
            local_driver = self.explorer_local()
        elif browser.lower() == 'chrome':
            local_driver = self.chrome_local()
        elif browser.lower() == 'safari':
            local_driver = self.safari_local()
        elif browser.lower() == 'headless-chrome':
            local_driver = self.headless_chrome()
        
        return local_driver
