from os import getenv
from dotenv import load_dotenv

from config.logging_config import setup_logging

# Carregar variáveis do .env
load_dotenv()

ACCOUNTS_CORE = ["torvi_hb", "kprand", "ysetheus", "helpier011", "golerobom196", "valenteb1", "gbgmss", "Tarkeru", "crucisx", "slcaiodev"]
BOT_TOKEN = getenv("BOT_TOKEN")

bot_logger = setup_logging("telegram", "logs/telegram.log")