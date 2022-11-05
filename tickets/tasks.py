from time import sleep

from test_innowise.celery import app


@app.task
def hello_world():
    sleep(10)  # поставим тут задержку в 10 сек для демонстрации ассинхрности
    print('Hello World')
