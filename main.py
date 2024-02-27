import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

os.environ['PATH'] += "C:/web-scraping/chromedriver-win64"

# Create crhome sesion
driver = webdriver.Chrome()
driver.get('https://www.recetasnestle.com.co/recetas')

# Time to wait popUp content
time.sleep(4)
btn_cookies = driver.find_element(By.ID, 'onetrust-accept-btn-handler')
btn_cookies.click()

# Get categories for search recipes
categories_nav = driver.find_elements(
    By.CSS_SELECTOR, 'a.item')


def getTopRecipes():
    result_scrapping = {}

    for category in categories_nav:
        time.sleep(4)
        driver.implicitly_wait(4)
        recipes = []

        driver.add_cookie({'name': 'main_category', 'value': category.text})

        # Click to new page and Changes to new tab context
        category.send_keys(Keys.CONTROL + Keys.RETURN)
        driver.switch_to.window(driver.window_handles[1])

        driver.maximize_window()
        driver.implicitly_wait(10)

        section_top_recipes = driver.find_element(
            By.CLASS_NAME, 'recipeList--numbers')
        title_current_category = section_top_recipes.find_elements(
            By.CSS_SELECTOR, 'a.recipeCard__content')
        button_next = section_top_recipes.find_element(
            By.CSS_SELECTOR, '.recipeList button.glide__arrow--right')

        for top_recipes in title_current_category:
            recipes.append(top_recipes.text)
            button_next.click()

        cookie = driver.get_cookie('main_category')
        main_category = cookie['value']

        result_scrapping[main_category] = recipes
        print(result_scrapping)

        driver.close()
        driver.switch_to.window(driver.window_handles[0])


getTopRecipes()


driver.quit()
