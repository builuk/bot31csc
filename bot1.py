import time
import requests
import random
from commands.calculator import calculate_expression
from commands.weather import get_weather
import os
from dotenv import load_dotenv

load_dotenv()

bot_key = os.getenv("TOKEN")
URL = os.getenv("URL")
url = f"{URL}{bot_key}/"

class Bot:
    __elem = None
    COMMANDS = {'hi','hello','hey',
                'csc31',
                'gin',
                'python',
                'dice',
                'weather'}

    @staticmethod
    def single_init(token, url):
        if Bot.__elem is None:
            element = Bot(token, url)
            Bot.__elem = element
            return element
        else:
            return Bot.__elem

    def __init__(self, token, url):
        self.token = token
        self.url = url

    def _last_update(self, request):
        response = requests.get(request + 'getUpdates')
        # TODO: Uncomment just for local testing, clean up before release
        # print(response)
        response = response.json()
        print(response)
        results = response['result']
        if not response['result']:
            return None
        total_updates = len(results) - 1
        return results[total_updates]

    def _get_chat_id(self, update):
        chat_id = update['message']['chat']['id']
        return chat_id

    def _get_message_text(self, update):
        message_text = update['message']['text']
        return message_text

    def _send_message(self, chat, text):
        params = {'chat_id': chat, 'text': text}
        response = requests.post(url + 'sendMessage', data=params)
        return response

    def _handle_csc31(self, update):
        chat_id = self._get_chat_id(update)
        message_text = 'Python'
        return self._send_message(chat_id, message_text)

    def run(self):
        bot_work = True
        while bot_work:
            last_update = self._last_update(self.url)
            if last_update is None:
                print('Type something.')
                time.sleep(3)
                continue
            update_id = last_update['update_id']
            try:
                while bot_work:
                    time.sleep(1)
                    self.update = self._last_update(url)
                    if update_id == self.update['update_id']:
                        if self._get_message_text(self.update).lower() == 'hi' or self._get_message_text(
                                self.update).lower() == 'hello' or self._get_message_text(self.update).lower() == 'hey':
                            self._send_message(self._get_chat_id(self.update), 'Greetings! Type "Dice" to roll the dice!')
                        elif self._get_message_text(self.update).lower() == 'csc31':
                            self._handle_csc31(self.update)
                        elif self._get_message_text(self.update).lower() == 'gin':
                            self._send_message(self._get_chat_id(self.update), 'Finish')
                            bot_work = False
                        elif self._get_message_text(self.update).lower() == 'python':
                            self._send_message(self._get_chat_id(self.update), 'version 3.10')
                        # from weather import get_weather
                        elif 'weather' in self._get_message_text(self.update).lower():
                            city = self._get_message_text(self.update).lower().replace('weather ', '')
                            weather = get_weather(city)
                            self._send_message(self._get_chat_id(self.update), weather)
                        elif self._get_message_text(self.update).lower() == 'dice':
                            _1 = random.randint(1, 6)
                            _2 = random.randint(1, 6)
                            self._send_message(self._get_chat_id(self.update),
                                         'You have ' + str(_1) + ' and ' + str(_2) + '!\nYour result is ' + str(
                                             _1 + _2) + '!')
                        else:
                            result = calculate_expression(self._get_message_text(self.update))
                            if result is not None:
                                self._send_message(self._get_chat_id(self.update), result)
                            else:
                                self._send_message(self._get_chat_id(self.update), 'Sorry, I don\'t understand you :(')

                        update_id += 1
            except KeyboardInterrupt:
                print('\nБот зупинено')


if __name__ == '__main__':
    bot = Bot.single_init(bot_key, url)
    bot1 = Bot.single_init(bot_key, url)
    bot2 = Bot.single_init(bot_key, url)
    print(bot)
    print(bot1)
    print(bot2)
    bot.run()
    bot1.run()
    bot2.run()
