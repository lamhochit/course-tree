import time
import pathlib
import pandas as pd
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from textwrap import wrap
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.service import Service


class CourseCrawler():
    def __init__(self):
        self.service = Service(os.path.join(pathlib.Path.cwd(), 'chromedriver'))
        self.service.start()
        print('starting service...')
        self.driver = webdriver.Remote(self.service.service_url)

    def quit_crawler(self):
        self.driver.quit()

    def run(self):
        course_info = {}
        self.driver.get('https://w5.ab.ust.hk/wcq/cgi-bin/2010/');
        depts = wrap(self.driver.find_elements_by_xpath('/html/body/div[2]/div[2]')[0].text, 4)
        print('departments: ', depts)
        for dept in depts:
            print('processing %s...' % dept)
            self.driver.get('https://w5.ab.ust.hk/wcq/cgi-bin/2010/subject/%s' % dept);
            courses = self.driver.find_elements_by_id('classes')[0].find_elements_by_class_name("course")
            for course in courses:
                name = course.find_elements_by_tag_name('h2')[0].text
                course = course.find_elements_by_class_name("courseinfo")[0]
                table = course.find_element_by_css_selector('div.courseattr.popup').find_element_by_class_name('popupdetail').find_elements_by_tag_name('table')[0]
                rows = table.find_elements_by_tag_name('tr')
                record = {}
                for row in rows:
                    try:
                        index = row.find_element_by_tag_name('th').get_attribute('innerHTML')
                        element = row.find_element_by_tag_name('td').get_attribute('innerHTML')
                        record[index] = element
                    except:
                        pass
                course_info[name] = record
        return course_info


if __name__ == '__main__':
    cc = CourseCrawler()
    x = cc.run()
