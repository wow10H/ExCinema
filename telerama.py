#!/usr/bin/python

#permet de récupérer une page html
import requests

#regex
import re

#parser
from bs4 import BeautifulSoup

#sql
import psycopg2

import sys

import configparser

def extraction_premier_nombre(text):
    
    n = re.findall('[0-9]+',text)
    
    if n != []:
        return n[0]
    else:
        return None

def extraction_telerama(url):
    url = url.strip()

    if re.match('(http://www.telerama.fr|http://television.telerama.fr)',url) is None:
        print("URL ko :", url)
        return None
    
    req = requests.get(url)
    url = req.url

    soup = BeautifulSoup(req.content, "html.parser")

    p = re.compile('([0-9]+)(\.php|,critique|,photos)')
    
    if p.match(url) is None:
        print("URL ko num::", url)
        return None
    
    idfilms = p.search(url).group(1)
    


    #<p class="rating--tra"><i class="tra-2"></i> <span>On n’aime pas</span></p>
    rating_p = soup.find('p', class_='rating--tra')
    
    #parfois ce n'est pas une page de note par exemple 
    #http://www.telerama.fr/festival-de-cannes/2018/lhomme-qui-tua-don-quichotte,-de-terry-gilliam-arrive-enfin-a-cannes-inegal-mais-avec-de-vrais,n5654356.php 
    if rating_p is None:
        return None

    note = rating_p.get_text().strip()
    note_img = rating_p.find('i')['class'][0]

    # <li class="pw-title hidden"><a class="pw_title">Bienvenue en Sicile</a></li>
    titre = soup.find('li',class_='pw-title hidden').get_text()

    #<span itemprop="dateCreated"> (2016)</span>
    #annee_text récupère ' (2016)'
    annee_text = soup(itemprop='dateCreated')
   
    if len(annee_text) > 0:
        annee = extraction_premier_nombre(annee_text[0].get_text())
    else:
        annee = 0


    #<p class="fiche--director">
    #     Réalisé par      <span itemprop="director" itemscope="" itemtype="http://schema.org/Person">
    #    <a data-href="L3BlcnNvbm5hbGl0ZS9waWYsNTY2NTUzLnBocA==" class="obf"><span itemprop="name">Pif</span></a>      </span>
    #          <span itemprop="dateCreated"> (2016)</span>
    #  </p>

    try:
        real_p = soup.find('p', class_='fiche--director')
        real = real_p.find('a', class_='obf').get_text()
    except AttributeError:
        real = ""

    return {'idfilms': int(idfilms), 'note': note, 'note_img': note_img, 'titre': titre, 'annee': int(annee), 'real': real, 'url': url} 



def add_dic_to_telefilms(dic):
    curseur.execute("""
        INSERT INTO telefilms (idfilms, titre, annee, real, note, note_img, url) 
        VALUES (%(idfilms)s, %(titre)s, %(annee)s, %(real)s, %(note)s, %(note_img)s, %(url)s)
        ON CONFLICT DO NOTHING""", dic) 


def add_idac_to_telefilm(dic):
    curseur.execute("UPDATE telefilms SET idac = %(idac)s where idfilms = %(idtele)s", dic) 


def ajout_url_tele_to_telefilms(url):
    dic_tele = extraction_telerama(url)
    
    if dic_tele is not None:
        add_dic_to_telefilms(dic_tele)

def extraction_telerama_allocine_page(text):
    soup = BeautifulSoup(text, "html.parser")

    rubric = soup.find('div', class_='colcontent')
    datablock = rubric.findAll('div', class_='datablock')

    for block in datablock:
        idac_div = block.find('div', class_='titlebar')
        idac_hr = block.find('a', href=True)['href']
        idac = extraction_premier_nombre(idac_hr)

        tele_a = block.find('a', class_='test')
        
        if tele_a is not None:
            tele_url = tele_a['href']
            tele_id = extraction_premier_nombre(tele_url)
        else:
            tele_id = None

        if tele_id is not None:
            print(tele_url)
            ajout_url_tele_to_telefilms(tele_url)
            add_idac_to_telefilm({'idac': idac, 'idtele': tele_id})


def extraction_telerama_allocine_recursive(url):
    req = requests.get(url)

    soup = BeautifulSoup(req.content, "html.parser")

    extraction_telerama_allocine_page(req.content)
    db.commit()

    prochain_li = soup.find('li', class_='navnextbtn')
    prochain_href = prochain_li.find('a',href=True)
    
    if prochain_href is not None:
        prochain = "http://www.allocine.fr" + prochain_href['href']
        print(prochain)
        extraction_telerama_allocine_recursive(prochain)
    else:
        print("fini")
    
config = configparser.RawConfigParser()
config.read('conf.ini')

dbname = config.get('DatabaseSection', 'database.dbname')
dbuser = config.get('DatabaseSection', 'database.user')

db = psycopg2.connect("dbname=" + dbname + " user=" + dbuser)
curseur = db.cursor()

#extraction_telerama(sys.argv[1])

extraction_telerama_allocine_recursive(sys.argv[1])

curseur.close()
db.close()
