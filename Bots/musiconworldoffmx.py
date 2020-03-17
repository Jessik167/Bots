# -*- coding: utf-8 -*-
'''
Created on 11 mar. 2020

@author: Jessy APDIF
'''
import scrapy
from selenium import webdriver
from scrapy.http import Request
from Verifica import imprime_datos, retorna_dominio, Get_megaLink, Inserta_Datos


class musiconworldoffmx(scrapy.Spider):
    name = 'musiconworldoffmx'
    _num_pagina = 1
    id_domin = 0
    start_urls = ['http://musiconworldoffmx.com/']
    # RETORNA EL �LTIMO DOMINIO
    id_domin = retorna_dominio(start_urls[0])
    
    
    def parse(self, response):
        print('##### PÁGINA #{} #####'.format(self._num_pagina))
        #####RECORRE "ARTICLES"#####
        for art in response.css('div.entry-content a'):
            #print(art.get())
            referer = art.css('a ::attr(href)').get()
            yield Request(referer, callback=self.parse_attr)

            
        next_page = response.css('div.nav-previous > a ::attr(href)').get()
        if next_page:
            self._num_pagina += 1   
            yield response.follow(next_page, callback= self.parse)
            
                  
    def parse_attr(self, response):
        #print(response.text)
        try:
            Titulo = response.css('h2.entry-title > a ::text').get()
            Cantante = self.Limpia_titulo(Titulo)
            Fecha = response.css('div.entry-meta ::text').extract()[0].strip() +' '+ response.css('div.entry-meta ::text').extract()[1].strip()
            Fecha = Fecha.strip()
            for alb in response.css('div.entry-content > p a'):
                Album = alb.css('::text').get()
                Album = self.get_Album(Album)
                Inf = alb.css('::attr(href)').get()
                imprime_datos(Titulo,Fecha, Cantante, Album, response.url, Inf)
                # INGRESA INFRINGING A LA BD LOS DATOS
                Inserta_Datos(Titulo, Cantante, Album, response.url, Inf, Fecha, self.id_domin)
            driver = webdriver.Chrome('C:\\Users\\APDIF\\Desktop\\chromedriver.exe')
            driver.get(Inf)
            Infringing_mega = Get_megaLink(driver)
            imprime_datos(Titulo,Fecha, Cantante, Album, response.url, Infringing_mega)
            # INGRESA INFRINGING A LA BD LOS DATOS
            Inserta_Datos(Titulo, Cantante, Album, response.url, Infringing_mega, Fecha, self.id_domin)
        except:
            pass
        
                    
                    
    def Limpia_titulo(self,Titulo):
        if Titulo:
            Titulo = Titulo.replace('Discografia','').replace('Discograifa','').replace('MEGA','')
            Titulo = Titulo.split('(')[0]
            try:
                Titulo = Titulo.split('(')[0].strip()
            except:
                pass
        return Titulo
    
    def get_Album(self,Texto):
        Texto = Texto.strip()
        try:
            Album = Texto.split('–')[1]
            return Album
        except:
            return Texto