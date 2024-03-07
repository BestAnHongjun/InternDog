import os
from datetime import datetime


def print_history(chat_history, response_dict):
    os.system('cls' if os.name == 'nt' else 'clear')
    if len(chat_history) <= 6:
        for chat in chat_history: print(chat)
    else:
        for chat in chat_history[:2]: print(chat)
        print("...(省略{}条对话)...".format(len(chat_history) - 6))
        for chat in chat_history[-4:]: print(chat)
    print("\n↑↑历史消息↑↑\n-----------")
    print("InternDog当前的内心想法：", response_dict["thought"])
    print("InternDog当前调用的方法：", response_dict["method"])
    print("InternDog通过扬声器广播：", response_dict["broadcast"] if response_dict["broadcast"] else "无")
    print("InternDog通过耳机对你说：", response_dict["earphone"] if response_dict["earphone"] else "无")
    print("-----------")


def add_chat_history(chat_history, source, message):
    chat_history.append("[{} {}] >>> {}\n\n".format(datetime.now().strftime("%H:%M:%S"), source, message))
    