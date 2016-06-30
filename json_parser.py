#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from datetime import date
import urllib, urllib2, json
import unicodedata

TEAMS_ABREVIATIONS = {'Palmeiras-SP':'PAL','Internacional-RS':'INT','Gremio-RS':'GRE','Corinthians-SP':'COR',\
'Sao Paulo-SP':'SAO','Flamengo-RJ':'FLA','Chapecoense-SC':'CHA','Santos-SP':'SAN','Atletico-PR':'CAP',\
'Ponte Preta-SP':'PON','Fluminense-RJ':'FLU','Figueirense-SC':'FIG','Santa Cruz-PE':'STA','Atletico-MG':'CAM',\
'Vitoria-BA':'VIT','Coritiba-PR':'CFC','Sport-PE':'SPO','Botafogo-RJ':'BOT','Cruzeiro-MG':'CRU','America-MG':'AME',}

MATCH_STATUS = {'encerrados':'encerrado(s)', 'em_andamento':'em andamento', 'agendados':'agendado(s)'}

LINE_SEPARATOR_FIXTURE = "\n---------------------------------------\n"
LINE_SEPARATOR_CLASSIFICATION = "\n-----------------------\n"

def getClassification():
	urlClassification = "http://www.futebolinterior.com.br/json/Classificacao/getClassificacao?id_ano=585&id_fase=&rodada="
	response = urllib.urlopen(urlClassification)
	data = json.loads(response.read())

	position = 1
	strClassification = "|" + '{:^3}'.format('POS') + "|" + '{:^5}'.format('TIME') + "|" + '{:^3}'.format('P') + "|"\
	+ '{:^3}'.format('V') + "|" + '{:^3}'.format('SG') + "|" + LINE_SEPARATOR_CLASSIFICATION
	for team in data['classificacao']:
		strClassification += "|" + '{:>3}'.format(str(position)) + "|" +\
		'{:^5}'.format(TEAMS_ABREVIATIONS[unicodedata.normalize('NFKD', team['clube']).encode('ascii','ignore')]) +\
		"|" + '{:>3}'.format(team['pg']) + "|" + '{:>3}'.format(team['vi']) + "|" + '{:>3}'.format(team['sg']) +\
		"|" + LINE_SEPARATOR_CLASSIFICATION
		position += 1
	return strClassification

def getFixture(fixture=""):
	urlFixture = "http://www.futebolinterior.com.br/json/Agenda/getJogos?id_ano=585&id_fase=2168&rodada=" + fixture + "&por_grupo=1&id_grupo=-1&hash=fase%3DUnica%26rodada%3D6"
	response = urllib.urlopen(urlFixture)
	data = json.loads(response.read())
	
	if (fixture == ""):
		fixture = data["rodada"]
	strFixture = "Rodada " + fixture + ":" + LINE_SEPARATOR_FIXTURE
	for match in data['jogos']:
		if (match['status'] == 'Agendado'):
			strFixture += match['mandante'] + " x " + match['visitante'] + "\n"
			strFixture += match['datahora'] + "\n"
			strFixture += "Agendado"
		elif (match['status'] == 'Encerrado'):
			strFixture += match['mandante'] + " " + match['placar'] + " " + match['visitante'] + "\n"
			strFixture += match['datahora'] + "\n"
			strFixture += "Encerrado"
		else:
			strFixture += match['mandante'] + " " + match['placar'] + " " + match['visitante'] + "\n"
			strFixture += match['datahora'] + "\n"
			strFixture += "Em andamento"
		strFixture += LINE_SEPARATOR_FIXTURE
	return strFixture

def getTopScorers():
	urlTopScorers = "http://www.futebolinterior.com.br/futebol/Brasileiro/Serie-A/2016/artilharia"

	opener = urllib2.build_opener()
	opener.addheaders = [('Accept-Charset', 'utf-8')]
	url_response = opener.open(urlTopScorers)
	content = url_response.read().decode('utf-8')
	soup = BeautifulSoup(content, 'html.parser')

	divStrikers = soup.find_all("div", {"class": "col-md-8"})[2]
	counter = 0
	
	strikers = divStrikers.find_all('p')[1]
	strikers = str(strikers).replace('<p>','')
	strikers = strikers.replace('</p>','')
	strikers = strikers.replace('<strong>','')
	strikers = strikers.replace('</strong>','')
	strikers = strikers.replace('<br/>','\n')
	strikers = strikers.split("\n")

	strStrikers = "Artilheiro(s) do Brasileirão 2016:\n"
	strStrikers += strikers[0]+"\n"
	for i in range(len(strikers)):
		if i > 0:
			strikerReversed = strikers[i].split(" - ")
			strikerReversed.reverse()
			strikerReversed = " - ".join(strikerReversed)
			strStrikers += strikerReversed + "\n"
	return strStrikers

def getMatchesByStatus(status):
	urlFixture = "http://www.futebolinterior.com.br/json/Agenda/getJogos?id_ano=585&id_fase=2168&rodada=&por_grupo=1&id_grupo=-1&hash=fase%3DUnica%26rodada%3D6"
	response = urllib.urlopen(urlFixture)
	data = json.loads(response.read())

	fixture = data["rodada"]

	strFixture = "Jogo(s) " + MATCH_STATUS[status] + " da rodada " + data["rodada"] + ":" + LINE_SEPARATOR_FIXTURE
	strInitial = strFixture
	
	if (status == 'encerrados'):
		for match in data['jogos']:
			if (match['status'] == 'Encerrado'):
				strFixture += match['mandante'] + " " + match['placar'] + " " + match['visitante'] + "\n"
				strFixture += match['datahora']
				strFixture += LINE_SEPARATOR_FIXTURE
	elif (status == 'agendados'):
		for match in data['jogos']:
			if (match['status'] == 'Agendado'):
				strFixture += match['mandante'] + " x " + match['visitante'] + "\n"
				strFixture += match['datahora'] 
				strFixture += LINE_SEPARATOR_FIXTURE
	else:
		for match in data['jogos']:
			if (match['status'] != 'Encerrado') and (match['status'] != 'Agendado'):
				strFixture += match['mandante'] + " " + match['placar'] + " " + match['visitante'] + "\n"
				strFixture += match['datahora']
				strFixture += LINE_SEPARATOR_FIXTURE
	
	if strFixture == strInitial:
		return  "Sem jogo(s) " + MATCH_STATUS[status] + " na rodada " + fixture
	else:
		return strFixture

def getMatchesOfTheDay():
	today = str(date.today().day).zfill(2) + "/" + str(date.today().month).zfill(2) + "/" + str(date.today().year)

	urlFixture = "http://www.futebolinterior.com.br/json/Agenda/getJogos?id_ano=585&id_fase=2168&rodada=&por_grupo=1&id_grupo=-1&hash=fase%3DUnica%26rodada%3D6"
	response = urllib.urlopen(urlFixture)
	data = json.loads(response.read())

	strMatches = "Jogo(s) de hoje" + LINE_SEPARATOR_FIXTURE
	strInitial = strMatches

	for match in data['jogos']:
		if (match['datahora'].split(" ")[0] == today):
			strMatches += match['mandante'] + " x " + match['visitante'] + "\n"
			strMatches += match['datahora']
			strMatches += LINE_SEPARATOR_FIXTURE

	if strMatches == strInitial:
		return  "Sem jogo(s) hoje"
	else:
		return strMatches
