import config

def login (driver):
    elem = driver.find_element_by_link_text('Connexion')
    elem.click()
    username = driver.find_element_by_name("username")
    password = driver.find_element_by_name("password")
    submit = driver.find_element_by_name("submit")

    username.send_keys(config.USER_CREDENTIALS['username'])
    password.send_keys(config.USER_CREDENTIALS['password'])
    submit.click()

def logout (driver):
    #elem = driver.find_element_by_link_text('Connexion')
    #assert elem is null
    url_logout = config.URL_PLATEFORM ['base_url'] + config.URL_PLATEFORM ['region'] + "/user/logout"
    #logout_link = driver.find_element_by_xpath('//a[contains(@href, "%s")]' % href_logout)
    #logout_link.click()
    assert (driver.find_element_by_link_text('Connexion')) not in driver.page_source
    driver.save_screenshot('/home/tgerbeau/Documents/screen_fail.png')
    driver.get (url_logout)
