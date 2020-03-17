# -*- coding: utf-8 -*-
'''
Created on 20 ene. 2020

@author: Jessy APDIF
'''
import scrapy
import Vista as v
import Controlador as c
from datetime import date
from Verifica import veri, separa_titulo, imprime_datos, retorna_dominio


class elmanualnlhc(scrapy.Spider):
    name = 'elmanualnlhc'
    _num_pagina = 1
    id_domin = 0
    start_urls = ['https://elmanualnlhc.wordpress.com/']

    id_domin = retorna_dominio(start_urls[0])           
    
    def parse(self, response):
        #####RECORRE DIVS#####
        for div in response.css('div.narrowcolumn > div'):
            infringing = div.css('div >p > a ::text').extract_first()
            #####VERIFICA QUE INFRINGING CONTENGA TEXTO#####
            if infringing is not None:
                #####SI CONTIENE LA PALABRA DOWNLOAD#####
                if infringing.find('Download') != -1 or infringing.find('download') != -1:
                    #####TOMA EL RESTO DE LOS DATOS#####
                    Titulo = div.css('h2 ::attr(title)').get()
                    referer = div.css('h2 ::attr(href)').get()
                    Fecha = div.css('p.postmetadata ::text').get()
                    Fecha = Fecha.replace('\n\t\t\t','')
                    #####TOMA EL INFRINGING#####
                    infringing = div.css('div >p > a ::attr(href)').extract_first()
                    #####VERIFICA QUE NO SEA UNA IMAGEN#####
                    if infringing.find('.png') == -1 or infringing.find('.jpg') == -1:
                        #####VERIFICA SI ES UN LINK VÁLIDO#####
                        if veri(infringing) == True:
                            #####LIMPIA EL TEXTO DEL TÍTULO#####
                            if Titulo is not None:
                                Titulo = Titulo.replace('\xa0', ' ')
                            #####SEPARA EL CANTANTE Y EL ALBUM DEL TÍTULO#####
                            Cantante, Album = separa_titulo(Titulo,'–')
                            print((Titulo,Cantante,Album,referer,infringing,Fecha))
                            #####SI NO EXISTE, LO INSERTA LOS DATOS EN LA BD#####
                            if c.existe_inf(infringing) == False:
                                c.inserta_item(Titulo, Cantante, Album, referer, infringing, Fecha, self.id_domin)
                                v.muestra_item_guardado(Titulo)
        
        #####PASA A LA SIGUIENTE PÁGINA#####
        self._num_pagina+=1
        try:
            next_page = 'https://elmanualnlhc.wordpress.com/page/{}/'.format(self._num_pagina)
            yield response.follow(next_page, callback= self.parse)
        except:
             pass