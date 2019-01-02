import os

from src.blue import BlueConnector
from src.media import MediaController
import subprocess as sp


def init():
    global controller, connector
    connector = BlueConnector()
    device = connector.connect()

    controller = MediaController(device)


def execute(ch):
    if ch == '1':
        controller.play()
    elif ch == '2':
        controller.stop()
    elif ch == '3':
        controller.next()
    elif ch == '4':
        controller.prevoius()
    elif ch == '5':
        print(str(connector.state))
    elif ch == 'q':
        os._exit(0)
    else:
        pass


def run():
    sp.call('clear')
    print("Connected")

    ch = ''
    while ch != 'q':
        print("What you want to do?")
        print("1) Play")
        print("2) Stop")
        print("3) Next")
        print("4) Prev")
        print("5) Now playing")
        print("q) Exit")

        ch = input("Choose: ")
        sp.call('clear', shell=True)
        execute(ch)


if __name__ == "__main__":
    init()
    run()
