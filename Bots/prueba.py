# -*- coding: utf-8 -*-
'''
Created on 12 mar. 2020

@author: APDIF
'''
import time
from selenium import webdriver

def userCloud(Inf):
        driver = webdriver.Chrome('C:\\Users\\APDIF\\Desktop\\chromedriver.exe')
        driver.get(Inf)
        time.sleep(2)
        try:
            element = driver.find_element_by_css_selector("button.btn.btn-inverse.btn-icon-stacked")
            driver.execute_script("arguments[0].click();", element)
        except:
            pass
        time.sleep(2)
        element = driver.find_element_by_css_selector("button#btn_download")
        driver.execute_script("arguments[0].click();", element)
        time.sleep(1)
        sel = driver.execute_script("return document.getElementsByClassName('ribbon-heading ribbon-default top-left-right')[0].innerHTML;")#, element)#.get_attribute('href')
        Infringing = get_atr(sel)
        #print(Infringing)
        driver.quit()
        return Infringing

def get_atr(texto):
        if texto:
            texto = texto.split('onclick')[0]
            texto = texto.split('=')[1].replace('"','')
        return texto

print(userCloud('https://userscloud.com/65ycpn27215g'))