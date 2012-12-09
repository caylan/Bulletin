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

    def test_functions(self):
	#admin page
        self.browser.get(self.live_server_url + '/admin/')

        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Django administration', body.text)
	
	#log in
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('test')

        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('test')
        password_field.send_keys(Keys.RETURN)

        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Site administration', body.text)

	logout_link = self.browser.find_element_by_link_text('Log out')
	logout_link.click()

	#base page
        self.browser.get(self.live_server_url)

        login_header = self.browser.find_element_by_tag_name('h1')
        self.assertIn('Bulletin', login_header.text)
        
	login_accordian = self.browser.find_element_by_id('Log in')
	login_accordian.click()

        # admin email
        email_field = self.browser.find_element_by_name('email')
        email_field.send_keys('test@test.com')

        #admin password
        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('test')
        password_field.send_keys(Keys.RETURN)
        #log in

        inbox_header = self.browser.find_element_by_tag_name('h1')
        self.assertIn('inbox', inbox_header.text)

	new_group_link = self.browser.find_element_by_link_text('New Group')
	new_group_link.click()

	group_name_field = self.browser.find_element_by_name('name')
        group_name_field.send_keys('test group')
        group_name_field.send_keys(Keys.RETURN)

	new_group_link = self.browser.find_element_by_link_text('test group')
	new_group_link.click()

	test_post = self.browser.find_element_by_name('message')
        test_post.send_keys('test post')
        test_post.send_keys(Keys.RETURN)
	
