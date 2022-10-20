from ctypes.wintypes import PHANDLE
import pytest

from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys

@pytest.fixture
def browser():
  # Chrome() инициализирует экземпляр ChromeDriver на локальном компьютере, используя параметры по умолчанию. 
  # Возвращаемый объект драйвера привязан к экземпляру ChromeDriver. 
  # Все вызовы WebDriver будут осуществляться через него.
  driver = Chrome()
  # Самая болезненная часть автоматизации тестирования веб-интерфейса — это ожидание загрузки/изменения страницы 
  # после запуска взаимодействия.
  # Странице требуется время для отображения новых элементов. 
  # Если автоматизация попытается получить доступ к новым элементам до того, как они будут созданы,
  # WebDriver создаст файл NoSuchElementException. 
  # Неправильное ожидание — одна из основных причин «ненадежности» веб-тестов пользовательского интерфейса.
  driver.implicitly_wait(10) # Метод  implicitly_wait, описанный выше, говорит драйверу ждать до 10 секунд существования элементов при попытке их найти. 
  # Механизм ожидания умен: вместо того, чтобы заснуть на 10 секунд, он перестанет ждать, как только появится элемент.
  yield driver
  driver.quit()

def test_basic_duckduckgo_search(browser): 
    # Тест объявляет URL-адрес домашней страницы DuckDuckGo 
    # как переменную для удобочитаемости и удобства обслуживания.
    URL = 'https://www.duckduckgo.com' 
    PHRASE = 'panda' 
    browser.get(URL) 
    search_input = browser.find_element_by_id('search_form_input_homepage') 
    search_input.send_keys(PHRASE + Keys.RETURN) 
    link_divs = browser.find_elements_by_css_selector('#links > div') 
    assert len(link_divs) > 0 
    xpath = f"//div[@id='links']//*[содержит(текст(), '{PHRASE}' )]" 
    results = browser.find_elements_by_xpath(xpath) 
    assert len(results) > 0 
    search_input = browser.find_element_by_id('search_form_input') 
    assert search_input.get_attribute('value') == PHRASE
