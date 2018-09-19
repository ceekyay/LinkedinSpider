from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import os.path
import random
"""
Failures: 
2. WebApply.txt and EasyApply.txt are not being updated properly
3. Catch errors such as "company = tag <'a'> not found"
4. Deal with already applied companies
"""
ERRORS = "data/errors.txt"
APPLIED = "data/applied.txt"
IDK = "data/idk.txt"
WEB = "data/webApply.txt"
BIG = "data/big.txt"

links = []
applied = set()
webApply = set()
idk = set()
big = set()
errors = []

userId = "email address"
passKey = "pass"

browser = webdriver.Firefox()


def loadData(filename, arr):
    f = open(filename)
    line = f.readline()
    while line:
        arr.add(line)
        line = f.readline()
    f.close()


def writeData(filename, arr):
    f = open(filename, "w")
    for link in arr:
        f.write(link)
    f.close()


def warmUp():
    loadData(APPLIED, applied)
    loadData(WEB, webApply)
    loadData(IDK, idk)
    loadData(BIG, big)

    f = open("base.txt")
    line = f.readline()
    while line:
        if line not in applied:
            if line not in webApply:
                if line not in idk:
                    if line not in big:
                        links.append(line)
        line = f.readline()
    f.close()


def signin():
    browser.get("https://www.linkedin.com/uas/login?")
    time.sleep(6)
    username = browser.find_element_by_xpath('//*[@id="session_key-login"]')
    password = browser.find_element_by_xpath('//*[@id="session_password-login"]')
    username.send_keys(userId)
    password.send_keys(passKey)
    browser.find_element_by_name("signin").click()


def pause(duration):
    if duration == "long":
        time.sleep(random.randint(8, 13))
    elif duration == "med":
        time.sleep(random.randint(5, 8))
    elif duration == "short":
        time.sleep(random.randint(3, 5))


def getCompany(url):
    try:
        company = browser.find_element_by_xpath('/html/body/div[5]/div[5]/div[2]/div/div[1]/div[1]/div/div[1]/div/div/div[3]/h3')
        company = company.find_element_by_tag_name('a').text
    except NoSuchElementException:
        company = ""
        errors.append(("Company Name Error", url))
    return company


def getLocation(url):
    try:
        location = browser.find_element_by_xpath('/html/body/div[5]/div[5]/div[2]/div/div[1]/div[1]/div/div[1]/div/div/div[3]/h3/span[3]').text
    except NoSuchElementException:
        location = ""
        errors.append(("Job Location Error", url))
    return location


def getTitle(url):
    try:
        title = browser.find_element_by_xpath('/html/body/div[5]/div[5]/div[2]/div/div[1]/div[1]/div/div[1]/div/div/div[3]/h1').text
    except NoSuchElementException:
        title = ""
        errors.append(("Job Title Error", url))
    return title


def getApplyType(url):
    try:
        applyType = browser.find_element_by_xpath(
            '/html/body/div[5]/div[5]/div[2]/div/div[1]/div[1]/div/div[1]/div/div/div[3]/div/div/button/span[2]').text
    except NoSuchElementException:
        applyType = ""
        errors.append(("Apply-Type Error", url))
    return applyType


def getDetails(url):
    try:
        details = browser.find_element_by_xpath('//*[@id="job-details"]').text
    except NoSuchElementException:
        details = ""
        errors.append(("Job Details Error", url))
    return details


def grabData(url):
    data = {}
    browser.get(url)
    pause("long")

    # Click on "See More" to see the full job description
    check = browser.find_element_by_xpath('/html/body/div[5]/div[5]/div[2]/div/div[1]/div[1]/div/div[2]/div/button')
    try:
        seeMore = check.find_element_by_tag_name('span')
        seeMore = browser.find_element_by_xpath('/html/body/div[5]/div[5]/div[2]/div/div[1]/div[1]/div/div[2]/div/button')
    except NoSuchElementException:
        seeMore = browser.find_element_by_xpath('/html/body/div[5]/div[5]/div[2]/div/div[1]/div[1]/div/div[3]/div/button')

    seeMore.click()
    pause("long")

    data['company'] = getCompany(url)
    data['location'] = getLocation(url)
    data['title'] = getTitle(url)
    data['applyType'] = getApplyType(url)
    data['details'] = getDetails(url)

    return data


def criteriaPass(details, url):
    omit = ["C#", "c#", "C++", "c++", ".net", ".NET", "sponsorship", "Sponsorship", "US Citizens"]

    for keyword in omit:
        if keyword in details:
            idk.add(url)
            return False
    return True


def checkCompany(company, url):
    companies = ["IBM", "GE", "GE Digital", "Amazon", "General Electric", "Facebook", "Apple", "LinkedIn", "Google", "Uber"]

    if company in companies:
        big.add(url)
        return True
    return False


def clickEasyApply(url):
    try:
        browser.find_element_by_xpath(
            '/html/body/div[5]/div[5]/div[2]/div/div[1]/div[1]/div/div[1]/div/div/div[3]/div/div/button').click()
    except NoSuchElementException:
        errors.append(("Easy Apply BTN Error", url))


def clickResumeDropdown(url):
    try:
        browser.find_element_by_xpath(
            '/html/body/div[5]/div[6]/div/div[1]/div/div/div/form/div/form/div[1]/div').click()
    except NoSuchElementException:
        errors.append(("EasyApply Resume Dropdown Error", url))


def selectResume(url):
    try:
        browser.find_element_by_xpath(
            '/html/body/div[5]/div[6]/div/div[1]/div/div/div/form/div/form/div[2]/ol[1]/li').click()
    except NoSuchElementException:
        errors.append(("EasyApply Resume Select Error", url))


def clickSubmit(url):
    try:
        browser.find_element_by_xpath(
            '/html/body/div[5]/div[6]/div/div[1]/div/div/div/form/footer/div/button[2]').click()
    except NoSuchElementException:
        errors.append(("EasyApply Submit Error", url))


def dropApp(link):
    pause("short")
    # First click on "Easy Apply"
    clickEasyApply(link)

    pause("short")
    # Click on Resume Drop Down
    clickResumeDropdown(link)

    pause("short")
    # Choose the latest Resume
    selectResume(link)

    pause("short")
    # Click on submit application button
    clickSubmit(link)


def sortApps():
    signin()
    pause("med")

    for link in links:
        data = grabData(link)

        if "Senior" in data['title']:
            pause("short")
            continue

        if data['applyType'] == 'Easy Apply':
            if criteriaPass(data['details'], link):
                if not checkCompany(data['company'], link):
                    dropApp(link)
                    applied.add(link)
        else:
            webApply.add(link)

        pause("long")

    print("#####################")
    print("Applied")
    for app in applied:
        print(app)

    print("#####################")
    print("IDK")
    for a in idk:
        print(a)

    writeData(BIG, big)
    #writeData(ERRORS, errors)
    writeData(WEB, webApply)
    writeData(IDK, idk)
    writeData(APPLIED, applied)

    browser.close()


    print("#####################")
    print("ERRORS")
    for err in errors:
        print(err)


warmUp()
sortApps()
