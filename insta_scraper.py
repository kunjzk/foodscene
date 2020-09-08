from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from time import sleep
import sys
from insta_password import insta_pw
from bs4 import BeautifulSoup
import requests

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
        try:
            self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]").click()
        except:
            pass

    def go_to_page(self, account_name):
        self.driver.get("https://instagram.com/{}".format(str(account_name)))

    def go_to_post_by_link(self, link):
        self.driver.get(link)

    def scroll(self, scroll_amount):
        scroll_js_code = "window.scrollBy(0,{})".format(int(scroll_amount))
        self.driver.execute_script(scroll_js_code)

    def get_post_img_link(self):
        img = self.driver.find_element_by_xpath("//img[@class=\"FFVAD\"]")
        soup = BeautifulSoup(img.get_attribute('outerHTML'),'lxml')
        img_link = soup.find('img')['src']
        return img_link

    def get_post_datetime(self):
        time = self.driver.find_element_by_xpath("//time")
        soup = BeautifulSoup(time.get_attribute('outerHTML'),'lxml')
        datetime = soup.find('time')['datetime']
        return datetime

    def get_post_caption(self, getting_restaurant=False):
        caption = self.driver.find_element_by_xpath("//div[@class=\"C4VMK\"]")
        soup = BeautifulSoup(caption.get_attribute('innerHTML'),'lxml')
        if getting_restaurant: return soup
        captiontext = soup.find_all('span')[1].text
        return captiontext

    def get_restaurant_from_caption(self):
        '''
        Go to all accounts tagged in the caption, check the "category_enum" to
        see if its a personal page or a (food) business
        '''
        personal_account_categories = ["", None, "none", "PERSONAL_BLOG"]
        full_caption_div = self.get_post_caption(getting_restaurant=True)
        caption_html = full_caption_div.find_all('span')[1]
        refs = caption_html.find_all('a')
        for ref in refs:
            homepage_link = "http://instagram.com" + ref['href'] + "?__a=1"
            response=requests.get(homepage_link)
            jsonRequest = response.json()
            category = jsonRequest['graphql']['user']['category_enum']
            if category not in personal_account_categories:
                restaurant = jsonRequest['graphql']['user']['full_name']
                return restaurant, homepage_link
        restaurant = "NIL"
        page = "NIL"
        return restaurant,page

    def get_post_restaurant(self):
        '''
        The restaurant is either in the location of the post, or its a tag in the post itself
        '''
        try:
            location_tag = self.driver.find_element_by_xpath("//a[@class=\"O4GlU\"]")
        except:
            return self.get_restaurant_from_caption()
        restaurant = location_tag.get_attribute('innerHTML')
        reject_tags = [None, "Home", ""]
        if restaurant not in reject_tags:
            soup = BeautifulSoup(location_tag.get_attribute('outerHTML'), 'lxml')
            page = "https://instagram.com"+soup.find('a')['href']
            return restaurant,page
        else:
            return self.get_restaurant_from_caption()

    def scrape_posts(self, account_name):
        self.go_to_page(account_name)
        first_post = self.driver.find_element_by_xpath("//div[@class=\"_9AhH0\"]")
        first_post.click()
        post_number = 1
        sleep(3)
        last_post = False
        while not last_post:
            try:
                img_link = self.get_post_img_link()
                datetime = self.get_post_datetime()
                caption = self.get_post_caption()
                restaurant,page = self.get_post_restaurant()
                print("{}, {}".format(str(post_number), restaurant))
                self.driver.find_element_by_xpath("//a[@class=\" _65Bje  coreSpriteRightPaginationArrow\"]").click()
                sleep(2)
                post_number += 1
            except Exception as e:
                print(str(e))
                last_post=True
                print("All posts scraped!")
        print("Donezos")

post_scraper=InstaBot()
post_scraper.login('drumprogress', insta_pw())
post_scraper.scrape_posts("breadstixnchill")
