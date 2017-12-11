import config
import credentials
import re
import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def login (driver, region):
    elem = driver.find_element_by_link_text('Connexion')
    elem.click()
    username = driver.find_element_by_name("username")
    password = driver.find_element_by_name("password")
    submit = driver.find_element_by_name("submit")

    username.send_keys(credentials.USER_CREDENTIALS['username'])
    password.send_keys(credentials.USER_CREDENTIALS['password'])
    submit.click()

    # Check if we are connected to the app
    driver.get (config.URL_PLATFORM ['base_url'] + region + config.URL_PLATFORM ['user'])
    title = driver.find_element_by_xpath("//H1[text()='Votre compte']")
    assert (title)


def logout (driver):
    url_logout = config.URL_PLATFORM ['base_url'] + config.URL_PLATFORM ['region'] + "/user/logout"

    driver.get (url_logout)
    btn_connect = driver.find_element_by_link_text('Connexion')
    print ('>>logout')

def setUp ():
    driver = webdriver.Firefox()
    return driver

def tearDown (driver):
    driver.close()

def screenshot (driver):
    driver.save_screenshot('/screenshot.png')

def createDataSet (driver, region, id_metadata) :
    # page1
    url_create_dataset = config.URL_PLATFORM ['base_url'] + region + config.URL_PLATFORM ['create_dataset']

    driver.get (url_create_dataset)
    meta = driver.find_element_by_id("ginco_jdd_metadata_id")
    meta.send_keys(id_metadata)
    submit = driver.find_element_by_id("ginco_jdd_submit")
    submit.click()

    # page2
    submit = driver.find_element_by_id("ginco_data_submission_submit")
    submit.click()

    # page3
    # Uploading the test ".csv" file
    upload = driver.find_element_by_id("upload_data_file_observation")
    # Get the relative path from current working directory
    cwd= os.getcwd()
    upload.send_keys(cwd + config.CSV_FILENAME ['csv_filename'])

    srid = driver.find_element_by_id("upload_data_SRID")
    srid.send_keys(config.SRID['wgs84'])

    submit = driver.find_element_by_id("upload_data_submit")
    submit.click()

def checkImport (driver, url_all_dataset) :

    driver.get (url_all_dataset)
    content = driver.find_element_by_class_name('submission-line-lines')
    text= str (content.text)
    # Remove parenthesis from string
    s = re.sub(r'[^\w\s.]',"", text)
    if int (s) == 0:
        assert ("Import dataset has failed. 0 line imported.")

def removeDataSet (driver, url_all_dataset , id_metadata) :
    # Go on jdd/all page
    driver.get (url_all_dataset)
    driver.get (url_all_dataset)

    # Use searching bar with given id_metadata
    search = driver.find_element_by_css_selector('input.form-control')
    search.send_keys(id_metadata)

    # Get all the metadata elements in page
    elements = driver.find_elements_by_css_selector("span.text-muted.longtext")
    # //*[@id="integration-cancel-link-131"]/span
    # //*[@id="jddTable"]/tbody/tr[1]
    # Check if id_metadata is on the list of elements
    for ii in elements:
        print (ii.text)
        if (id_metadata == ii.text):
            print ("Same metadata found")
            # Clean all imports
            empty_imports = False
