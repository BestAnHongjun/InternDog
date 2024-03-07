from agent.utils import *
import agent.task_room_funcs
import agent.task_lift_funcs
import agent.task_street_funcs

from agent.config import system_prompt_template, chat_prompt_template

task_prompt = [
    agent.task_room_funcs.task_room_prompt,
    agent.task_lift_funcs.task_lift_prompt,
    agent.task_street_funcs.task_street_prompt
]

task_funcs = [
    {
        "get_door_info": agent.task_room_funcs.get_door_info,
        "move_forward": agent.task_room_funcs.move_forward,
        "stop": agent.task_room_funcs.stop,
        "det_door": agent.task_room_funcs.det_door,
        "turn_left": agent.task_room_funcs.turn_left,
        "turn_right": agent.task_room_funcs.turn_right
    }, {
        "get_door_state": agent.task_lift_funcs.get_door_state,
        "get_floor_state": agent.task_lift_funcs.get_floor_state,
        "move_in": agent.task_lift_funcs.move_in,
        "move_out": agent.task_lift_funcs.move_out
    }, {
        "get_surrounding_state": agent.task_street_funcs.get_surrounding_state,
        "move_forward": agent.task_street_funcs.move_forward,
        "stop": agent.task_street_funcs.stop,
        "climb_mode": agent.task_street_funcs.climb_mode,
        "common_mode": agent.task_street_funcs.common_mode
    }
]