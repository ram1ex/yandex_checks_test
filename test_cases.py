import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from page_object_elements import MainOperations

@pytest.fixture(scope="session")
def browser_1():
    service = Service('/path/to/webdriver')
    service.start()
    driver = webdriver.Remote(service.service_url)
    yield driver
    driver.quit()

@pytest.fixture(scope="session")
def browser_2():
    service = Service('/path/to/webdriver')
    service.start()
    driver = webdriver.Remote(service.service_url)
    yield driver
    driver.quit()

def test_yandex_search(browser_1):
    main_ops = MainOperations(browser_1)
    main_ops.go_to_site_ya() # 1)	Зайти на yandex.ru / ya.ru
    time.sleep(2)
    search_field = main_ops.click_on_search_field() # 2)	Проверить наличия поля поиска
    main_ops.type_a_word(search_field,"Тензор") # 3)	Ввести в поиск Тензор
    main_ops.check_suggests() # 4)	Проверить, что появилась таблица с подсказками (suggest) 
    main_ops.click_Enter(search_field) # нажимаем Enter
    main_ops.check_search_result_table() # 5) При нажатии Enter появляется таблица результатов поиска
    tensor_link = main_ops.check_search_result_links() # 6.1) Проверить 1 ссылка является tensor.ru (! первая после рекламных ссылок если такие выводятся в таблице результатов)
    main_ops.click_the_link(tensor_link) # кликаем по данной ссылке
    main_ops.switch_to_the_next_tab() # переключаемся на второй таб
    time.sleep(2)
    assert main_ops.get_current_url() == "https://tensor.ru/" # 6.2) Проверить что эта ссылка ведет на сайт tensor.ru
    main_ops.switch_to_the_prev_tab() # возвращаемся на первый таб        
       
def test_yandex_picures(browser_2):
    main_ops = MainOperations(browser_2)
    main_ops.go_to_site_yandex() # 1)	Зайти на yandex.ru
    time.sleep(2)
    pictures = main_ops.check_pictures_link() # 2)	Проверить, что ссылка «Картинки» присутствует на странице
    main_ops.click_the_link(pictures) # 3)	Кликаем на ссылку
    main_ops.switch_to_the_next_tab() # переключаемся на второй таб
    time.sleep(2)
    assert main_ops.get_current_url() == "https://yandex.ru/images/?from=tabbar" # 4)	Проверить, что перешли на url https://yandex.ru/images/
    pic_category = main_ops.check_first_pic_category() # проверяем что первая категория на месте
    category_name = main_ops.get_attribute(pic_category,'data-grid-text') # берем имя данной категории
    main_ops.click_the_link(pic_category) # 5)	Открыть первую категорию
    time.sleep(2)
    title_category = main_ops.get_name_in_title() # берем имя данной категории из заголовка открытой страницы (что так же отображается в поле поиска)
    assert category_name == title_category # 6)	Проверить, что название категории отображается в поле поиска (*так же в оглавлении страницы)
    first_picture_link = main_ops.check_first_pic_in_the_list() # найти ссылку первой картинки из списка
    first_picture_ID = main_ops.get_attribute(first_picture_link,'src').split("=")[1].split("-")[0] # взять ID первой картинки картинки из списка
    main_ops.click_the_link(first_picture_link) # 7)	Открыть 1 картинку
    preview_open_first_picture_link = main_ops.check_preview_open_first_pic_in_list() # найти ссылку первой картинки из превью списка слева (которая открыта в данный момент)
    preview_open_first_picture_ID = main_ops.get_attribute(preview_open_first_picture_link,'style').split("=")[1].split("-")[0] # взять ID этой картинки
    assert first_picture_ID == preview_open_first_picture_ID # 8)	Проверить, что именно та картинка открылась (то есть та, что была первой в списке и в данный момент выбрана в превью слева)
    orig_open_first_picture_link = main_ops.check_open_picture_link() # найти ссылку оригинала картинки, что открыт в данный момент на экране 
    orig_open_first_picture_ID = main_ops.get_attribute(orig_open_first_picture_link,'src').split("=")[1].split("-")[0] # взять ID этой открытой картинки-оригинала
    next_button_link = main_ops.check_next_button_link() # найти кнопку вперед
    main_ops.click_the_link(next_button_link) # 9)	Нажать кнопку вперед
    time.sleep(2)
    next_open_picture_link = main_ops.check_open_picture_link() # найти ссылку оригинала картинки, что открыт в данный момент на экране 
    next_open_picture_ID = main_ops.get_attribute(next_open_picture_link,'src').split("=")[1].split("-")[0] # взять ID этой открытой картинки
    assert next_open_picture_ID != orig_open_first_picture_ID # 10)	Проверить, что картинка сменилась (ID отличается от предыдущей)
    prev_button_link = main_ops.check_prev_button_link() # найти кнопку назад
    main_ops.click_the_link(prev_button_link) # 11) Нажать назад
    time.sleep(2)
    prev_open_picture_link = main_ops.check_open_picture_link() # найти ссылку оригинала картинки, что открыт в данный момент на экране 
    prev_open_picture_ID = main_ops.get_attribute(prev_open_picture_link,'src').split("=")[1].split("-")[0] # взять ID этой открытой картинки
    assert prev_open_picture_ID == orig_open_first_picture_ID # 12.	Проверить, что картинка осталась из шага 8 (ID совпадают)