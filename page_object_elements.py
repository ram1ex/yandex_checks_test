from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class BasePage:
    
    def __init__(self, driver):
        self.driver = driver
        self.base_url_1 = "https://ya.ru/"
        self.base_url_2 = "https://yandex.ru/search/"
    
    def find_element(self, locator,time=3):
        return WebDriverWait(self.driver,time).until(EC.presence_of_element_located(locator),message=f"Can't find element by locator {locator}")
    
    def go_to_site_ya(self):
        return self.driver.get(self.base_url_1)
    
    def go_to_site_yandex(self):
        return self.driver.get(self.base_url_2)
    
    def get_current_url(self):
        return self.driver.current_url

    def switch_to_the_next_tab(self):
        next_tab = self.driver.window_handles[1]
        return self.driver.switch_to.window(next_tab)
    
    def switch_to_the_prev_tab(self):
        prev_tab = self.driver.window_handles[0]
        return self.driver.switch_to.window(prev_tab)
    
    def get_attribute(self, found_element, attribute_name):
        value = str(found_element.get_attribute(attribute_name))
        return value
    
    def get_name_in_title(self):
        title_category = str(self.driver.title.split(":")[0])
        return title_category

class Locators:
    
    search_field_locator = (By.XPATH, ("//*[@name='text']"))
    suggests_locator = (By.CLASS_NAME, "mini-suggest_open")
    search_result_table = (By.XPATH, ("//*[@id='search-result']"))
    first_element_tensor = (By.XPATH, ("//*[@id='search-result']/li[1]/div/div[1]/div[2]/div[1]/a/b[text()='tensor.ru']"))
    second_element_tensor = (By.XPATH, ("//*[@id='search-result']/li[2]/div/div[1]/div[2]/div[1]/a/b[text()='tensor.ru']"))
    third_element_tensor = (By.XPATH, ("//*[@id='search-result']/li[3]/div/div[1]/div[2]/div[1]/a/b[text()='tensor.ru']"))
    pictures_locator = (By.XPATH, ("/html/body/div[1]/nav/ul/li[2]/div[1]/a/span[text()='Картинки']"))
    first_pic_category_locator = (By.CLASS_NAME, "PopularRequestList-Item_pos_0")
    first_pic_in_list_locator = (By.XPATH, ("/html/body/div[3]/div[2]/div[1]/div[1]/div/div[1]/div/a/img"))
    preview_open_first_pic_in_list_locator = (By.CLASS_NAME, "MMThumbImage-Image")
    origin_open_first_pic_in_list_locator = (By.CLASS_NAME, "MMImage-Origin")
    next_button_locator = (By.CLASS_NAME, "CircleButton_type_next")
    prev_button_locator = (By.CLASS_NAME, "CircleButton_type_prev")
    
class MainOperations(BasePage):
    
    def click_on_search_field(self):
        search_field = self.find_element(Locators.search_field_locator)
        search_field.click()
        return search_field
    
    def type_a_word(self, found_element, word):
        type = found_element.send_keys(word)
        return type
    
    def click_Enter(self, found_element):
        click_enter = found_element.send_keys(Keys.ENTER)
        return click_enter
    
    def click_the_link(self, found_element):
        click_link = found_element.click()
        return click_link
    
    def check_suggests(self):
        suggests = self.find_element(Locators.suggests_locator)
        return suggests
    
    def check_search_result_table(self):
        table_in_place = self.find_element(Locators.search_result_table)
        return table_in_place
    
    def check_search_result_links(self):
        try:
            element_tensor = self.find_element(Locators.first_element_tensor)  # проверяем первый элемент в списке
        except TimeoutException:
            try:
                element_tensor= self.find_element(Locators.second_element_tensor) # иногда первым элементом появляется рекламный блок, проверяем второй..
            except TimeoutException:
                element_tensor = self.find_element(Locators.third_element_tensor) # иногда первые два элемента появляются рекламными блоками, проверяем третий..
        return element_tensor    
    
    def check_pictures_link(self):
        pictures = self.find_element(Locators.pictures_locator)
        return pictures     
    
    def check_first_pic_category(self):
        pic_link = self.find_element(Locators.first_pic_category_locator)
        return pic_link
    
    def check_first_pic_in_the_list(self):
        f_pic_link = self.find_element(Locators.first_pic_in_list_locator)
        return f_pic_link
    
    def check_preview_open_first_pic_in_list(self):
        prev_f_pic_link = self.find_element(Locators.preview_open_first_pic_in_list_locator)
        return prev_f_pic_link
    
    def check_open_picture_link(self):
        orig_f_pic_link = self.find_element(Locators.origin_open_first_pic_in_list_locator)
        return orig_f_pic_link

    def check_next_button_link(self):
        next_pic = self.find_element(Locators.next_button_locator)
        return next_pic  

    def check_prev_button_link(self):
        prev_pic = self.find_element(Locators.prev_button_locator)
        return prev_pic   