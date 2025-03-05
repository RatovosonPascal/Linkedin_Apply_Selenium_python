from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By


driver = webdriver.Chrome()

def is_popup_open():
    try:
        popup = driver.find_element(By.CLASS_NAME, 'artdeco-modal__content')
        if popup.is_displayed():
            return True
    except NoSuchElementException:
        return False
    return False


