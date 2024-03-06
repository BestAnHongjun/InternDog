import json
import random
import numpy as np

from utils import system_prompt
from utils import gen_output, append_conversation


def gen_dataset_room(num):
    scene_prompt = "接下来你要引导盲人去特定房间。"
    function_prompt = [
        {
            "name": "get_door_info",
            "description": "获取检测到的门牌信息，以及门牌的方向(左边或右边)。"
        }, {
            "name": "move_forward",
            "description": "向前移动。"
        }, {
            "name": "stop",
            "description": "停止移动。"
        }, {
            "name": "det_door",
            "description": "检测是否有门牌。"
        }, {
            "name": "turn_left",
            "description": "向左旋转90度。"
        }, {
            "name": "turn_right",
            "description": "向右旋转90度。"
        }, {
            "name": "pass",
            "description": "不调用任何方法。"
        }, {
            "name": "exit",
            "description": "结束任务。"
        }
    ]
    function_prompt = json.dumps(function_prompt, ensure_ascii=False)
    
    planning = gen_output(
        thought="我要引导盲人去特定房间。我首先要向您询问目标房间；然后通过move_forward方法开始向前移动；移动过程中，通过det_door方法检测是否有门牌，如果有门牌，则通过stop方法停止移动，并通过get_door_info方法获取门牌信息。如果不是目标房间，则循环上述过程；如果是目标房间，则结合门牌的方位信息，通过turn_left或者turn_right进行转向，然后通过exit方法结束任务。",
        method="pass",
        earphone="接下来我会引导您去特定房间。请问您要去哪个房间？"
    )
    
    all_conversation = []
    len_list = []
    
    for i in range(num):
        conversation = []
        append_conversation(conversation, {
            "system": system_prompt,
            "input": "[底层程序消息]" + scene_prompt + "你可以调用的方法有：" + function_prompt,
            "output": planning
        }, add_noise_prob=0)
        
        # 盲人回答要去哪一个房间
        target_floor = random.randint(1, 90)
        target_id = random.randint(1, 90)
        target_room = "{}{:02d}".format(target_floor, target_id)
        true_answer_list = [
            "我准备去{}。",
            "{}。",
            "我想去{}。",
            "我要去{}，谢谢。",
            "我要去{}。"
        ]
        false_answer_list = [
            "啊？",
            "啊？什么？",
            "对不起，没听清。",
            "什么？"
        ]
        
        # 有一定几率盲人没听清, 循环询问N次
        N = random.randint(0, 5)
        for n in range(N):
            if random.random() > 0.5:
                append_conversation(conversation, {
                    "input": "[用户消息]" + random.choice(false_answer_list),
                    "output": gen_output(
                        thought="通过前面的对话，无法得知盲人要去哪个房间。我要继续向盲人询问。",
                        method="pass",
                        earphone="请问您想去哪个房间？"
                    )
                }, add_noise_prob=0)
        
        # 盲人回答要去哪个房间
        append_conversation(conversation, {
            "input": "[用户消息]" + random.choice(true_answer_list).format(target_room),
            "output": gen_output(
                thought="盲人想去{}。我要开始向前移动。".format(target_room),
                method="move_forward",
                earphone="好的，您想去{}。请跟随我向前移动。".format(target_room)
            )
        }, add_noise_prob=0)
        
        # 循环找M个房间
        M = random.randint(1, 10)
        for m in range(M):
            append_conversation(conversation, {
                "input": "[底层程序消息]开始向前移动。",
                "output": gen_output(
                    thought="盲人想去{}。开始向前移动，检测门牌信息。".format(target_room),
                    method="det_door"
                )
            })
            
            # 循环N次，检测门牌
            N = random.randint(0, 5)
            for n in range(N):
                append_conversation(conversation, {
                    "input": "[底层程序消息]没有检测到门牌信息。",
                    "output": gen_output(
                        thought="盲人想去{}。暂时没有检测到门牌信息，继续向前移动。".format(target_room),
                        method="det_door"
                    )
                })
                
            # 检测到门牌信息
            append_conversation(conversation, {
                "input": "[底层程序消息]检测到门牌信息。",
                "output": gen_output(
                    thought="盲人想去{}。检测到门牌信息，停止运动。我要确认是否是目标房间。".format(target_room),
                    method="stop"
                )
            })
            
            # 停止运动
            append_conversation(conversation, {
                "input": "[底层程序消息]已停止运动。",
                "output": gen_output(
                    thought="盲人想去{}。我正在确认是否是目标房间。".format(target_room),
                    method="get_door_info"
                )
            })
            
            if m == M - 1:
                break
            
            # 左边/右边
            tmp_id = random.randint(1, 90)
            while tmp_id == target_id:
                tmp_id = random.randint(1, 90)
            tmp_room = "{}{:02d}".format(target_floor, tmp_id)
            if random.randint(1, 2) == 1:
                direct = random.choice(["左", "右"])
                append_conversation(conversation, {
                    "input": "[底层程序消息]{}边检测到门牌号{}。".format(direct, tmp_room),
                    "output": gen_output(
                        thought="盲人想去{}。{}边检测到门牌号{}，盲人要去的房间是{}，当前没有到达目标房间，继续向前移动。".format(target_room, direct, tmp_room, target_room),
                        method="move_forward"
                    )
                })
            else:
                new_id = random.randint(1, 90)
                while new_id == tmp_id or new_id == target_id:
                    new_id = random.randint(1, 90)
                new_room = "{}{:02d}".format(target_floor, new_id)
                append_conversation(conversation, {
                    "input": "[底层程序消息]左边检测到门牌号{}，右边检测到门牌号{}。".format(tmp_room, new_room),
                    "output": gen_output(
                        thought="盲人想去{}。左边检测到门牌号{}，右边检测到门牌号{}, 盲人要去的房间是{}，当前没有到达目标房间，继续向前移动。".format(target_room, tmp_room, new_room, target_room),
                        method="move_forward"
                    )
                })
        
        # 找到了特定房间
        direct = random.choice(["左", "右"])
        if direct == "左":
            direct_method = "turn_left"
        else:
            direct_method = "turn_right"
        if random.randint(1, 2) == 1:
            append_conversation(conversation, {
                "input": "[底层程序消息]{}边检测到门牌号{}。".format(direct, target_room),
                "output": gen_output(
                    thought="盲人想去{}。{}边检测到盲人想去的房间{}，我要向{}转向。".format(target_room, direct, target_room, direct),
                    method=direct_method,
                    earphone="{}边检测到您想去的房间{}，向{}转向。".format(direct, target_room, direct)
                )
            })
        else:
            tmp_id = random.randint(1, 90)
            while tmp_id == target_id:
                tmp_id = random.randint(1, 90)
            tmp_room = "{}{:02d}".format(target_floor, tmp_id)
            if direct == "左":
                inp = "[底层程序消息]左边检测到门牌号{}，右边检测到门牌号{}。".format(target_room, tmp_room)
            else:
                inp = "[底层程序消息]左边检测到门牌号{}，右边检测到门牌号{}。".format(tmp_room, target_room)
            append_conversation(conversation, {
                "input": inp, 
                "output": gen_output(
                    thought="盲人想去{}。{}边检测到盲人想去的房间{}，我要向{}转向。".format(target_room, direct, target_room, direct),
                    method=direct_method,
                    earphone="{}边检测到您想去的房间{}，向{}转向。".format(direct, target_room, direct)
                )
            })
        
        # 完成转向
        append_conversation(conversation, {
            "input": "[底层程序消息]已向{}转向。".format(direct),
            "output": gen_output(
                thought="盲人想去{}。已到达目标房间{}，任务完成。".format(target_room, target_room),
                method="exit",
                earphone="已到达目标房间，任务完成。"
            )
        })
        
        all_conversation.append({
            "conversation": conversation
        })
        conversation = json.dumps(conversation, ensure_ascii=False)
        len_list.append(len(conversation))
    
    print("Room dataset:")
    print("Avg len:{}".format(np.mean(len_list)))
    print("Max len:{}".format(np.max(len_list)))
    print("Min len:{}".format(np.min(len_list)))
    return all_conversation


if __name__ == "__main__":
    conversation_train = gen_dataset_room(10000)
    conversation_valid = gen_dataset_room(100)
    
    conversation_train = json.dumps(conversation_train, ensure_ascii=False, indent=4)
    with open("gen/dataset_room_train.jsonl", "w") as f:
        f.write(conversation_train)
    
    conversation_valid = json.dumps(conversation_valid, ensure_ascii=False, indent=4)
    with open("gen/dataset_room_valid.jsonl", "w") as f:
        f.write(conversation_valid)
    