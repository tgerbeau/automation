# GINCO/SINP Automation Project 

Python + Selenium WebDriver. 

You will find here the code to automate several critical parts of GINCO/SINP web application.

- _library.py_ contains all functions 
- _config.py_ contains urls for platforms, metadata ids, csv files used to run our tests    
- _credentials.py_ will contain credentials we need to set to run our tests      
- _main.py_  

## How to set up:

main steps:

- [ ] Install Python (or check if already installed)
- [ ] Download geckodriver https://github.com/mozilla/geckodriver/releases 
- [ ] Move "geckodriver" into /usr/local/bin 
- [ ] Install Selenium ```pip install selenium```
- [ ] Checkout the "automation" repository 
- [ ] Add your own credentials into _config.py_
- [ ] Add your .csv file into "automation" repository with this name: "dee_test_mnhn.csv"  



You can also find help here http://selenium-python.readthedocs.io/installation.html

## How to run automation:

- [ ] Inside automation repository, type ``` python main.py ``` or ``` python main.py countryname```
 
* If any parameter is given, "dailybuild" will be the default region.  

Please, feel free to share your comments with me. 
Thanks ;)


