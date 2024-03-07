import gradio as gr
from tqdm import tqdm
import time

from agent.config import wait_time
from agent.utils import return_to_web_demo


task_room_prompt = """[底层程序消息]接下来你要引导盲人去特定房间。你可以调用的方法有：[{"name": "get_door_info", "description": "获取检测到的门牌信息，以及门牌的方向(左边或右边)。"}, {"name": "move_forward", "description": "向前移动。"}, {"name": "stop", "description": "停止移动。"}, {"name": "det_door", "description": "检测是否有门牌。"}, {"name": "turn_left", "description": "向左旋转90度。"}, {"name": "turn_right", "description": "向右旋转90度。"}, {"name": "pass", "description": "不调用任何方法。"}, {"name": "exit", "description": "结束任务。"}]"""


def get_door_info(message="", chat_history=[], chat_history_clear=[], prompt="", task_id=-1, cli=True):
    if cli:
        print("[情景模拟]")
        print("InternDog刚刚检测到了门牌！")
        print("现在，由您来充当底层程序，您可以决定InternDog看到的门牌信息。")
        print("InternDog看到的门牌号是？（输入一个三位数或四位数，比如605，1104，1501……）")
        room = input("[你的输入] >>> ")
        while True:
            direct = input("------\n好的，InternDog看到的门牌号是{}。请问他在InternDog的左侧还是右侧？(输入0或1，0代表左侧，1代表右侧。)\n[你的输入] >>> ".format(room))
            if not direct.isdigit():
                print("!!!!警告：输入格式错误!!!")
                continue 
            direct = int(direct)
            if direct == 0:
                direct = "左"
                break
            elif direct == 1:
                direct = "右"
                break
            else:
                print("!!!!警告：输入格式错误!!!")
                continue
        message = "[底层程序消息]{}边检测到门牌号{}。".format(direct, room)
        return message
    else:
        return return_to_web_demo(
            message, chat_history, chat_history_clear, prompt, task_id,
            controller_room_get_door_info=gr.update(visible=True)
        )


def move_forward(message="", chat_history=[], chat_history_clear=[], prompt="", task_id=-1, cli=True):
    if cli:
        print("[情景]导盲犬开始向前移动...")
        for i in tqdm(range(wait_time)):
            time.sleep(0.1)
        message = "[底层程序消息]开始向前移动。"
        return message
    else:
        return return_to_web_demo(
            message, chat_history, chat_history_clear, prompt, task_id,
            controller_common=gr.update(visible=True),
            controller_common_method=gr.update(value="模型向底层程序调用了`move_forward`方法"),
            controller_common_message=gr.update(value="[底层程序消息]开始向前移动。")
        )


def stop(message="", chat_history=[], chat_history_clear=[], prompt="", task_id=-1, cli=True):
    if cli:
        print("[情景]导盲犬正在停止运动...")
        for i in tqdm(range(wait_time)):
            time.sleep(0.1)
        message = "[底层程序消息]已停止运动。"
        return message
    else:
        return return_to_web_demo(
            message, chat_history, chat_history_clear, prompt, task_id,
            controller_common=gr.update(visible=True),
            controller_common_method=gr.update(value="模型向底层程序调用了`stop`方法"),
            controller_common_message=gr.update(value="[底层程序消息]已停止运动。")
        )


def det_door(message="", chat_history=[], chat_history_clear=[], prompt="", task_id=-1, cli=True):
    if cli:
        while True:
            print("[情景模拟]")
            answer = input("InternDog正在走廊中向前移动，并在移动的过程中检测左右两边是否有门牌。\n现在，由您来充当底层程序，您可以决定InternDog是否检测到门牌。\nInternDog检测到门牌了吗？（输入0或1，0代表没看到，1代表看到了。）\n[你的输入] >>> ")
            if not answer.isdigit():
                print("!!!!警告：输入格式错误!!!")
                continue 
            answer = int(answer)
            if answer == 0:
                message = "[底层程序消息]没有检测到门牌信息。"
                break
            elif answer == 1:
                message = "[底层程序消息]检测到门牌信息。"
                break
            else:
                print("!!!!警告：输入格式错误!!!")
                continue
        return message
    else:
        return return_to_web_demo(
            message, chat_history, chat_history_clear, prompt, task_id, 
            controller_room_det_door=gr.update(visible=True)
        )


def turn_left(message="", chat_history=[], chat_history_clear=[], prompt="", task_id=-1, cli=True):
    if cli:
        print("[情景]导盲犬正在向左转向...")
        for i in tqdm(range(wait_time)):
            time.sleep(0.1)
        message = "[底层程序消息]已向左转向。"
        return message
    else:
        return return_to_web_demo(
            message, chat_history, chat_history_clear, prompt, task_id,
            controller_common=gr.update(visible=True),
            controller_common_method=gr.update(value="模型向底层程序调用了`turn_left`方法"),
            controller_common_message=gr.update(value="[底层程序消息]已向左转向。")
        )


def turn_right(message="", chat_history=[], chat_history_clear=[], prompt="", task_id=-1, cli=True):
    if cli:
        print("[情景]导盲犬正在向右转向...")
        for i in tqdm(range(wait_time)):
            time.sleep(0.1)
        message = "[底层程序消息]已向右转向。"
        return message
    else:
        return return_to_web_demo(
            message, chat_history, chat_history_clear, prompt, task_id,
            controller_common=gr.update(visible=True),
            controller_common_method=gr.update(value="模型向底层程序调用了`turn_right`方法"),
            controller_common_message=gr.update(value="[底层程序消息]已向右转向。")
        )
