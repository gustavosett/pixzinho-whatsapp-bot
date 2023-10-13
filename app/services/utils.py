"""
    Esse código guarda todas funções utilitárias para a aplicação.

author: github.com/gustavosett 
"""

import asyncio
import logging

import queue
import threading


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