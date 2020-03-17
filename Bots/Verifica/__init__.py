# -*- coding: utf-8 -*-
import time
import requests
import Vista as v
import numpy as np
import unicodedata
import Controlador as c
from datetime import date
from xml.dom import minidom
import urllib.request, json
from urllib.parse import quote
from urllib.parse import urljoin


def retorna_dominio(dominio):
    id_domin = c.existe_id(dominio)
    if id_domin == False:
        #####TOMA EL �LTIMO ID DE LA TABLA DE DOMINIOS EN LA BD#####
        id_domin = c.ultimo_id()
        #####SI NO EXISTE, LO AGREGA#####
        if c.existe_ultimoId(dominio) == False:
            id_domin = id_domin + 1
            #####TOMA LA FECHA ACTUAL#####
            hoy = date.today().strftime("%d %B, %Y")
            #####INSERTA EN LA TABLA RELACIONAL#####
            c.inserta_uno_relacional(id_domin,dominio,hoy)
    return id_domin


def veri(url):
    try:
        url = quote(url)
        nueva_url = 'http://infringinglinks-bil.owlphacentri.com/checker/isInfringing?url=' + url
        #print(nueva_url)
        xml_str = urllib.request.urlopen(nueva_url).read()
        xmldoc = minidom.parseString(xml_str)
        num = xmldoc.getElementsByTagName('detail')[0]
        #print(num.firstChild.data)
        if num.firstChild.data == '1' or num.firstChild.data == '3' or num.firstChild.data == '11' or num.firstChild.data == '12':
            return True
        else:
            return False
    except urllib.error.URLError as e:
            print(e.reason)
            
#print(veri('https://download1580.mediafire.com/pfvzq965zqqg/0xyj5j9dvttsjil/RC+-+MGYY4%28A%29.zip'))

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
                cantante, album = s[0].strip(), s[1].strip()
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


def Inserta_Datos(Titulo, Cantante, Album, Referer, Infringing, Fecha, id_domin):
    #####SI NO EXISTE, LO INSERTA LOS DATOS EN LA BD#####
    if c.existe_inf(Infringing) == False:
        if veri(Infringing) == True:
            c.inserta_item(Titulo, Cantante, Album, Referer, Infringing, Fecha, id_domin)
            v.muestra_item_guardado(Titulo)
                
#Inserta_Datos('El Loquito del Rancho  Reloj', 'El Loquito del Rancho', 'Reloj', 'http://playcorridos.com/el-loquito-del-rancho-reloj-en-vivo-single-2020/', 'https://download.usercdn.com:443/d/eyl5tljqtn2fvxijx7iynukzkpsbkxbtj5h52knpjin23v3qbbejg6lfisgzt3p2gprms5pc/El Loquito del Rancho - Reloj (En Vivo).mp3', 'March 12, 2020', 27)

def imprime_datos(titulo = '', fecha = '', cantante = '', album = '', referer = '', infringing= ''):
    if fecha == '':
        fecha = date.today().strftime("%d %B, %Y")
    print('\n*****************DATOS*****************')
    print('Infringing: ' + str(infringing))
    print('Referer: ' + str(referer))
    print('Titulo: ' + str(titulo))
    print('Fecha: ' + str(fecha))
    print('Cantante: ' + str(cantante))
    print('Album: ' + str(album))
    print('***************************************\n')
    
    
def get_inf(url):
    response = requests.get(url)
    print(response.request.url)
    '''print('URL: ' + url)
    while(response.request.url == url):
        print('ENTRAA')
        response = requests.get(url)'''
    return str(response.request.url)

def cierra_ventanas(driver):
        original_handle = driver.window_handles[0]
        for handle in driver.window_handles:
            if handle != original_handle:
                driver.switch_to.window(handle)
                driver.close()
        driver.switch_to.window(original_handle)
        
def Get_megaLink(driver):
    Infringing_mega = False
    while True:
        time.sleep(3)
        try:
            try:
                element = driver.find_element_by_id("btn-main")
                driver.execute_script("arguments[0].click();", element)
            except:
                driver.find_element_by_id("btn-main").click()
            cierra_ventanas(driver)
            time.sleep(0.5)
            Infringing_mega = driver.current_url
            if Infringing_mega.find('mega') != -1:
                break
        except:
            break
    driver.quit()
    return Infringing_mega


#print(API_JSON('http://mynewhits.blogspot.com/feeds/posts/summary?alt=json-in-script&callback=pageNavi&max-results=99999'))
#print(get_inf('http://mynewhits.blogspot.com/feeds/posts/summary?alt=json-in-script&callback=pageNavi&max-results=99999'))
#print(veri('https://ngleakers.com/wp-content/uploads/2019/06/MC-Galaxy-–-Man-Must-Wack-feat.-Harrysong-Duncan-Mighty.mp3'))
#print(strip_accents('https://ngleakers.com/wp-content/uploads/2019/07/01-It-Aint-Me-Tiëstos-AFTR_HRS-Re.mp3'))