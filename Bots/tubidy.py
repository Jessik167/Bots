# -*- coding: utf-8 -*-
'''
Created on 21 ene. 2020

@author: APDIF
'''
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
from datetime import date
from verifica_link import separa_titulo, imprime_datos, veri


class tubidy(scrapy.Spider):
    name = 'tubidy'
    allowed_domains = ['vww.tubidy-mp3.cc','www.internet-dvr.com']
    start_urls = ['http://vww.tubidy-mp3.cc/']
    
    
    def parse(self, response):
        le = LinkExtractor() 
        for link in le.extract_links(response):
            print(link.url)
            yield Request(link.url, meta= {'referer': link.url},callback=self.parse_attr)
        yield Request(link.url,callback=self.parse)
        
    def parse_attr(self, response):
        for li in response.css('li.mp3Play'):
            Titulo = li.css('b ::text').get()
            Cantante,Album = separa_titulo(Titulo,'-')
            Fecha = date.today().strftime("%d %B, %Y")
            id = li.css('a.b_down ::attr(data-url)').get()
            if id is not None:
                url = 'https://www.internet-dvr.com/api-private.js?vidID={}&token=37fb468a1118f225202b8f6be914f4406c93954f1b460d36afb40d540581508b74fefaa886db99f2fb8d3ac3bcd481a77a658c4432f801bd8df0c4da26916588'.format(id)
                #print(url)
                yield Request(url, meta= {'referer': response.meta['referer'], 'Titulo': Titulo, 'Cantante': Cantante, 'Album':Album, 'Fecha': Fecha}, callback=self.parse_attr2)
        
    def parse_attr2(self, response):
        #print('ENTRA')
        infringing = response.css('a.download-mp3-url ::attr(href)').get()
        #print(infringing[-3::])
        if infringing[-3::] == 'mp3':
            if veri(infringing)==True:
                imprime_datos(response.meta['Titulo'],response.meta['Fecha'],response.meta['Cantante'],response.meta['Album'],response.meta['referer'],infringing)