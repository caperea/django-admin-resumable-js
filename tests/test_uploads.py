from .models import Foo

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pytest
import time


def create_test_file(file_path, size_in_megabytes):
    with open(file_path, 'wb') as bigfile:
        bigfile.seek(size_in_megabytes * 1024 * 1024)
        bigfile.write(b'0')


@pytest.mark.django_db
def test_file_uploads(admin_user, live_server, driver):

    test_file_path = "/tmp/test_small_file.bin"
    create_test_file(test_file_path, 5)

    driver.get(live_server.url + '/admin/')
    driver.find_element_by_id('id_username').send_keys("admin")
    driver.find_element_by_id("id_password").send_keys("password")
    driver.find_element_by_xpath('//input[@value="Log in"]').click()

    driver.implicitly_wait(2)
    driver.get(live_server.url + '/admin/tests/foo/add/')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "id_bar")))
    driver.find_element_by_id("id_bar").send_keys("bat")

    driver.find_element_by_css_selector(
        'input[type="file"]').send_keys(test_file_path)

    status_text = driver.find_element_by_id("id_foo_uploaded_status").text
    i = 0
    while i < 5:
        if "Uploaded" in status_text:
            return  # success
        time.sleep(1)
        i += 1
    raise Exception  # something went wrong
