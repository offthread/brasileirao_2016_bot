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

LINE_SEPARATOR = "\n---------------------------------------\n"
LINE_SEPARATOR_CLASSIFICATION = "\n-----------------------\n"

NUMBER_OF_STRIKERS = 5

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
	strFixture = "Rodada " + fixture + ":" + LINE_SEPARATOR
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
		strFixture += LINE_SEPARATOR
	return strFixture

def getTopScorers():
	urlTopScorers = "http://www.futebolinterior.com.br/futebol/Brasileiro/Serie-A/2016/artilharia"

	opener = urllib2.build_opener()
	opener.addheaders = [('Accept-Charset', 'utf-8')]
	url_response = opener.open(urlTopScorers)
	content = url_response.read().decode('utf-8')
	soup = BeautifulSoup(content, 'html.parser')

	divStrikers = soup.find_all("div", {"class": "col-md-8"})[2]

	strikersList = divStrikers.find_all('p')
	finalStrikers = []

	for i in range (1, NUMBER_OF_STRIKERS):
		strikersList[i] = str(strikersList[i]).replace('<p>','')
		strikersList[i] = strikersList[i].replace('</p>','')
		strikersList[i] = strikersList[i].replace('<strong>','')
		strikersList[i] = strikersList[i].replace('</strong>','')
		strikersList[i] = strikersList[i].replace('<br/>','\n')
		strikersList[i] = strikersList[i].strip()
		if strikersList[i].endswith('\n'):
			strikersList[i] = strikersList[i][:-2]
		if strikersList[i] != '':
			finalStrikers.append(strikersList[i])

	strStrikers = "Artilheiros do Brasileirão 2016"
	for i in finalStrikers:
		strStrikers += LINE_SEPARATOR
		strStrikers += i

	return strStrikers

def getMatchesByStatus(status):
	urlFixture = "http://www.futebolinterior.com.br/json/Agenda/getJogos?id_ano=585&id_fase=2168&rodada=&por_grupo=1&id_grupo=-1&hash=fase%3DUnica%26rodada%3D6"
	response = urllib.urlopen(urlFixture)
	data = json.loads(response.read())

	fixture = data["rodada"]

	strFixture = "Jogo(s) " + MATCH_STATUS[status] + " da rodada " + data["rodada"] + ":" + LINE_SEPARATOR
	strInitial = strFixture
	
	if (status == 'encerrados'):
		for match in data['jogos']:
			if (match['status'] == 'Encerrado'):
				strFixture += match['mandante'] + " " + match['placar'] + " " + match['visitante'] + "\n"
				strFixture += match['datahora']
				strFixture += LINE_SEPARATOR
	elif (status == 'agendados'):
		for match in data['jogos']:
			if (match['status'] == 'Agendado'):
				strFixture += match['mandante'] + " x " + match['visitante'] + "\n"
				strFixture += match['datahora'] 
				strFixture += LINE_SEPARATOR
	else:
		for match in data['jogos']:
			if (match['status'] != 'Encerrado') and (match['status'] != 'Agendado'):
				strFixture += match['mandante'] + " " + match['placar'] + " " + match['visitante'] + "\n"
				strFixture += match['datahora']
				strFixture += LINE_SEPARATOR
	
	if strFixture == strInitial:
		return  "Sem jogo(s) " + MATCH_STATUS[status] + " na rodada " + fixture
	else:
		return strFixture

def getMatchesOfTheDay():
	today = str(date.today().day).zfill(2) + "/" + str(date.today().month).zfill(2) + "/" + str(date.today().year)

	urlFixture = "http://www.futebolinterior.com.br/json/Agenda/getJogos?id_ano=585&id_fase=2168&rodada=&por_grupo=1&id_grupo=-1&hash=fase%3DUnica%26rodada%3D6"
	response = urllib.urlopen(urlFixture)
	data = json.loads(response.read())

	strMatches = "Jogo(s) de hoje" + LINE_SEPARATOR
	strInitial = strMatches

	for match in data['jogos']:
		if (match['datahora'].split(" ")[0] == today):
			strMatches += match['mandante'] + " x " + match['visitante'] + "\n"
			strMatches += match['datahora']
			strMatches += LINE_SEPARATOR

	if strMatches == strInitial:
		return  "Sem jogo(s) hoje"
	else:
		return strMatches
