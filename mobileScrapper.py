import json
import time
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
import unittest
from appium.options.android import UiAutomator2Options


capabilities = dict(
        platformName='Android',
        automationName='UiAutomator2',
        deviceName='Google_Pixel_2',
        language='en',
        locale='US'
    )
appium_server_url  = 'http://localhost:4723/wd/hub'
capabilities_options = UiAutomator2Options().load_capabilities(capabilities)
bot_info_dict = []
metrics = []

class TestAppium(unittest .TestCase):
    def setUp(self) -> None:
        self.driver = webdriver.Remote(command_executor=appium_server_url,options=capabilities_options)

    def tearDown(self) -> None:
        if self.driver:
            self.driver.quit()

    def test_find_battery(self) -> None:  
        
        def search_bot_monthly_users_info(bot_info_dict):
            self.driver.implicitly_wait(5)
            el = self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@text="Search"]').send_keys(bot_info_dict['bot_link'])

            self.driver.implicitly_wait(5)
            el = self.driver.find_element(by=AppiumBy.XPATH, value="//android.view.ViewGroup[contains(@text,'"+bot_info_dict['bot_name']+"')]")

            el.click()
            self.driver.implicitly_wait(5)
            el = self.driver.find_element(by=AppiumBy.XPATH, value="//android.widget.TextView[contains(@text,'monthly users')]")
            monthly_users_string = el.text
            monthly_users_number = monthly_users_string.replace(' monthly users', '')
            monthly_users = int(monthly_users_number.replace(',', ''))
            self.driver.implicitly_wait(5)


            el = self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.ImageView[@content-desc="Go back"]')
            el.click()
            self.driver.implicitly_wait(5)

            # Go back если не вернулся к списку чатов
            try:
                el = self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.ImageView[@content-desc="Go back"]')
                el.click()
                self.driver.implicitly_wait(5)
            except:
                pass

            el = self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.ImageButton[@content-desc="Search"]')
            el.click()

            return monthly_users

        # запуск тг 
        el = self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.TextView[@text="Telegram"]')
        el.click()
        # клик по строке поиска
        self.driver.implicitly_wait(5)
        el = self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.ImageButton[@content-desc="Search"]')
        el.click()

        # прочесть json с сылками на ботов
        with open(r"json\trending.json", 'r', encoding='utf-8') as file:
            json_data = json.load(file)
            for item in json_data:  
                bot_info_dict.append({
                'bot_link': item['bot_link'],
                'bot_name': item['bot_name'],
                })

        for bot_info in bot_info_dict:
            monthly_users = search_bot_monthly_users_info(bot_info)
            bot_name = bot_info['bot_name']
            metrics.append({
                'bot_name': bot_name,
                'bot_monthly_users': monthly_users,
                })

        t = time.localtime()
        current_time = time.strftime("%H.%M_%d.%m.%y", t)

        with open(r"json\metrics\metrics "+current_time+".json", 'w', encoding='utf-8') as file:
            json.dump(metrics, file, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    unittest.main()