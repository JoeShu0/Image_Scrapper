from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def GetChromeDriver():
    print("正在创建网页实例...")
    #driver = webdriver.Chrome()
    coptions = webdriver.ChromeOptions()
    coptions.add_argument('--ignore-certificate-errors')
    coptions.add_argument('--ignore-ssl-errors')
    coptions.add_argument('--ignore-certificate-errors-spki-list')
    # 忽略 Bluetooth: bluetooth_adapter_winrt.cc:1075 Getting Default Adapter failed. 错误
    #coptions.add_experimental_option('excludeSwitches', ['enable-automation'])
    # 忽略 DevTools listening on ws://127.0.0.1... 提示
    coptions.add_experimental_option('excludeSwitches', ['enable-logging'])
    coptions.page_load_strategy = 'eager'
    """
    debugMode =  input("Debug模式？(y/n),默认为无头模式: ")
    if debugMode != "y":
        coptions.add_argument("--headless")
    """

    #Avoid Detection
    # Adding argument to disable the AutomationControlled flag 
    coptions.add_argument("--disable-blink-features=AutomationControlled")
    # Exclude the collection of enable-automation switches 
    coptions.add_experimental_option("excludeSwitches", ["enable-automation"])
    # Turn-off userAutomationExtension 
    coptions.add_experimental_option("useAutomationExtension", False)

    try:
        driver = webdriver.Chrome(options=coptions)
    except:
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=coptions)

    # Changing the property of the navigator value for webdriver to undefined 
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") 

    return driver

def WaitForElement(driver, method, pattern, timeout = 5):
    elementlogin_present = EC.presence_of_element_located((method, pattern))
    WebDriverWait(driver, timeout).until(elementlogin_present)