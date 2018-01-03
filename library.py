import config
import credentials
import re
import os
import logging as log

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


def login (driver, region):
    elem = driver.find_element_by_link_text('Connexion')
    elem.click()
    username = driver.find_element_by_name("username")
    password = driver.find_element_by_name("password")
    submit = driver.find_element_by_name("submit")

    username.send_keys(credentials.USER_CREDENTIALS['username'])
    password.send_keys(credentials.USER_CREDENTIALS['password'])
    submit.click()

    #wait = WebDriverWait(driver, 5)
    #wait.until(EC.url_changes(config.URL_PLATFORM ['base_url'] + region))

    # Check if we are connected to the app
    try:
        driver.get (config.URL_PLATFORM ['base_url'] + region + config.URL_PLATFORM ['user'])
        element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//H1[text()='Votre compte']")))
    except:
        print ("Element h1 not found")
        driver.quit()


def logout (driver, region):
    url_logout = config.URL_PLATFORM ['base_url'] + region + "/user/logout"
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

    # Select one data model to run your test
    # Note that the name can be different from one platfrom to another
    model = Select (driver.find_element_by_id("ginco_jdd_model"))
    model.select_by_visible_text(config.DATAMODEL_NAME ['data_model_name'])


    meta = driver.find_element_by_id("ginco_jdd_metadata_id")
    meta.send_keys(id_metadata)
    submit = driver.find_element_by_id("ginco_jdd_submit")
    submit.click()

    # page2
    model = Select (driver.find_element_by_id("ginco_data_submission_dataset"))
    model.select_by_visible_text(config.DATAMODEL_NAME ['data_submission_dataset'])
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

    # Explicit wait until page jdd is loaded
    wait = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'submission-line-lines')))

def checkImport (driver, url_my_dataset) :
    log.info(">> checkImport ()")

    # span.glyphicon.glyphicon-ok.color-success
    # glyphicon glyphicon-play
    # wait = WebDriverWait(driver, 20).until(
    # EC.presence_of_element_located((By.CLASS_NAME, 'a.btn.btn-xs.btn-success')))
    # "//*[@id=\"jddTable\"]/tbody/tr[" + str(i) + "]/td[1]/button/span"
    # publish = driver.find_element_by_xpath('//*[@id="jddTable"]/tbody/tr/td[4]/div/div/a[1]')

    # Wait until the tick icon is displayed
    wait = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="jddTable"]/tbody/tr/td[6]/div/div[3]/span')))

    # find the publish button
    publish = driver.find_element_by_xpath('//*[@id="jddTable"]/tbody/tr/td[4]/div/div/a[1]')
    # publish.click()

    lines_imported = driver.find_element_by_class_name('submission-line-lines')
    text= str (lines_imported.text)

    # Remove parenthesis from string
    s = re.sub(r'[^\w\s.]',"", text)
    if int (s) == 0:
         log.error (">> Import dataset has failed. 0 line imported.")

def removeSubmission (driver, submission_array) :
    for submission_link in submission_array:
        print submission_link
        driver.get (submission_link)

def removeEntireDataSet (driver, id_metadata) :

    # TO DO : //*[@id="jddTable"]/tbody/tr[1]/td[9]/div/div/a[3]/span
    # Check if DEE transmission is not made before process cleaning
    log.info(">> removeEntireDataSet")
    str_xpath_remove = ""
    elements = driver.find_elements_by_css_selector("span.text-muted.longtext")
    i=1
    for ii in elements:
        print (ii.text)
        # Check if id_metadata is on the list of elements
        if (id_metadata == ii.text):
            str_xpath_remove = "//*[@id=\"jddTable\"]/tbody/tr[" + str(i) + "]/td[1]/button/span"

        i = i+1

    if str_xpath_remove != "":
        btn_cancel_submission = driver.find_element_by_xpath(str_xpath_remove)
        btn_cancel_submission.click()
        # Catch the popup alert, click on "Continuer" button
        wait = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Continuer")))
        btn_continuer = driver.find_element_by_link_text('Continuer')
        btn_continuer.click()

def removeDataSet (driver, url_all_dataset , id_metadata) :
    # Go on jdd/all page
    driver.get (url_all_dataset)
    try:
        # Get all the metadata elements in page
        elements = driver.find_elements_by_css_selector("span.text-muted.longtext")
        i=1
        # Submission link(s) tab
        urlToClean = []
        # Index
        #tabIndex = []
        for ii in elements:
            # Check if id_metadata is on the list of elements
            if (id_metadata == ii.text):
                # matching imports are set in tab
                try:
                    # //*[@id="jddTable"]/tbody/tr/td[4]/div[1]/div
                    str_xpath = "//*[@id=\"jddTable\"]/tbody/tr[" + str (i) + "]/td[5]/div/div/a[2]"
                    tab = driver.find_elements_by_xpath(str_xpath)
                    #tabIndex.append (int (i))
                    for z in tab:
                        urlToClean.append (z.get_attribute("href"))
                except:
                    pass
            i = i +1
    except:
         print (">> No previous import(s) to clean")

    # Clean all submissionLinks collected
    removeSubmission (driver, urlToClean)
    # Clean the general data set (main delete button)
    removeEntireDataSet (driver, id_metadata)
