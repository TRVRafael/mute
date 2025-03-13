import re
from collections import Counter

from habbo.managers import user_manager
from habbo.config import habbo_logger
from data import db_controller
from habbo.utils import get_timestamp

from collections import deque
import time

class SpamDetector:
    def __init__(self, max_messages=3, time_window=5, min_length=30):
        self.messages = deque()  # Armazena timestamps das mensagens
        self.max_messages = max_messages  # Máximo de mensagens permitidas no tempo
        self.time_window = time_window  # Intervalo de tempo (segundos)
        self.min_length = min_length  # Tamanho mínimo da mensagem para ser contada
        self.user_messages = {}  # Dicionário para armazenar mensagens por usuário

    def is_spam(self, user_id: int, message: str) -> bool:
        """Verifica se o usuário enviou 3 mensagens grandes em menos de 5s."""
        if len(message) < self.min_length:
            return False  # Ignora mensagens curtas

        current_time = time.time()
        
        # Se o usuário ainda não existe no dicionário, cria um deque para ele
        if user_id not in self.user_messages:
            self.user_messages[user_id] = deque()
        
        user_queue = self.user_messages[user_id]
        user_queue.append(current_time)

        # Remove mensagens antigas fora da janela de tempo
        while user_queue and user_queue[0] < current_time - self.time_window:
            user_queue.popleft()

        # Se já temos 3 mensagens no intervalo de tempo, é spam
        return len(user_queue) >= self.max_messages


class Message:
    def __init__(self, user_room_index : int, message_text : str):
        self._user_room_index = user_room_index
        self._message_text = message_text
        
    def is_valid_command(self) -> bool:
        command = self._message_text.split(" ", 1)[0]
        if command in {"!mute", "!unmute"}:
            habbo_logger.info(f"Command detected: {command}")
            return True
        return False
        
    def contains_muted_expressions(self, muted_expressions: list) -> list:
        message_text = self._message_text.lower()  # Converte para minúsculas
    
        # Converte lista de tuplas em lista de strings
        muted_expressions_list = [re.escape(expression[0].lower()) for expression in muted_expressions]
        
        found_expressions = []

        # Verifica se alguma das frases bloqueadas está na mensagem como uma palavra/frase isolada
        for exp in muted_expressions_list:
            pattern = rf'\b{exp}\b'  # Usa \b para garantir que é uma palavra/frase separada
            if re.search(pattern, message_text):
                found_expressions.append(exp)

        if found_expressions:
            habbo_logger.warning(f"Message with muted expressions ({found_expressions}): {self._message_text}")

        return found_expressions  # Retorna a lista de expressões encontradas
    
    def handle_command(self):
        expression = self._message_text.split()[1]
        if self._message_text.split()[0] == "!mute":
            db_controller.insert_muted_expression(user_manager.get_user_info(self._user_room_index)['user_name'], expression, get_timestamp())
        elif self._message_text.split()[0] == "!unmute":
            db_controller.remove_muted_expression(user_manager.get_user_info(self._user_room_id)['user_name'], expression, get_timestamp())
            
    def is_too_repetitive(self, threshold: int = 10) -> bool:
        words = re.findall(r'\b\w+\b', self._message_text.lower())  # Divide o texto em palavras
        word_counts = Counter(words)  # Conta a frequência de cada palavra
        
        for word, count in word_counts.items():
            if count >= threshold:
                return True  # Encontra pelo menos uma palavra repetida acima do limite
        
        return False
            
    def check_spam(self):
        self._message_text = self._message_text.encode("latin1").decode("utf-8")
        return self._message_text.count("¬") > 5 or self._message_text.count("•") > 5 or self.is_too_repetitive()