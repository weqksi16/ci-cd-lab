import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)
    driver.get("http://localhost:8000")   # ← заменили
    yield driver
    driver.quit()

def test_page_title(driver):
    assert "Тестовая форма" in driver.title

def test_submit_with_valid_data(driver):
    driver.find_element(By.ID, "name").send_keys("Иван")
    driver.find_element(By.ID, "email").send_keys("ivan@example.com")
    driver.find_element(By.ID, "password").send_keys("123456")
    driver.find_element(By.ID, "submitBtn").click()
    time.sleep(0.5)
    msg = driver.find_element(By.ID, "message").text
    assert "успешно" in msg

def test_submit_with_empty_fields(driver):
    driver.find_element(By.ID, "submitBtn").click()
    # Ждём, пока элемент message станет видимым и получим его текст
    msg_element = WebDriverWait(driver, 3).until(
        EC.visibility_of_element_located((By.ID, "message"))
    )
    assert "Заполните все поля" in msg_element.text

def test_email_field_accepts_input(driver):
    email_input = driver.find_element(By.ID, "email")
    email_input.send_keys("test@test.com")
    assert email_input.get_attribute("value") == "test@test.com"