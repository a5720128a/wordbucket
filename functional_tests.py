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
        header_text = self.browser.find_element_by_tag_name('h1').text  
        self.assertIn('Word Bucket', header_text) 
        
        # She is invited to enter a word item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Add new word'
        )
        
        # She types "weeb" into a text box
        inputbox.send_keys('weeb')
        
        # When she hits enter, the page updates, and now the page word lists
        # "1: weeb" as an item in a word list table
        inputbox.send_keys(Keys.ENTER)  
        time.sleep(1)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')  
        self.assertTrue(
            any(row.text == '1: weeb' for row in rows)
        )
        self.fail('Finish the test!') 

if __name__ == '__main__':  
    unittest.main(warnings='ignore')
