from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from time import sleep
import sys
from insta_password import insta_pw

class InstaBot:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://instagram.com")
        sleep(3)

    def login(self, username, pw):
        self.driver.find_element_by_xpath("//input[@name=\"username\"]").send_keys(username)
        self.driver.find_element_by_xpath("//input[@name=\"password\"]").send_keys(pw)
        self.driver.find_element_by_xpath('//button[@type="submit"]').click()
        sleep(3)
        self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]")\
            .click()
        sleep(3)

    def go_to_page(self, account_name):
        self.driver.get("https://instagram.com/{}".format(str(account_name)))

    def scroll(self, scroll_amount):
        scroll_js_code = "window.scrollBy(0,{})".format(int(scroll_amount))
        self.driver.execute_script(scroll_js_code)

    def scrape_posts(self, account_name):
        self.go_to_page(account_name)
        first_post = self.driver.find_element_by_xpath("//div[@class=\"_9AhH0\"]")
        first_post.click()
        sleep(3)
        last_post = False
        while not last_post:
            try:
                self.driver.find_element_by_xpath("//a[@class=\" _65Bje  coreSpriteRightPaginationArrow\"]").click()
                sleep(2)
                #todo: get caption, link, location
            except:
                last_post=True
                print("All posts scraped!")
        print("Donezos")

post_scraper=InstaBot()
post_scraper.login('drumprogress', insta_pw())
users_to_scrape = []
for user in users:
    post_scraper.scrape_posts(user)
