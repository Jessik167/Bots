# -*- coding: utf-8 -*-
'''
Created on 19 feb. 2020

@author: Jessy APDIF
'''
import re
import time
import requests
import Vista as v
import Controlador as c
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from verifica_link import separa_titulo, imprime_datos
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from Verifica import veri, separa_titulo, imprime_datos, retorna_dominio
from selenium.webdriver.remote.webelement import WebElement

pag = 1


def extrae_categoria(driver):
    global pag
    next_page = 1
    while next_page:
        print("#################################### Página {} ####################################".format(pag))
        for a in driver.find_elements_by_css_selector('div#blog-entries > article h2 > a'):
            titulo = a.get_attribute('title').replace('(FLAC)', '').replace('(Mp3)', '')
            referer = a.get_attribute('href')
            cantante, album = separa_titulo(titulo, '–')
            time.sleep(2)
            driver.execute_script("window.open(arguments[0]);", referer)
            driver.switch_to.window(driver.window_handles[2])
            ref_inf = extrae_infringing(driver)
            if ref_inf:
                for inf in ref_inf:
                    mega_link = get_mega(inf)
                    if mega_link != False:
                        if mega_link.find('mega') != -1:
                            if c.existe_inf(mega_link) == False:
                                imprime_datos(titulo, fecha, cantante, album, referer, mega_link)
                                c.inserta_item(titulo, cantante, album, referer, mega_link, fecha, id_domin)
                                v.muestra_item_guardado(titulo)
            close_taps(driver, 1)
        try:
            next_page = driver.find_element_by_css_selector('a.next.page-numbers')
            next_page.click()
            pag += 1
        except:
            print('Ocurrió un error al cambiar de página')
            break
    close_taps(driver, 0)
    
    
def extrae_infringing(driver):
    i = 5
    try:
        p = driver.find_element_by_xpath('//div[@class= "entry-content clr"]/p['+str(i)+']')
        try:
            p.find_element_by_css_selector('a > img').get_attribute('src')
        except:
            i = 6
            p = driver.find_element_by_xpath('//div[@class= "entry-content clr"]/p['+str(i)+']')
        p.find_element_by_css_selector('a > img').get_attribute('src')
        ref_inf1 = p.find_element_by_xpath('./a[1]').get_attribute('href')
        ref_inf2 = p.find_element_by_xpath('./a[2]').get_attribute('href')
        #print((ref_inf1,ref_inf2))
        time.sleep(2)
        return ref_inf1, ref_inf2
    except:
        return


def close_taps(driver, i):
    handle = driver.window_handles
    num_taps = len(handle) -1
    while num_taps > i:
        driver.switch_to.window(driver.window_handles[num_taps])
        driver.close()
        num_taps-=1
    driver.switch_to.window(driver.window_handles[i])


def open_page(driver, css):
    b = 0
    while True:
        try:
            driver.find_element_by_css_selector(css).click()
            b = 1
            driver.find_element_by_css_selector(css).click()
            break
        except:
            try:
                element = driver.find_element_by_id('btn-main')
                ActionChains(driver).move_to_element(element).click().perform()
            except:
                break
            #driver.find_element_by_css_selector('body').click()
            if b == 1:
                break


def get_mega(url):
    #####ABRE NAVEGADOR#####
    options = webdriver.ChromeOptions()
    options.add_extension('./extension_AdFly-Skipper.crx')
    options.add_extension('./extension_im_not_a_robot.crx')
    options.add_extension('./Buster_Captcha.crx')
    driver = webdriver.Chrome('C:\\Users\\APDIF\\Desktop\\chromedriver.exe', options=options)
    driver.get(url)
    time.sleep(2)
    try:
        url_check = driver.current_url
    except:
        driver.get(url)
        try:
            url_check = driver.current_url
        except:
            return False
    if re.findall('http[s]?://free.propdfconverter.com/*', url_check):
        driver.quit()
        return False
    elif re.findall('http[s]?://ouo.io/*', url_check):
        try:
            open_page(driver, 'form#form-captcha > div > button')
            driver.switch_to.window(driver.window_handles[0])
            WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'form#form-go > button')))
            open_page(driver, 'form#form-go > button')
            WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'body')))
            mega_inf = driver.current_url
            driver.quit()
            return mega_inf
        except:
            driver.quit()
            return False
    else:
        try:
            WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID,'btn-main'))) ##cambiar 5 por número más grande, cuando haga pruebas con captcha
            time.sleep(3)
            prev_mega = driver.find_element_by_id('btn-main').get_attribute('href')
            driver.execute_script("window.open(arguments[0]);", prev_mega)
            driver.switch_to.window(driver.window_handles[1]) 
            WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'body')))
            mega_inf = driver.current_url
            driver.quit()
            return mega_inf
        except:
            driver.quit()
            return False


def busca_todas_categorias(driver):
    for a in driver.find_elements_by_css_selector('ul.sub-menu > li > a'):
        cate_ref = a.get_attribute('href')
        driver.execute_script("window.open(arguments[0]);", cate_ref)
        driver.switch_to.window(driver.window_handles[1])
        extrae_categoria(driver)
    driver.quit()


def busca_por_categoria(driver, cate_ref):
    driver.execute_script("window.open(arguments[0]);", cate_ref)
    driver.switch_to.window(driver.window_handles[1])
    extrae_categoria(driver)
    driver.quit()
    
    

fecha = date.today().strftime("%d %B, %Y")
url = 'https://www.barboflacmusic.com/'
#####TOMA EL ÚLTIMO ID DE LA TABLA DE DOMINIOS EN LA BD#####
id_domin = retorna_dominio(url)
#####ABRE NAVEGADOR#####
driver = webdriver.Chrome('C:\\Users\\APDIF\\Desktop\\chromedriver.exe')
driver.get(url)
#print(get_mega('https://ouo.io/VlrKab'))
#cate_ref = 'https://www.barboflacmusic.com/category/salsa/page/{}/'.format(pag)
busca_por_categoria(driver,'https://www.barboflacmusic.com/category/vallenato/')