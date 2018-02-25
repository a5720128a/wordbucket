from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):  

    def setUp(self):  
        self.browser = webdriver.Firefox()

    def tearDown(self):  
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):  
        # Ann has heard about a cool new online word app. She goes
        # to check out its homepage
        self.browser.get('http://localhost:8000')

        # She notices the page title and header mention Word Bucket lists
        self.assertIn('Word Bucket', self.browser.title)
        self.fail('Finish the test!')  

        # She is invited to enter a word item straight away
        # She types "weeb" into a text box

if __name__ == '__main__':  
    unittest.main(warnings='ignore')
