from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import os.path
import random
from spider import LinkedinCrawler

def main():
    spider = LinkedinCrawler()
    spider.crawl()


main()