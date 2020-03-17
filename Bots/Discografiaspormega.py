# -*- coding: utf-8 -*-
'''
Created on 10 mar. 2020

@author: Jessy APDIF
'''
import time
import scrapy
from datetime import date
from selenium import webdriver
from scrapy.http import Request
from Verifica import separa_titulo, imprime_datos, retorna_dominio, Inserta_Datos


class discografiaspormega(scrapy.Spider):
    name = 'discografiaspormega'
    _num_pagina = 1
    id_domin = 0
    start_urls = ['https://www.discografiaspormega.com/']
    # RETORNA EL �LTIMO DOMINIO
    id_domin = retorna_dominio(start_urls[0])
    
    
    def parse(self, response):
        print('##### PÁGINA #{} #####'.format(self._num_pagina))
        #####RECORRE "ARTICLES"#####
        for art in response.css('div#content article'):
            referer = art.css('a ::attr(href)').get()
            #print(referer)
            yield Request(referer, meta= {'referer': referer},callback=self.parse_attr)
            
        next_page = response.css('a.next.page-numbers ::attr(href)').get()
        if next_page:
            self._num_pagina += 1   
            yield response.follow(next_page, callback= self.parse)
            
                  
    def parse_attr(self, response):
        #print(response.text)
        i = 0
        Titulos = []
        Fecha = date.today().strftime("%d %B, %Y")
        driver = webdriver.Chrome('C:\\Users\\APDIF\\Desktop\\chromedriver.exe')
        driver.get(response.url)
        for str in driver.find_elements_by_xpath('//p/strong'):
            i += 1
            if i % 2 != 0:
                Titulos.append(str.text)
                #print(str.text)
            else:
                continue
        i = 0
        tam = len(Titulos)
        for a in driver.find_elements_by_css_selector('p > a'):
            #print(i)
            if i == 0:
                i += 1
                continue
            if i == tam:
                break
            inf = a.get_attribute('href')
            driver.execute_script("window.open(arguments[0]);", inf)
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(1)
            Infringing_mega = driver.current_url
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            Titulo = self.Limpia_titulo(Titulos[i])
            Cantante, Album = separa_titulo(Titulo, '–')
            imprime_datos(Titulo,'', Cantante, Album, response.url, Infringing_mega)
            # INGRESA INFRINGING A LA BD LOS DATOS
            Inserta_Datos(Titulo, Cantante, Album, response.url, Infringing_mega, Fecha, self.id_domin)
            i += 1
        driver.quit()

                    
    def Limpia_titulo(self,Titulo):
        Titulo = Titulo.replace('Descargar','').replace('MEGA','')
        Titulo = Titulo.split('[')[0]
        return Titulo