from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class SessionsTest(LiveServerTestCase):
    fixtures = ['admin_user.json']

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_log_in_and_out(self):
        self.browser.get(self.live_server_url)
        
        # admin email
        email_field = self.browser.find_element_by_name('email')
        email_field.send_keys('a@b.com')

        #admin password
        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('admin')
        password_field.send_keys(Keys.RETURN)

        header = self.browser.find_element_by_tag_name('h1')
        self.assertIn('inbox', body.text)

        self.browser.find_elements_by_link_text('Logout').click()

        header = self.browser.find_element_by_tag_name('h1')
        self.assertIn('Bulletin', body.text)