import unittest, os
from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

class TestContactManagement(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        option = webdriver.FirefoxOptions()
        option.add_argument('--headless')
        cls.browser = webdriver.Firefox(options=option)
        try:
            cls.url = os.environ['URL']
        except:
            cls.url = "http://localhost/DamnCRUD/src/"

    def login(self):
        self.browser.get(f"{self.url}/login.php")
        self.browser.find_element(By.ID, "inputUsername").send_keys("admin")
        self.browser.find_element(By.ID, "inputPassword").send_keys("nimda666!")
        self.browser.find_element(By.XPATH, "//button[@type='submit']").click()

    def wait_for_url(self, url, timeout=10):
        WebDriverWait(self.browser, timeout).until(
            lambda driver: driver.current_url == url
        )

    def test_1_add_new_contact(self):
        self.login()
        self.browser.get(f"{self.url}/create.php")
        self.browser.find_element(By.ID, 'name').send_keys("John Doe")
        self.browser.find_element(By.ID, 'email').send_keys("john.doe@example.com")
        self.browser.find_element(By.ID, 'phone').send_keys("123456789")
        self.browser.find_element(By.ID, 'title').send_keys("Developer")
        self.browser.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()
        assert self.browser.current_url == f"{self.url}/index.php"

    def test_2_delete_contact(self):
        self.login()
        actions_section = self.browser.find_element(By.XPATH, "//tr[@role='row'][1]//td[contains(@class, 'actions')]")
        delete_button = actions_section.find_element(By.XPATH, ".//a[contains(@class, 'btn-danger')]")
        delete_button.click()
        self.browser.switch_to.alert.accept()
        assert self.browser.current_url == f"{self.url}/index.php"

    def test_3_change_profile_picture(self):
        self.login()
        self.browser.get(f"{self.url}/profil.php")
        file_path = os.path.join(os.getcwd(), 'image_test.jpg')
        self.browser.find_element(By.ID, 'formFile').send_keys(file_path)
        self.browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        assert self.browser.current_url == f"{self.url}/profil.php"

    def test_4_update_contact(self):
        self.login()
        actions_section = self.browser.find_element(By.XPATH, "//tr[@role='row'][1]//td[contains(@class, 'actions')]")
        update_button = actions_section.find_element(By.XPATH, ".//a[contains(@class, 'btn-success')]")
        update_button.click()
        self.browser.find_element(By.ID, 'name').clear()
        self.browser.find_element(By.ID, 'name').send_keys("Jane Doe")
        self.browser.find_element(By.ID, 'email').clear()
        self.browser.find_element(By.ID, 'email').send_keys("jane.doe@example.com")
        self.browser.find_element(By.ID, 'phone').clear()
        self.browser.find_element(By.ID, 'phone').send_keys("987654321")
        self.browser.find_element(By.ID, 'title').clear()
        self.browser.find_element(By.ID, 'title').send_keys("Designer")
        self.browser.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()
        assert self.browser.current_url == f"{self.url}/index.php"

    def test_5_test_xss_security(self):
        self.login() 
        self.browser.get(f"{self.url}/vpage.php")
        self.browser.find_element(By.NAME, 'thing').send_keys("<script>alert(1)</script>")
        self.browser.find_element(By.NAME, 'submit').click()
        
        try:
            alert = self.browser.switch_to.alert
            alert.accept()
            self.fail("XSS vulnerability detected!")
        except NoAlertPresentException:
            pass

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2, warnings='ignore')
