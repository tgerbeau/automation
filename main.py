
import library

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox(executable_path='/home/tgerbeau/Documents/geckodriver')
driver.get("https://ginco.naturefrance.fr/dailybuild")

assert "Plateforme GINCO Dailybuild" in driver.title

library.login(driver)
library.logout(driver)
driver.close()
