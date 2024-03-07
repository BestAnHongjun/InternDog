import random
from agent.utils import processor

from agent.task_room_funcs import task_room_prompt
from agent.task_lift_funcs import task_lift_prompt
from agent.task_street_funcs import task_street_prompt

from agent.task_room_funcs import get_door_info as room_get_door_info
from agent.task_room_funcs import move_forward as room_move_forward
from agent.task_room_funcs import stop as room_stop
from agent.task_room_funcs import det_door as room_det_door
from agent.task_room_funcs import turn_left as room_turn_left
from agent.task_room_funcs import turn_right as room_turn_right

from agent.task_lift_funcs import get_door_state as lift_get_door_state
from agent.task_lift_funcs import get_floor_state as lift_get_floor_state
from agent.task_lift_funcs import move_in as lift_move_in 
from agent.task_lift_funcs import move_out as lift_move_out

from agent.task_street_funcs import get_surrounding_state as street_get_surrounding_state
from agent.task_street_funcs import move_forward as street_move_forward
from agent.task_street_funcs import stop as street_stop
from agent.task_street_funcs import climb_mode as street_climb_mode
from agent.task_street_funcs import common_mode as street_common_mode


task_prompt = [
    task_room_prompt,
    task_lift_prompt,
    task_street_prompt
]

task_funcs = [
    {
        "get_door_info": room_get_door_info,
        "move_forward": room_move_forward,
        "stop": room_stop,
        "det_door": room_det_door,
        "turn_left": room_turn_left,
        "turn_right": room_turn_right
    }, {
        "get_door_state": lift_get_door_state,
        "get_floor_state": lift_get_floor_state,
        "move_in": lift_move_in,
        "move_out": lift_move_out
    }, {
        "get_surrounding_state": street_get_surrounding_state,
        "move_forward": street_move_forward,
        "stop": street_stop,
        "climb_mode": street_climb_mode,
        "common_mode": street_common_mode
    }
]

def web_room_get_door_info(state, direct, chat_history,chat_history_clear, prompt, task_id):
    if direct == "左侧":
        direct = "左"
    else:
        direct = "右"
    msg = "[底层程序消息]{}边检测到门牌号{}。".format(direct, int(state))
    return processor(msg, chat_history, chat_history_clear, task_funcs, prompt, task_id)


def web_room_det_door(state, chat_history, chat_history_clear, prompt, task_id):
    if state == "检测到了":
        msg = "[底层程序消息]检测到门牌信息。"
    else:
        msg = "[底层程序消息]没有检测到门牌信息。"
    return processor(msg, chat_history, chat_history_clear, task_funcs, prompt, task_id)


def web_lift_get_door_state(state, chat_history, chat_history_clear, prompt, task_id):
    if state == "门开了":
        msg = "[底层程序消息]门开了。"
    else:
        msg = "[底层程序消息]门没开。"
    return processor(msg, chat_history, chat_history_clear, task_funcs, prompt, task_id)


def web_lift_get_floor_state(state, chat_history, chat_history_clear, prompt, task_id):
    msg = "[底层程序消息]已到达{}楼。".format(int(state))
    return processor(msg, chat_history, chat_history_clear, task_funcs, prompt, task_id)


def web_street_get_surrounding_state(state, chat_history, chat_history_clear, prompt, task_id):
    if state == "周围安全":
        msg = "[底层程序消息]周围安全。"
    elif state == "周围1m内有人":
        direct = random.choice(["左", "右"])
        msg =  "[底层程序消息]{}方距离{:.2f}m有行人。".format(direct, random.random())
    elif state == "周围5m内有车":
        direct = random.choice(["左", "右"])
        msg = "[底层程序消息]{}方距离{:.2f}m有车辆驶来。".format(direct, random.random() * 5)
    elif state == "前方有楼梯":
        msg = "[底层程序消息]前方楼梯。"
    elif state == "已离开楼梯":
        msg = "[底层程序消息]离开楼梯。"
    else:
        msg = "[底层程序消息]已进入教学楼。"
    return processor(msg, chat_history, chat_history_clear, task_funcs, prompt, task_id)
    