from selenium.webdriver.chrome.options import Options
import sys
from selenium import webdriver

class LocalBrowsers():
    
    """
        Class contains methods for getting webfrivers for various browsers.
    """

    @staticmethod
    def firefox_local():
        """Get webdriver for firefox."""
        local_driver = webdriver.Firefox()

        return local_driver

    @staticmethod
    def explorer_local():
        """Get webdriver for internet explorer."""
        local_driver = webdriver.Ie()

        return local_driver

    @staticmethod
    def chrome_local():
        """Get webdriver for chrome."""
        local_driver = webdriver.Chrome()

        return local_driver

    @staticmethod
    def safari_local():
        """Get webdriver for safari."""
        local_driver = webdriver.Safari()

        return local_driver

    @staticmethod
    def headless_chrome():
        """Set up headless chrome driver options and get webdriver for headless chrome."""
        options = Options()
        options.headless = True
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-extensions")
        options.add_argument("--proxy-server='direct://'")
        options.add_argument("--proxy-bypass-list=*")
        options.add_argument("--start-maximized")
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        options.add_argument('--ignore-certificate-errors')
        local_driver = webdriver.Chrome(options=options)

        return local_driver