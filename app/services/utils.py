"""
    Esse código guarda todas funções utilitárias para a aplicação.

author: github.com/gustavosett 
"""

import asyncio
import datetime
import logging
from os import getenv

import queue
import threading
from typing import Optional

import jwt


def setup_logger() -> logging.Logger:
    """função que cria logger e salva erros em arquivo txt"""
    logger = logging.getLogger("_logs")
    logger.setLevel(logging.ERROR)
    file_handler = logging.FileHandler("error_logs.txt")
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

# inicia logger globalmente
LOGGER = setup_logger()

def async_timeout(seconds: int):
    def decorator(func):
        def wrapper(*args, **kwargs):
            async def async_func():
                return await asyncio.to_thread(func, *args, **kwargs)

            def thread_func(result_queue):
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    result = loop.run_until_complete(
                        asyncio.wait_for(async_func(), timeout=seconds)
                    )
                    result_queue.put(result)
                except asyncio.TimeoutError:
                    logging.warning(f"Function {func.__name__} timed out")
                    result_queue.put(TimeoutError())
                except Exception as e:
                    logging.error(f"Function {func.__name__} raised {str(e)}")
                    result_queue.put(e)
                finally:
                    loop.close()

            result_queue = queue.Queue()
            threading.Thread(target=thread_func, args=(result_queue,)).start()
            result = result_queue.get()

            if isinstance(result, Exception):
                raise result
            return result

        return wrapper
    return decorator

def generate_password_reset_token(email: str) -> str:
    delta = datetime.timedelta(hours=getenv("RESET_TOKEN_EXPIRE_HOURS", 24))
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email}, getenv("JWT_SECRET_KEY"), algorithm="HS256",
    )
    return encoded_jwt


def verify_password_reset_token(token: str) -> Optional[str]:
    try:
        decoded_token = jwt.decode(token, getenv("JWT_SECRET_KEY"), algorithms=["HS256"])
        return decoded_token["email"]
    except jwt.JWTError:
        return None
