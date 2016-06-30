# brasileirao_2016_bot
A Telegram bot to monitor results, standings and the top scorers of the Brazilian Championship. The information is retrieved from www.futebolinterior.com.br

If you are a Telegram user, you can include this bot (@brasileirao_2016_bot) into a channel or write commands directly on a private chat.

We support the following commands:

* /rodada - To show the results of the current fixture

* /rodada fixtureNumber - To show the results of a certain fixture

* /classificacao - To show the league table

* /artilharia - To show the top scorers

* /encerrados - To show the finished matches of the current fixture

* /em_andamento - To show the ongoing matches of the current fixture

* /agendados - To show the scheduled matches of the current fixture

* /jogos_do_dia - To show the matches of the day

## Example of usage ##
* /rodada 10 -> To show the results of the tenth fixture

## Project Configuration ##

This project is configured to run using the following configuration:

* Python version - 2.7.6
* Python Telegram Bot - 4.2.1
* BeautifulSoup - 4.4.1

## Deployment Instructions ##

```python
python bot <YOUR_BOT_TOKEN>
```
to start the bot

## License ##
This software is licensed under the Apache 2 license, quoted below.

Copyright 2016 OFF Thread <offthread@gmail.com>

Licensed under the Apache License, Version 2.0 (the "License"); you may not
use this file except in compliance with the License. You may obtain a copy of
the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
License for the specific language governing permissions and limitations under
the License.

## Contributing ##

Feel free to contribute using your own bot.
