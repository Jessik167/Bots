# -*- coding: utf-8 -*-
'''
Created on 11 mar. 2020

@author: Jessy APDIF
'''
import time
import scrapy
from datetime import date
from selenium import webdriver
from scrapy.http import Request
from Verifica import imprime_datos, retorna_dominio, Get_megaLink, Inserta_Datos, separa_titulo, strip_accents


class playcorridos(scrapy.Spider):
    name = 'playcorridos'
    _num_pagina = 1
    id_domin = 0
    Fecha = date.today().strftime("%d %B, %Y")
    start_urls = ['http://playcorridos.com/']
    # RETORNA EL �LTIMO DOMINIO
    id_domin = retorna_dominio(start_urls[0])
    
    
    def parse(self, response):
        print('##### PÁGINA #{} #####'.format(self._num_pagina))
        #####RECORRE "ARTICLES"#####
        for art in response.css('article.item-list'):
            Titulo = art.css('h2 > a ::text').get()
            Titulo = self.Limpia_titulo(Titulo)
            Cantante, Album = separa_titulo(Titulo, '–')
            Titulo, Cantante, Album = self.acentos(Titulo, Cantante, Album)
            referer = art.css('h2 > a ::attr(href)').get()
            for a in art.css('p > a'):
                try:
                    Inf = a.css('::attr(href)').get()
                    if Inf.find('zippyshare') != -1:
                        Infringing = self.zippy(Inf)
                        imprime_datos(Titulo,'', Cantante, Album, referer, Infringing)
                        # INGRESA INFRINGING A LA BD LOS DATOS
                        Inserta_Datos(Titulo, Cantante, Album, referer, Infringing, self.Fecha, self.id_domin)
                    elif Inf.find('mediafire') != -1:
                        yield Request(Inf, meta={'Titulo': Titulo, 'Cantante': Cantante, 'Album': Album, 'Referer': referer} ,callback=self.mediaFire)
                    elif Inf.find('userscloud') != -1:
                        Infringing = self.userCloud(Inf)
                        imprime_datos(Titulo,'', Cantante, Album, referer, Infringing)
                        # INGRESA INFRINGING A LA BD LOS DATOS
                        Inserta_Datos(Titulo, Cantante, Album, referer, Infringing, self.Fecha, self.id_domin)
                except:
                    continue
            #break
            
        next_page = response.css('span#tie-next-page > a ::attr(href)').get()
        if next_page:
            self._num_pagina += 1   
            yield response.follow(next_page, callback= self.parse)
            
        
    def userCloud(self, Inf):
        driver = webdriver.Chrome('C:\\Users\\APDIF\\Desktop\\chromedriver.exe')
        driver.get(Inf)
        time.sleep(2)
        try:
            element = driver.find_element_by_css_selector("button.btn.btn-inverse.btn-icon-stacked")
            driver.execute_script("arguments[0].click();", element)
        except:
            pass
        time.sleep(3)
        element = driver.find_element_by_css_selector("button#btn_download")
        driver.execute_script("arguments[0].click();", element)
        time.sleep(1)
        sel = driver.execute_script("return document.getElementsByClassName('ribbon-heading ribbon-default top-left-right')[0].innerHTML;")
        Infringing = self.get_atr(sel).strip()
        #print(Infringing)
        driver.quit()
        return Infringing
        
      
    def zippy(self, Inf):
        driver = webdriver.Chrome('C:\\Users\\APDIF\\Desktop\\chromedriver.exe')
        driver.get(Inf)
        time.sleep(0.5)
        Infringing = driver.find_element_by_id("dlbutton").get_attribute('href')
        driver.quit()
        return Infringing
    
    def mediaFire(self, response):
        Infringing = response.css('a.input.popsok ::attr(href)').extract_first().strip()
        imprime_datos(response.meta['Titulo'],'', response.meta['Cantante'], response.meta['Album'], response.meta['Referer'], Infringing)
        # INGRESA INFRINGING A LA BD LOS DATOS
        Inserta_Datos(response.meta['Titulo'], response.meta['Cantante'], response.meta['Album'], response.meta['Referer'], Infringing, self.Fecha, self.id_domin)
    
    def get_atr(self, texto):
        if texto:
            texto = texto.split('onclick')[0]
            texto = texto.split('=')[1].replace('"','')
        return texto
                        
    def Limpia_titulo(self,Titulo):
        if Titulo:
            Titulo = Titulo.split('(')[0]
        return Titulo
    
    def get_Album(self,Texto):
        Texto = Texto.strip()
        try:
            Album = Texto.split('–')[1]
            return Album
        except:
            return Texto
    
    def acentos(self, Titulo, Cantante, Album):
        Titulo = strip_accents(Titulo)
        Cantante = strip_accents(Cantante)
        Album = strip_accents(Album)
        return Titulo,Cantante,Album