from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import os.path
import random


class LinkedinCrawler(object):

    def __init__(self):
        self.userId = "E-mail"
        self.passKey = "password"
        self.browser = webdriver.Firefox()
        self.links = []

    def loadLinks(self):
        f = open('base.txt')
        line = f.readline()
        while line:
            self.links.append(line)
            line = f.readline()
        f.close()

    @staticmethod
    def rand():
        return random.randint(6, 11)

    def seeMoreJobs(self):

        for i in range(0, 9):
            time.sleep(random.randint(0, 5))
            try:
                self.browser.find_element_by_xpath('/html/body/div[5]/div[5]/div[2]/div/section/div[3]/div/div/div[2]/button').click()
                time.sleep(random.randint(0, 5))
                self.browser.execute_script("window.scrollTo(0, 500)")
            except NoSuchElementException:
                break

    def addJobLinks(self, parentList):

        f = open("base.txt", "w")

        for link in parentList:
            url = link.get_attribute("href")
            if url.startswith('https://www.linkedin.com/jobs/view/'):
                url = url[:45]
                if url not in self.links:
                    self.links.append(url)
                    f.write(url)
                    f.write("\n")
        f.close()

    def crawl(self):

        self.browser.get("https://www.linkedin.com/uas/login?")

        time.sleep(self.rand())

        username = self.browser.find_element_by_xpath('//*[@id="session_key-login"]')
        password = self.browser.find_element_by_xpath('//*[@id="session_password-login"]')
        username.send_keys(self.userId)
        password.send_keys(self.passKey)
        self.browser.find_element_by_name("signin").click()

        time.sleep(self.rand())

        self.browser.get("https://www.linkedin.com/jobs")

        time.sleep(self.rand())

        # Scroll Down the page (Behave like human)
        self.browser.execute_script("window.scrollTo(0, 1080)")

        # Selenium will click on the "See more Jobs" button 9 times. So we now have links to 200 jobs.
        self.seeMoreJobs()

        # These are all the job cards, arranged as a list.
        parentLinks = self.browser.find_elements_by_tag_name('li a')

        # Lets extract all the links from the parentLinks
        self.addJobLinks(parentLinks)

        self.browser.close()
