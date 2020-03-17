# -*- coding: utf-8 -*-
'''
Created on 23 ene. 2020

@author: JessyAPDIF
'''
import emoji
import scrapy
import Vista as v
import Controlador as c
from datetime import date
from scrapy.http import Request
from Verifica import veri, separa_titulo, imprime_datos, retorna_dominio


class mp3teca(scrapy.Spider):
    name = 'mp3teca'
    _num_pagina = 2
    id_domin = 0
    start_urls = ['https://mp3teca.com/mp3s/']
    inf_url = 'http://yyy-music.com/d/'
    hoy = date.today().strftime("%d %B, %Y")
    
    custom_settings = {'CONCURRENT_REQUESTS': 10,
                       'DOWNLOAD_DELAY':0.8}
    
    id_domin = retorna_dominio(start_urls[0])
    
    def parse(self, response):
        for li in response.css('div#content > div ul > li'):
            referer = li.css('a ::attr(href)').get()
            Titulo = li.css('a ::text').get()
            Titulo = self.give_emoji_free_text(Titulo)
            #print(Titulo)
            Cantante, Cancion = separa_titulo(Titulo, '–')
            Cantante = self.give_emoji_free_text(Cantante)
            id = self.get_id(referer)
            url = self.inf_url + id
            yield Request(url, meta= {'referer': referer, 'Titulo': Titulo, 'Cantante': Cantante, 'Cancion': Cancion, 'Fecha': self.hoy}, callback=self.parse_attr)
        #####PASA A LA SIGUIENTE PÁGINA#####
        self._num_pagina+=1
        try:
            next_page = 'https://mp3teca.com/mp3s/page/{}/'.format(self._num_pagina)
            yield response.follow(next_page, callback= self.parse)
        except:
            pass
    
    
    def parse_attr(self, response):
        infringing = response.css('a.btn-nwo ::attr(href)').get()
        #infringing = str(infringing,'utf-8')
        #infringing = self.give_emoji_free_text(infringing)
        #####VERIFICA SI ES UN LINK VÁLIDO#####
        if veri(infringing) == True:
            if c.existe_ref(response.meta['referer']) == False:
                imprime_datos(response.meta['Titulo'], response.meta['Fecha'], response.meta['Cantante'], response.meta['Cancion'], response.meta['referer'], infringing)
                if c.inserta_item(response.meta['Titulo'], response.meta['Cantante'], response.meta['Cancion'], response.meta['referer'], infringing, response.meta['Fecha'], self.id_domin) == True:
                    v.muestra_item_guardado(response.meta['Titulo'])
                
                
    def give_emoji_free_text(self, text):
        allchars = [str for str in text]
        emoji_list = [c for c in allchars if c in emoji.UNICODE_EMOJI]
        clean_text = ' '.join([str for str in text.split() if not any(i in str for i in emoji_list)])
        return clean_text
        
        
    def get_id(self,ref):
        ref = ref.split('/')
        return ref[4]