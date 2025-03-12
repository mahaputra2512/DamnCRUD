import unittest, os
from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
        # Memastikan login berhasil
        WebDriverWait(self.browser, 10).until(
            lambda driver: driver.current_url == f"{self.url}/index.php"
        )

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
        # Pastikan diarahkan ke halaman index setelah menambah kontak
        self.wait_for_url(f"{self.url}/index.php")
        assert self.browser.current_url == f"{self.url}/index.php"

    def test_2_delete_contact(self):
        self.login()
        # Pastikan kita berada di halaman index
        self.browser.get(f"{self.url}/index.php")
        # Temukan tombol delete pada baris pertama tabel
        actions_section = self.browser.find_element(By.XPATH, "//td[contains(@class, 'actions')]")
        delete_button = actions_section.find_element(By.XPATH, ".//a[contains(@class, 'btn-danger')]")
        delete_button.click()
        # Konfirmasi dialog alert
        self.browser.switch_to.alert.accept()
        # Verifikasi kembali ke halaman index
        self.wait_for_url(f"{self.url}/index.php")
        assert self.browser.current_url == f"{self.url}/index.php"

    def test_3_change_profile_picture(self):
        # Siapkan file gambar untuk pengujian
        self.login()
        self.browser.get(f"{self.url}/profil.php")
        # Pastikan file gambar test tersedia di direktori yang sama dengan script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        file_path = os.path.join(parent_dir, 'image_test.jpg')
        # Jika file tidak ada, buat file dummy untuk pengujian
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                f.write('dummy image content')
        # Upload gambar
        self.browser.find_element(By.ID, 'formFile').send_keys(file_path)
        self.browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        # Verifikasi tetap di halaman profil
        self.wait_for_url(f"{self.url}/profil.php")
        assert self.browser.current_url == f"{self.url}/profil.php"

    def test_4_update_contact(self):
        self.login()
        # Pastikan kita berada di halaman index
        self.browser.get(f"{self.url}/index.php")
        # Temukan tombol edit pada baris pertama tabel
        actions_section = self.browser.find_element(By.XPATH, "//td[contains(@class, 'actions')]")
        update_button = actions_section.find_element(By.XPATH, ".//a[contains(@class, 'btn-success')]")
        update_button.click()
        # Update data kontak
        name_field = self.browser.find_element(By.ID, 'name')
        name_field.clear()
        name_field.send_keys("Jane Doe")
        
        email_field = self.browser.find_element(By.ID, 'email')
        email_field.clear()
        email_field.send_keys("jane.doe@example.com")
        
        phone_field = self.browser.find_element(By.ID, 'phone')
        phone_field.clear()
        phone_field.send_keys("987654321")
        
        title_field = self.browser.find_element(By.ID, 'title')
        title_field.clear()
        title_field.send_keys("Designer")
        
        self.browser.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()
        # Verifikasi kembali ke halaman index
        self.wait_for_url(f"{self.url}/index.php")
        assert self.browser.current_url == f"{self.url}/index.php"

    def test_5_test_xss_security(self):
        self.login() 
        self.browser.get(f"{self.url}/vpage.php")
        # Uji untuk kerentanan XSS
        self.browser.find_element(By.NAME, 'thing').send_keys("<script>alert(1)</script>")
        self.browser.find_element(By.NAME, 'submit').click()
        
        try:
            # Jika alert muncul, itu berarti ada kerentanan XSS
            WebDriverWait(self.browser, 3).until(EC.alert_is_present())
            alert = self.browser.switch_to.alert
            alert.accept()
            self.fail("XSS vulnerability detected!")
        except:
            # Tidak ada alert berarti aplikasi aman dari XSS
            pass

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2, warnings='ignore')
