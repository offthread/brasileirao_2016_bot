#!/usr/bin/python
# -*- coding: latin-1 -*-

from telegram.ext import Updater, CommandHandler
from bs4 import BeautifulSoup
from json_parser import *
import sys
import logging

MIN_FIXTURES = 1
MAX_FIXTURES = 38
MSG_ERROR_FIXTURES = "O número da rodada deve ser um número entre 1 e 38."
TOKEN = sys.argv[1]

def showClassification(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text='<pre>'+getClassification()+'</pre>', parse_mode='HTML', reply_to_message_id=update.message['message_id'])

def showFixture(bot, update):
	if ((len(update.message['text'].split(" "))) > 1):
		fixture = int(update.message['text'].split(" ")[1])
		if (MIN_FIXTURES <= fixture <= MAX_FIXTURES):
			bot.sendMessage(chat_id=update.message.chat_id, text=getFixture(str(fixture)), reply_to_message_id=update.message['message_id'])
		else:
			bot.sendMessage(chat_id=update.message.chat_id, text=MSG_ERROR_FIXTURES, reply_to_message_id=update.message['message_id'])
	else:
		bot.sendMessage(chat_id=update.message.chat_id, text=getFixture(), reply_to_message_id=update.message['message_id'])

def showTopScorers(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text=getTopScorers(), reply_to_message_id=update.message['message_id'])

def showHelp(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text=
		"- Digite /classificacao para visualizar a tabela do Campeonato Brasileiro 2016\n" +\
        "- Digite /rodada para visualizar os jogos da rodada atual do Campeonato Brasileiro 2016\n" +\
        "- Digite /rodada <rodada> para visualizar os jogos de determinada rodada do Campeonato Brasileiro 2016. " +\
        "Exemplo de uso: /rodada 10\n" +\
        "- Digite /artilharia para visualizar a lista de artilheiros do Campeonato Brasileiro 2016.\n" +\
        "Qualquer dúvida ou sugestão envie email para offthread@gmail.com.\n\n" +\
        "Criado pela OFF Thread <http://www.facebook.com/offthread>"
        , reply_to_message_id=update.message['message_id'])

updater = Updater(token=TOKEN)

dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

classification_handler = CommandHandler('classificacao', showClassification)
fixture_handler = CommandHandler('rodada', showFixture)
topScorers_handler = CommandHandler('artilharia', showTopScorers)
help_handler = CommandHandler('ajuda', showHelp)

dispatcher.add_handler(classification_handler)
dispatcher.add_handler(fixture_handler)
dispatcher.add_handler(topScorers_handler)
dispatcher.add_handler(help_handler)

updater.start_polling()