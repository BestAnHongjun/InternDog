from tqdm import tqdm 
import time 

from agent.config import wait_time


task_lift_prompt = """[底层程序消息]接下来你要引导盲人由电梯下楼。你可以调用的方法有：[{"name": "get_door_state", "description": "向底层程序获取电梯门的状态，可能是开启，或关闭。"}, {"name": "get_floor_state", "description": "向底层程序获取电梯楼层状态。"}, {"name": "pass", "description": "不调用任何方法。"}, {"name": "move_in", "description": "进入电梯。"}, {"name": "move_out", "description": "离开电梯。"}, {"name": "exit", "description": "结束任务。"}]"""


def get_door_state(cli=True):
    if cli:
        print("[情景模拟]")
        print("InternDog正在检测电梯门是否开启！")
        print("现在，有您来充当底层程序。您可以将检测结果告诉InternDog。")
        print("电梯门开了吗？(输入0代表门没开，输入1代表门开了。)")
        while True:
            inp = input("[你的输入] >>> ")
            if not inp.isdigit():
                print("!!!!警告：输入格式错误!!!")
                continue 
            inp = int(inp)
            if inp == 0:
                message = "[底层程序消息]门没开。"
                break
            elif inp == 1:
                message = "[底层程序消息]门开了。"
                break
            else:
                print("!!!!警告：输入格式错误!!!")
                continue
        return message 


def get_floor_state(cli=True):
    if cli:
        print("[情景模拟]")
        print("InternDog正在检测当前电梯到达的楼层！")
        print("现在，有您来充当底层程序。您可以将检测结果告诉InternDog。")
        print("现在到几楼了？(输入1-99之间的整数。)")
        while True:
            inp = input("[你的输入] >>> ")
            if not inp.isdigit():
                print("!!!!警告：输入格式错误!!!")
                continue 
            inp = int(inp)
            if inp >= 1 and inp < 100:
                message = "[底层程序消息]已到达{}楼。".format(inp)
                break
            else:
                print("!!!!警告：输入格式错误!!!")
                continue
        return message 


def move_in(cli=True):
    if cli:
        print("[情景]导盲犬正在进入电梯...")
        for i in tqdm(range(wait_time)):
            time.sleep(0.1)
        message = "[底层程序消息]已进入电梯。"
        return message


def move_out(cli=True):
    if cli:
        print("[情景]导盲犬正在离开电梯...")
        for i in tqdm(range(wait_time)):
            time.sleep(0.1)
        message = "[底层程序消息]已离开电梯。"
        return message
    