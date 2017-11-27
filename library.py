import config
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def login (driver):
    print ('>>login')
    elem = driver.find_element_by_link_text('Connexion')
    elem.click()
    username = driver.find_element_by_name("username")
    password = driver.find_element_by_name("password")
    submit = driver.find_element_by_name("submit")

    username.send_keys(config.USER_CREDENTIALS['username'])
    password.send_keys(config.USER_CREDENTIALS['password'])
    submit.click()

def logout (driver):
    print ('>>logout')
    url_logout = config.URL_PLATEFORM ['base_url'] + config.URL_PLATEFORM ['region'] + "/user/logout"
    driver.get (url_logout)
    btn_connect = driver.find_element_by_link_text('Connexion')

def setUp ():
    driver = webdriver.Firefox(executable_path='/home/tgerbeau/Documents/geckodriver')
    return driver

def tearDown (driver):
    driver.close()

def screenshot (driver):
    driver.save_screenshot('/home/tgerbeau/Documents/screenshot.png')

def createDataSet (driver, region) :
    url_create_dataset = config.URL_PLATEFORM ['base_url'] + region
    driver.get (url_create_dataset) 
    meta = driver.find_element_by_name("ginco_jdd[metadata_id]")
    meta.send_keys(config.ID_METADONNEES['id'])
