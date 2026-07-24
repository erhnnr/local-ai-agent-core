import logging
import sys

def setup_logger(name: str = "LocalAIAgent") -> logging.Logger:
    """Proje genelinde kullanılacak standart ve renkli/düzenli loglama yapılandırması."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
            datefmt="%H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.propagate = False
    return logger