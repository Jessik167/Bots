# -*- coding: utf-8 -*-
'''
Created on 15 ene. 2020

@author: Jessy APDIF
'''
import time
import requests
import Vista as v
import Controlador as c
from datetime import date
from selenium import webdriver
from urllib.parse import unquote
from Verifica import veri, separa_titulo, imprime_datos, retorna_dominio


#####LIMPIA EL REFERER Y RETORNA EL INFRINGING#####
def get_inf2(href):
    inf2 = href.split('dest=')
    inf2 = inf2[1].split('%3Fusp')
    inf2 = unquote(inf2[0])
    return inf2


#####VARIABLES GLOBALES#####
SCROLL_PAUSE_TIME = 0.5
url = 'https://lazonadelraro.blogspot.com/'

id_domin = retorna_dominio(url)

#####ABRE EL URL EN EL NAVEGADOR#####
driver = webdriver.Chrome('C:\\Users\\APDIF\\Desktop\\chromedriver.exe')
driver.get(url)
time.sleep(1)

#####BAJA EL SCROLL HASTA EL FINAL DE LA PÁGINA#####
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

#####TOMA LOS REFERERS DE CADA CANCIÓN#####
for a in driver.find_elements_by_css_selector('h3.title.entry-title > a'):
    Bandera = False
    #####TOMA REFERER#####
    referer = a.get_attribute('href')
    #####ABRE EL LINK QUE CONTIENE CADA TÍTULO EN UNA PESTAÑA NUEVA#####
    driver.execute_script("window.open(arguments[0]);", referer)
    #####CAMBIA DE PESTAÑA#####
    driver.switch_to.window(driver.window_handles[1])
    #####VERIFICA QUE EL LINK DE LA PÁGINA ESTÉ ARRIBA#####
    r = requests.get(referer)
    if r.status_code == 200:
        time.sleep(5)
        #####TOMA LOS DATOS#####
        Titulo = driver.find_element_by_css_selector('h1.title.entry-title > a').text
        Titulo = Titulo.replace("'",'').replace('"','')
        Cantante, Album = separa_titulo(Titulo,'–')
        Fecha = driver.find_element_by_css_selector('abbr.time.published').text
        try:
            infringing = driver.find_element_by_css_selector("div.MsoNormal span > a").text
        except:
            try:
                infringing = driver.find_element_by_xpath("//*[contains(text(),'http://j.gs/')]").text
            except:
                infringing = driver.find_element_by_xpath("//*[contains(text(),'https://drive.google.com')]").text
                Bandera = True
        r = requests.get(infringing)
        #####VERIFICA QUE EL INFRINGING NO SE ENCUENTRE EN LA BD#####
        if c.existe_inf(infringing) == False:
            #####VERIFICA QUE EL LINK SEA UN INFRACTOR VÁLIDO#####
            if veri(infringing) == True:
                #####IMPRIME LOS DATOS#####
                print((Titulo,Cantante,Album,infringing,Fecha))
                c.inserta_item(Titulo, Cantante, Album, referer, infringing, Fecha, id_domin)
                v.muestra_item_guardado(Titulo)
        driver.get(infringing)
        time.sleep(8)
        
        #####TOMA EL INFRACTOR 2 DE GOOGLE DRIVE#####
        if Bandera == False:
            try:
                href = driver.find_element_by_id('skip_bu2tton').get_attribute('href')
                #####LIMPIA EL REFERER#####
                infringing2 = get_inf2(href)
                #####VERIFICA QUE EL INFRINGING NO SE ENCUENTRE EN LA BD#####
                if c.existe_inf(infringing2) == False:
                    #####VERIFICA QUE EL LINK SEA UN INFRACTOR VÁLIDO#####
                    if veri(infringing2) == True:
                        #####IMPRIME LOS DATOS#####
                        print((Titulo,Cantante,Album,infringing2,Fecha))
                        c.inserta_item(Titulo, Cantante, Album, referer, infringing2, Fecha, id_domin)
                        v.muestra_item_guardado(Titulo)
            except:
                pass
    #####CAMBIA A LA PÁGINA PRINCIPAL#####
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    #break
#####CIERRA EL NAVEGADOR#####
driver.quit()