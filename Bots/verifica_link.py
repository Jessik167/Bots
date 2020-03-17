# -*- coding: utf-8 -*-
from xml.dom import minidom
from urllib.parse import urljoin
import urllib.request, json
import requests
import unicodedata
from urllib.parse import quote
import numpy as np

def veri(url):
    try:
        url = quote(url)
        nueva_url = 'http://infringinglinks-bil.owlphacentri.com/checker/isInfringing?url=' + url
        #print(nueva_url)
        xml_str = urllib.request.urlopen(nueva_url).read()
        xmldoc = minidom.parseString(xml_str)
        num = xmldoc.getElementsByTagName('detail')[0]
        
        if num.firstChild.data == '1' or num.firstChild.data == '3' or num.firstChild.data == '11' or num.firstChild.data == '12':
            return True
        else:
            return False
    except urllib.error.URLError as e:
            print(e.reason)
    
def separa_titulo(titulo,separador):
    #####SEPARA CANTANTE Y ALBUM#####
    if titulo is not None:
        try:
            s = titulo.split(separador)
        except:
            s = titulo.split('–')
        if len(s) > 2:
            cantante = '-'
            album = '-'
        else:
            try:
                cantante, album = s[0], s[1]
            except:
                cantante = '-'
                album = '-'
        return cantante, album
    else:
        return '',''
    
def separa(palabra, separador, ind):
        #####SEPARA CANTANTE Y ALBUM#####
        s = palabra.split(separador)
        try:
            item = s[ind]
        except:
            item = '-'
        return item

def strip_spaces(text):
    text = text.strip('\n')
    try:
        text = text.strip('\t')
    except:
        text = text.strip(' ')
    return text


def strip_accents(text):
    try:
        text = str(text, 'utf-8')
    except (TypeError, NameError): 
        pass
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text) 

def imprime_datos(titulo, fecha, cantante, album, referer, infringing):
    print('\n*****************DATOS*****************')
    print('infringing: ' + str(infringing))
    print('referer: ' + str(referer))
    print('titulo: ' + str(titulo))
    print('fecha: ' + str(fecha))
    print('cantante: ' + str(cantante))
    print('album: ' + str(album))
    print('***************************************\n')
    
    
def get_inf(url):
    response = requests.get(url)
    print(response.request.url)
    '''print('URL: ' + url)
    while(response.request.url == url):
        print('ENTRAA')
        response = requests.get(url)'''
    return str(response.request.url)

#print(API_JSON('http://mynewhits.blogspot.com/feeds/posts/summary?alt=json-in-script&callback=pageNavi&max-results=99999'))
#print(get_inf('http://mynewhits.blogspot.com/feeds/posts/summary?alt=json-in-script&callback=pageNavi&max-results=99999'))
#print(veri('https://ngleakers.com/wp-content/uploads/2019/06/MC-Galaxy-–-Man-Must-Wack-feat.-Harrysong-Duncan-Mighty.mp3'))
#print(strip_accents('https://ngleakers.com/wp-content/uploads/2019/07/01-It-Aint-Me-Tiëstos-AFTR_HRS-Re.mp3'))