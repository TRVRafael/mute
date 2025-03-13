from collections import deque
import time

class SpamDetector:
    def __init__(self, max_messages=2, time_window=5, min_length=3):
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
        print("aq")
        return len(user_queue) >= self.max_messages
    
spam_detector = SpamDetector()