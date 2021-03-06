import sys
import library
import config


driver = library.setUp()

# If any region is given in parameter, default region = dailybuild
if len(sys.argv) == 1:
    region = config.URL_PLATFORM['default_region']
else:
    region = sys.argv[1] + "/"

driver.get (config.URL_PLATFORM ['base_url'] + region)

# Choose one metadata which will be used for your data set import
id_metadata = config.ID_METADATA['id2']

# Built url to access all dataset list
url_all_dataset = config.URL_PLATFORM ['base_url'] + region + config.URL_PLATFORM ['all_dataset']
url_my_dataset = config.URL_PLATFORM ['base_url'] + region + config.URL_PLATFORM ['my_dataset']

library.login(driver, region)
# Clean previous import(s) using the same metadata id
library.removeDataSet(driver, url_all_dataset, id_metadata)

# A valid data model is required before creating a new data set
library.createDataSet(driver, region, id_metadata)

# Check that the nblines imported are not null
library.checkImport(driver, url_my_dataset)

# Clean previous import(s) using the same metadata id
library.removeDataSet(driver, url_all_dataset, id_metadata)

library.logout(driver, region)
library.tearDown(driver)
