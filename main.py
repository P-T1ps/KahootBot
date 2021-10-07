import threading
import time

from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common import keys
import math
import sys

code = 0
name = ''
number_of_bots = 0
number_of_threads = 0
try:
    pin = int(sys.argv[1])
    name = str(sys.argv[2])
    number_of_bots = int(sys.argv[3])
    number_of_threads = int(sys.argv[4])
except (IndexError, TypeError):
    print(f"Usage: \n python {sys.argv[0]} <pin> <name> <number of bots> <number of threads>")
    exit()

number_bot = 0


def new_thread(goal):
    global number_bot
    if True:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument("--log-level=3")

        driver = webdriver.Chrome(options=options)
    driver.get("http://kahoot.it")
    for _ in range(goal):
        number_bot += 1
        name_ = name + str(number_bot)
        for _ in range(50):
            try:
                pin_input = driver.find_element_by_xpath('//*[@id="game-input"]')
                pin_input.send_keys(pin)
                pin_input.send_keys(keys.Keys.ENTER)
                break
            except (exceptions.NoSuchElementException, exceptions.StaleElementReferenceException, AttributeError):
                print("-1")
                time.sleep(0.5)
                pass

        for _ in range(50):
            try:
                nick_input = driver.find_element_by_xpath('//*[@id="nickname"]')
                nick_input.send_keys(name_)
                nick_input.send_keys(keys.Keys.ENTER)
                break
            except (exceptions.NoSuchElementException, exceptions.StaleElementReferenceException, AttributeError):
                print("-2")
                time.sleep(0.02)
                pass
        else:
            for _ in range(50):
                try:
                    nick_input = driver.find_element_by_xpath('//*[@id="root"]/div[1]/div/div[3]/div/div/div[2]/button')
                    nick_input.click()
                    time.sleep(0.5)
                    break
                except (exceptions.NoSuchElementException, exceptions.StaleElementReferenceException, AttributeError):
                    time.sleep(0.5)
                    pass
            for _ in range(50):
                try:
                    time.sleep(1)
                    nick_ok = driver.find_element_by_xpath('//*[@id="root"]/div[1]/div/div[3]/div/div/div[2]/button[2]')
                    nick_ok.click()
                    print("Good")
                    break
                except (exceptions.NoSuchElementException, exceptions.StaleElementReferenceException, AttributeError):
                    print("-2")
                    time.sleep(0.5)
                    pass
        print("+1 <3")
        driver.execute_script("window.open('https://kahoot.it', '_blank');")
        window_name = driver.window_handles[-1]
        driver.switch_to.window(window_name=window_name)
    while True:
        if kill:
            driver.quit()
            break


per_thread = math.ceil(number_of_bots/number_of_threads)
kill = False

for i in range(number_of_threads):
    thread = threading.Thread(target=new_thread, args=[per_thread])
    thread.daemon = True
    thread.start()
    time.sleep(1)


input()
kill = True
