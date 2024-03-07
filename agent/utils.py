import os
import json
import gradio as gr
from datetime import datetime

from agent.model import chat
from agent.config import chat_prompt_template


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


def return_to_web_demo(
    message,
    chat_history,
    chat_history_clear,
    prompt,
    task_id,
    user_msg=gr.update(interactive=True, value="", placeholder=""),
    user_msg_submid=gr.update(interactive=True),
    controller_select=gr.update(visible=False),
    controller_pass=gr.update(visible=False),
    controller_common=gr.update(visible=False),
    controller_common_method=gr.update(value=""),
    controller_common_message=gr.update(value=""),
    controller_lift_get_door_state=gr.update(visible=False),
    controller_lift_get_floor_state=gr.update(visible=False),
    controller_room_get_door_info=gr.update(visible=False),
    controller_room_det_door=gr.update(visible=False),
    controller_street_get_surrounding_state=gr.update(visible=False),
    keep=False
):
    if keep:
        user_msg=gr.update(elem_id="user_msg")
        user_msg_submid=gr.update(elem_id="user_msg_submit")
        controller_select=gr.update(elem_id="controller_select")
        controller_pass=gr.update(elem_id="controller_pass")
        controller_common=gr.update(elem_id="controller_common")
        controller_common_method=gr.update(elem_id="controller_common_method")
        controller_common_message=gr.update(elem_id="controller_common_message")
        controller_lift_get_door_state=gr.update(elem_id="controller_lift_get_door_state")
        controller_lift_get_floor_state=gr.update(elem_id="controller_lift_get_floor_state")
        controller_room_get_door_info=gr.update(elem_id="controller_room_get_door_info")
        controller_room_det_door=gr.update(elem_id="controller_room_det_door")
        controller_street_get_surrounding_state=gr.update(elem_id="controller_street_get_surrounding_state")
    return (
        gr.update(value=message),
        user_msg, 
        user_msg_submid,
        gr.update(value=chat_history),
        gr.update(value=chat_history_clear),
        controller_select,
        controller_pass,
        controller_common,
        controller_common_method,
        controller_common_message,
        gr.update(value=prompt),
        gr.update(value=task_id),
        controller_lift_get_door_state,
        controller_lift_get_floor_state,
        controller_room_get_door_info,
        controller_room_det_door,
        controller_street_get_surrounding_state
    )


def analysis_response(response_dict):
    message = "* **InternDog当前内心的想法**:" + response_dict["thought"] + "\n"
    message += "* **InternDog当前调用的方法**:" + response_dict["method"] + "\n"
    message += "* **InternDog通过扬声器广播**:" + response_dict["broadcast"] + "\n"
    message += "* **InternDog通过耳机对你说**:" + response_dict["earphone"]
    return message


def processor(msg, chat_history, chat_history_clear, task_funcs, prompt, task_id):
    prompt += chat_prompt_template.format(msg)
    prompt, response, response_dict = chat(prompt)
    message = analysis_response(response_dict)
    chat_history.append((msg, response))
    if response_dict["earphone"]:
        chat_history_clear.append((msg, response_dict["earphone"]))
    else:
        chat_history_clear.append((msg, None))
    if response_dict["method"] == "pass":
        return return_to_web_demo(
            message, chat_history, chat_history_clear,
            prompt, task_id, keep=True
        )
    elif response_dict["method"] == "exit":
        return return_to_web_demo(
            message, chat_history, chat_history_clear, prompt, task_id,
            user_msg=gr.update(interactive=False, placeholder="请先通过右侧选择一个模拟情景。", value=""),
            user_msg_submid=gr.update(interactive=False),
            controller_select=gr.update(visible=True)
        )
    elif response_dict["method"] in task_funcs[int(task_id)].keys():
        return task_funcs[int(task_id)][response_dict["method"]](message, chat_history, chat_history_clear, prompt, task_id, cli=False)
    else:
        pass