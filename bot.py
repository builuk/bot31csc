import time
import requests
import random
import os
from typing import Optional, Dict, Callable
from dotenv import load_dotenv
from commands.calculator import calculate_expression
from commands.weather import get_weather

load_dotenv()


class TelegramBot:
    """Telegram Bot клас для обробки повідомлень та команд."""
    
    # Константи команд
    COMMANDS = {
        'hi', 'hello', 'hey',
        'csc31',
        'gin',
        'python',
        'dice',
        'weather'
    }
    
    # Грейтингові команди
    GREETING_COMMANDS = {'hi', 'hello', 'hey'}
    
    def __init__(self, token: str, base_url: str):
        """
        Ініціалізація бота.
        
        Args:
            token: Telegram Bot Token
            base_url: Base URL для Telegram API
        """
        self.token = token
        self.base_url = base_url
        self.url = f"{base_url}{token}/"
        self.update_id: Optional[int] = None
        self.command_handlers: Dict[str, Callable] = {
            'hi': self._handle_greeting,
            'hello': self._handle_greeting,
            'hey': self._handle_greeting,
            'csc31': self._handle_csc31,
            'gin': self._handle_gin,
            'python': self._handle_python,
            'dice': self._handle_dice,
            'weather': self._handle_weather,
        }
    
    def get_last_update(self) -> Optional[Dict]:
        """
        Отримує останнє оновлення з Telegram API.
        
        Returns:
            Словник з останнім оновленням або None якщо помилка
        """
        try:
            response = requests.get(self.url + 'getUpdates', timeout=10)
            response.raise_for_status()
            data = response.json()
            results = data.get('result', [])
            if not results:
                return None
            return results[-1]
        except requests.RequestException as e:
            print(f"Помилка отримання оновлень: {e}")
            return None
        except (KeyError, ValueError) as e:
            print(f"Помилка парсингу відповіді: {e}")
            return None
    
    def extract_chat_id(self, update: Dict) -> Optional[int]:
        """
        Витягує chat_id з оновлення.
        
        Args:
            update: Словник оновлення
            
        Returns:
            chat_id або None
        """
        try:
            return update['message']['chat']['id']
        except (KeyError, TypeError):
            return None
    
    def extract_message_text(self, update: Dict) -> Optional[str]:
        """
        Витягує текст повідомлення з оновлення.
        
        Args:
            update: Словник оновлення
            
        Returns:
            Текст повідомлення або None
        """
        try:
            return update['message']['text']
        except (KeyError, TypeError):
            return None
    
    def send_message(self, chat_id: int, text: str) -> bool:
        """
        Надсилає повідомлення користувачу.
        
        Args:
            chat_id: ID чату
            text: Текст повідомлення
            
        Returns:
            True якщо успішно, False інакше
        """
        try:
            params = {'chat_id': chat_id, 'text': text}
            response = requests.post(
                self.url + 'sendMessage',
                data=params,
                timeout=10
            )
            response.raise_for_status()
            return True
        except requests.RequestException as e:
            print(f"Помилка надсилання повідомлення: {e}")
            return False
    
    def _handle_greeting(self, chat_id: int, message_text: str) -> bool:
        """Обробка команд привітання."""
        return self.send_message(
            chat_id,
            'Greetings! Type "Dice" to roll the dice!'
        )
    
    def _handle_csc31(self, chat_id: int, message_text: str) -> bool:
        """Обробка команди CSC31."""
        return self.send_message(chat_id, 'Python')
    
    def _handle_gin(self, chat_id: int, message_text: str) -> bool:
        """Обробка команди gin (вихід)."""
        self.send_message(chat_id, 'Finish')
        return False  # Сигналізує про вихід
    
    def _handle_python(self, chat_id: int, message_text: str) -> bool:
        """Обробка команди python."""
        return self.send_message(chat_id, 'version 3.10')
    
    def _handle_dice(self, chat_id: int, message_text: str) -> bool:
        """Обробка команди dice."""
        dice1 = random.randint(1, 6)
        dice2 = random.randint(1, 6)
        result = dice1 + dice2
        message = (
            f'You have {dice1} and {dice2}!\n'
            f'Your result is {result}!'
        )
        return self.send_message(chat_id, message)
    
    def _handle_weather(self, chat_id: int, message_text: str) -> bool:
        """Обробка команди weather."""
        try:
            # Витягуємо назву міста після слова "weather"
            city = message_text.lower().replace('weather', '').strip()
            if not city:
                return self.send_message(
                    chat_id,
                    'Please specify a city. Example: weather Kyiv'
                )
            weather_info = get_weather(city)
            return self.send_message(chat_id, weather_info)
        except Exception as e:
            print(f"Помилка отримання погоди: {e}")
            return self.send_message(
                chat_id,
                'Sorry, I couldn\'t get the weather information.'
            )
    
    def _handle_calculator(self, chat_id: int, message_text: str) -> bool:
        """Обробка математичних виразів."""
        result = calculate_expression(message_text)
        if result is not None:
            return self.send_message(chat_id, result)
        return self.send_message(
            chat_id,
            'Sorry, I don\'t understand you :('
        )
    
    def _process_message(self, chat_id: int, message_text: str) -> bool:
        """
        Обробляє повідомлення та викликає відповідний обробник.
        
        Args:
            chat_id: ID чату
            message_text: Текст повідомлення
            
        Returns:
            True якщо продовжувати роботу, False якщо завершити
        """
        if not message_text:
            return True
        
        message_lower = message_text.lower()
        
        # Перевірка точних команд
        if message_lower in self.GREETING_COMMANDS:
            return self._handle_greeting(chat_id, message_text)
        elif message_lower == 'csc31':
            return self._handle_csc31(chat_id, message_text)
        elif message_lower == 'gin':
            return self._handle_gin(chat_id, message_text)
        elif message_lower == 'python':
            return self._handle_python(chat_id, message_text)
        elif message_lower == 'dice':
            return self._handle_dice(chat_id, message_text)
        elif message_lower.startswith('weather'):
            return self._handle_weather(chat_id, message_text)
        else:
            # Спробувати обробити як математичний вираз
            return self._handle_calculator(chat_id, message_text)
    
    def run(self):
        """Головний цикл бота."""
        print("Бот запущено...")
        
        # Отримуємо початкове update_id
        initial_update = self.get_last_update()
        if initial_update:
            self.update_id = initial_update.get('update_id', 0)
        
        try:
            while True:
                time.sleep(1)  # Обмеження для pythonanywhere
                
                update = self.get_last_update()
                if not update:
                    continue
                
                current_update_id = update.get('update_id')
                
                # Пропускаємо вже оброблені повідомлення
                if self.update_id is not None and current_update_id == self.update_id:
                    continue
                
                # Оновлюємо update_id перед обробкою
                self.update_id = current_update_id
                
                # Витягуємо дані з оновлення (кешуємо, щоб не викликати кілька разів)
                chat_id = self.extract_chat_id(update)
                message_text = self.extract_message_text(update)
                
                if not chat_id or not message_text:
                    continue
                
                # Обробляємо повідомлення
                should_continue = self._process_message(chat_id, message_text)
                if not should_continue:
                    print("Отримано команду виходу. Завершення роботи...")
                    break
                    
        except KeyboardInterrupt:
            print('\nБот зупинено')
        except Exception as e:
            print(f"Критична помилка: {e}")


def main():
    """Головна функція для запуску бота."""
    bot_token = os.getenv("TOKEN")
    base_url = os.getenv("URL")
    
    if not bot_token or not base_url:
        raise ValueError("TOKEN та URL повинні бути встановлені в змінних оточення")
    
    bot = TelegramBot(token=bot_token, base_url=base_url)
    bot.run()


if __name__ == '__main__':
    main()
