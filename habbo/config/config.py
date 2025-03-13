from g_python.gextension import Extension

from config.logging_config import setup_logging


habbo_logger = setup_logging("habbo", "logs/habbo.log")

extension_info = {
    "title": "Torvi. Teste",
    "description": "Teste DIC",
    "version": "1.0",
    "author": "Torvi."
}
ext = Extension(extension_info, ('-p', '9092'))
