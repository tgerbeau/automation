import config
import re
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def login (driver):
    elem = driver.find_element_by_link_text('Connexion')
    elem.click()
    username = driver.find_element_by_name("username")
    password = driver.find_element_by_name("password")
    submit = driver.find_element_by_name("submit")

    username.send_keys(config.USER_CREDENTIALS['username'])
    password.send_keys(config.USER_CREDENTIALS['password'])
    submit.click()

    #TODO: add validation step
    print ('>>login')

def logout (driver):
    url_logout = config.URL_PLATEFORM ['base_url'] + config.URL_PLATEFORM ['region'] + "/user/logout"
    driver.get (url_logout)
    btn_connect = driver.find_element_by_link_text('Connexion')
    print ('>>logout')

def setUp ():
    driver = webdriver.Firefox(executable_path='/home/tgerbeau/Documents/geckodriver')
    return driver

def tearDown (driver):
    driver.close()

def screenshot (driver):
    driver.save_screenshot('/home/tgerbeau/Documents/screenshot.png')

def createDataSet (driver, region) :
    #page1
    url_create_dataset = config.URL_PLATEFORM ['base_url'] + region + config.URL_PLATEFORM ['create_dataset']
    driver.get (url_create_dataset)
    meta = driver.find_element_by_id("ginco_jdd_metadata_id")
    meta.send_keys(config.ID_METADONNEES['id3'])
    submit = driver.find_element_by_id("ginco_jdd_submit")
    submit.click()

    #page2
    submit = driver.find_element_by_id("ginco_data_submission_submit")
    submit.click()

    #page3
    #Uploading the test ".csv" file
    upload = driver.find_element_by_id("upload_data_file_observation")
    #relatif path from current working directory
    cwd= os.getcwd()
    upload.send_keys(cwd + config.CSV_FILENAME ['csv_filename'])

    srid = driver.find_element_by_id("upload_data_SRID")
    srid.send_keys(config.SRID['wgs84'])

    submit = driver.find_element_by_id("upload_data_submit")
    submit.click()

def checkImport (driver, region) :
    url_all_dataset = config.URL_PLATEFORM ['base_url'] + region + config.URL_PLATEFORM ['all_dataset']
    driver.get (url_all_dataset)
    content = driver.find_element_by_class_name('submission-line-lines')
    text= str (content.text)
    #remove parenthesis
    s = re.sub(r'[^\w\s.]',"", text)
    if int (s) == 0:
        assert ("Import dataset has failed. 0 line imported.")
