# -*- coding: utf-8 -*-
'''
Created on 10 mar. 2020

@author: Jessy APDIF
'''
import scrapy
from datetime import date
from selenium import webdriver
from scrapy.http import Request
from Verifica import separa_titulo, imprime_datos, retorna_dominio, Get_megaLink, Inserta_Datos


class Discografiasmega(scrapy.Spider):
    name = 'Discografiasmega'
    _num_pagina = 1
    id_domin = 0
    start_urls = ['https://www.discografiasmega.com/']
    # RETORNA EL �LTIMO DOMINIO
    id_domin = retorna_dominio(start_urls[0])
    
    
    def parse(self, response):
        #####RECORRE "ARTICLES"#####
        for art in response.css('div.archive-main.archive-masonry  article'):
            referer = art.css('h2 > a ::attr(href)').get()
            yield Request(referer, meta= {'referer': referer},callback=self.parse_attr)
            
        next_page = response.css('a.next.page-numbers ::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback= self.parse)
            
                  
    def parse_attr(self, response):
        i = 0
        Fecha = date.today().strftime("%d %B, %Y")
        for T in response.xpath(".//strong[contains(text(), 'MEGA')]"):
            i += 1
            Titulo = self.Limpia_titulo(T.css('::text').get())
            Cantante, Album = separa_titulo(Titulo, '–')
            if i == 1:
                padre = T.xpath('..')
                Infringing = padre.css('a ::attr(href)').get()
                imprime_datos(Titulo,'', Cantante, Album, response.meta['referer'], Infringing)
                # INGRESA INFRINGING A LA BD LOS DATOS
                Inserta_Datos(Titulo, Cantante, Album, response.meta['referer'], Infringing, Fecha, self.id_domin)
            # INGRESA AL INFRINGING POR MEDIO DE SELENIUM
            self.Datos_Selenium(Titulo, Cantante, Album, response.meta['referer'], Infringing, Fecha, i)
            
            
    def Datos_Selenium(self,Titulo, Cantante, Album, Referer, Infringing, Fecha, i):
        driver = webdriver.Chrome('C:\\Users\\APDIF\\Desktop\\chromedriver.exe')
        driver.get(Infringing)
        Inf_short = driver.find_element_by_xpath("//div[@class='link-container']/a["+ str(i) +"]").text
        # SIGUE EL INFRINGING
        driver.get(Inf_short)
        # INGRESA INFRINGING A LA BD LOS DATOS
        imprime_datos(Titulo,'', Cantante, Album, Referer, Inf_short)
        # INGRESA INFRINGING A LA BD LOS DATOS
        Inserta_Datos(Titulo, Cantante, Album, Referer, Inf_short, Fecha, self.id_domin)
        Infringing_mega = Get_megaLink(driver)
        if Infringing_mega != False:
            # INGRESA INFRINGING A LA BD LOS DATOS
            imprime_datos(Titulo,'', Cantante, Album, Referer, Infringing_mega)
            # INGRESA INFRINGING A LA BD LOS DATOS
            Inserta_Datos(Titulo, Cantante, Album, Referer, Infringing_mega, Fecha, self.id_domin)
        driver.quit()
                    
                    
    def Limpia_titulo(self,Titulo):
        Titulo = Titulo.replace('Descargar','').replace('MEGA','')
        Titulo = Titulo.split('[')[0]
        return Titulo