import random
import threading
import pytest
import time
from app.services.utils import async_timeout

def slow_function():
    time.sleep(10)
    return "Finished"

def fast_function():
    return "Finished Quickly"

def error_function():
    raise ValueError("Some error occurred")

@pytest.mark.timeout(15)
def test_slow_function_timeout():
    """Testa se a função lenta é interrompida após o timeout"""
    @async_timeout(5)
    def wrapped_slow_function():
        return slow_function()

    with pytest.raises(TimeoutError):
        wrapped_slow_function()

def test_fast_function():
    """Testa se a função rápida executa corretamente sem ser interrompida"""
    @async_timeout(5)
    def wrapped_fast_function():
        return fast_function()
    
    assert wrapped_fast_function() == "Finished Quickly"

def test_error_function():
    """Testa se a função que lança uma exceção propaga o erro corretamente"""
    @async_timeout(5)
    def wrapped_error_function():
        return error_function()
    
    with pytest.raises(ValueError, match="Some error occurred"):
        wrapped_error_function()

def test_function_with_arguments():
    """Testa se a função decorada aceita argumentos e retorna o esperado"""
    @async_timeout(5)
    def wrapped_function_with_arguments(arg1, arg2):
        return arg1 + arg2
    
    assert wrapped_function_with_arguments(3, 4) == 7


def test_function_with_keyword_arguments():
    """Testa se a função decorada aceita argumentos nomeados e retorna o esperado"""
    @async_timeout(5)
    def wrapped_function_with_keyword_arguments(arg1, arg2):
        return arg1 * arg2
    
    assert wrapped_function_with_keyword_arguments(arg1=3, arg2=4) == 12


def test_multiple_function_calls():
    """Testa se a função decorada pode ser chamada múltiplas vezes"""
    @async_timeout(5)
    def wrapped_function_to_call_multiple_times(arg):
        return arg * 2
    
    assert wrapped_function_to_call_multiple_times(3) == 6
    assert wrapped_function_to_call_multiple_times(4) == 8
    assert wrapped_function_to_call_multiple_times(5) == 10


def test_variable_execution_time_function():
    """Testa se a função decorada lida corretamente com funções de tempo de execução variável"""
    @async_timeout(5)
    def wrapped_variable_execution_time_function(wait_time):
        time.sleep(wait_time)
        return "Finished"
    
    assert wrapped_variable_execution_time_function(1) == "Finished"
    
    with pytest.raises(TimeoutError):
        wrapped_variable_execution_time_function(10)

def test_to_flood_executions_on_decorator_and_do_not_freeze_the_system():
    """Testa se o decorador pode lidar com 1.000 execuções simultâneas sem congelar o sistema"""
    @async_timeout(5)
    def wrapped_variable_execution_time_function(wait_time):
        time.sleep(wait_time)
        return "Finished"
    
    def run_in_thread():
        # Gera um tempo de sono aleatório entre 1 e 10 segundos
        sleep_time = random.uniform(1, 10)
        try:
            wrapped_variable_execution_time_function(sleep_time)
        except TimeoutError:
            pass
    
    # Inicia 1.000 threads, cada uma executando a função decorada
    threads = [threading.Thread(target=run_in_thread) for _ in range(1000)]

    # Inicia todas as threads
    for thread in threads:
        thread.start()

    # Espera todas as threads terminarem
    for thread in threads:
        thread.join()

    # Verifica se o sistema ainda está responsivo executando uma função com um tempo de espera curto
    @async_timeout(5)
    def wrapped_quick_function():
        time.sleep(1)
        return "Finished Quickly"
    
    assert wrapped_quick_function() == "Finished Quickly"
