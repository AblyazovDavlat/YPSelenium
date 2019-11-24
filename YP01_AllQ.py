from selenium import webdriver
from selenium.webdriver.support.select import Select
from collections import defaultdict
import time

PASSED_TEXT = 'test'

browser = webdriver.Chrome('C:\chromedriver')
browser.get('http://test.youplace.net/')


def resolveTextBoxes():
    textBoxes = browser.find_elements_by_xpath("//input[@type='text']")
    for textBox in textBoxes:
        textBox.send_keys(PASSED_TEXT)


def resolveRadioBoxes():
    radioBoxes = browser.find_elements_by_xpath("//input[@type='radio']")
    if (len(radioBoxes) == 0):
        return;

    values = defaultdict(list)
    for radio in radioBoxes:
        values[radio.get_attribute("name")].append(radio.get_attribute("value"))
    for key in values.keys():
        maximum = max(values[key], key=len)

        validRadio = browser.find_element_by_xpath(("//input[@value='" + maximum + "']"))
        validRadio.click()


def resolveSelectBoxes():
    selectBoxes = browser.find_elements_by_tag_name("select")

    if (len(selectBoxes) == 0):
        return;

    for select in selectBoxes:
        lenBoxes = []
        options = select.find_elements_by_tag_name("option")
        for option in options:
            lenBoxes.append(len(option.get_attribute("value")))
        maximum = max(lenBoxes)
        Select(select).select_by_index(lenBoxes.index(maximum))


# -----FirstPage-----
startButton = browser.find_element_by_tag_name("button")
startButton.click()

# -----WhileTestNotPassed-----
while (len(browser.find_elements_by_xpath("//*[contains(text(), 'Test successfully passed')]")) == 0):
    resolveTextBoxes()
    resolveRadioBoxes()
    resolveSelectBoxes()
    submitButton = browser.find_element_by_tag_name("button")
    submitButton.click()

time.sleep(5)
browser.quit()