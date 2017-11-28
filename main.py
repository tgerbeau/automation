
import sys
import library
import config

#from selenium import webdriver
#from selenium.webdriver.common.keys import Keys

driver = library.setUp()

#If any region is given in parameter, default region = dailybuild
if len(sys.argv) == 1:
    region = config.URL_PLATEFORM['default_region']
else:
    region = sys.argv[1] + "/"

driver.get (config.URL_PLATEFORM ['base_url'] + region)
#assert "Plateforme GINCO Dailybuild" in driver.title

library.login(driver)
library.createDataSet(driver, region)
library.checkImport(driver, region)

#library.logout(driver)
library.tearDown(driver)
