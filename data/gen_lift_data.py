import json
import random
import numpy as np

from utils import system_prompt
from utils import gen_output, append_conversation


def gen_dataset_lift(num):
    scene_prompt = "接下来你要引导盲人由电梯下楼。"
    function_prompt = [
        {
            "name": "get_door_state",
            "description": "向底层程序获取电梯门的状态，可能是开启，或关闭。"
        }, {
            "name": "get_floor_state",
            "description": "向底层程序获取电梯楼层状态。"
        }, {
            "name": "pass",
            "description": "不调用任何方法。"
        }, {
            "name": "move_in",
            "description": "进入电梯。"
        }, {
            "name": "move_out",
            "description": "离开电梯。"
        }, {
            "name": "exit",
            "description": "结束任务。"
        }
    ]
    function_prompt = json.dumps(function_prompt, ensure_ascii=False)
    
    planning = gen_output(
        thought="我首先要向盲人询问目标楼层；然后通过get_door_state方法确认电梯门的状态；直到电梯门开启，通过move_in方法进入电梯。进入电梯后，通过get_floor_state方法获取电梯当前的楼层；直到到达指定楼层后，通过get_door_state方法确认电梯门的状态；直到电梯门开启，通过move_out方法离开电梯。最后，通过exit方法结束任务。",
        method="pass",
        earphone="接下来我要引导您由电梯下楼。请问您准备去几楼呀？"
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
        
        # 盲人回答要去哪一层楼
        target_floor = random.randint(1, 100)
        true_answer_list = [
            "我准备去{}楼。",
            "{}楼。",
            "我想去{}楼。",
            "我要去{}楼，谢谢。",
            "我要去{}楼。"
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
                        thought="前面的对话无法确认盲人想去几楼，我需要重新询问。",
                        method="pass",
                        earphone="请问您想去几楼？"
                    )
                }, add_noise_prob=0)
        
        # 盲人回答去几楼
        append_conversation(conversation, {
            "input": "[用户消息]" + random.choice(true_answer_list).format(target_floor),
            "output": gen_output(
                thought="通过前面的对话，我得知盲人想去{}楼。我要请求盲人按下电梯按钮，并等待电梯门开启。".format(target_floor),
                method="get_door_state",
                earphone="好的，您想去{}楼。请您按下电梯按钮，我将等待电梯门开启时引导您进入。".format(target_floor)
            )
        }, add_noise_prob=0)
        
        # 循环询问N次,等待门开
        N = random.randint(0, 5)
        for n in range(N):            
            append_conversation(conversation, {
                "input": "[底层程序消息]门没开。",
                "output": gen_output(
                    thought="盲人想去{}楼。门还没有开，我要继续等待。".format(target_floor),
                    method="get_door_state"
                )
            })
            
        # 门开了
        append_conversation(conversation, {
            "input": "[底层程序消息]门开了。",
            "output": gen_output(
                thought="盲人想去{}楼。门开了，我需要让盲人进入电梯。".format(target_floor),
                method="move_in",
                earphone="门开了，请进入电梯。"
            )
        })
        
        # 进入电梯
        append_conversation(conversation, {
            "input": "[底层程序消息]已进入电梯。",
            "output": gen_output(
                thought="盲人想去{}楼。盲人已经进入了电梯，我需要在到达{}楼时提醒盲人离开电梯。".format(target_floor, target_floor),
                method="get_floor_state",
                earphone="您已进入电梯。我将在到达{}楼时提醒您。".format(target_floor)
            )
        })
        
        # 循环询问N次，等待到达特定楼层
        N = random.randint(0, 5)
        for n in range(N):
            floor = random.randint(1, 100)
            if floor == target_floor:
                break
            append_conversation(conversation, {
                "input": "[底层程序消息]已到达{}楼。".format(floor),
                "output": gen_output(
                    thought="盲人想去{}楼。当前是{}楼，不是{}楼，我要提醒盲人耐心等待。".format(target_floor, floor, target_floor),
                    method="get_floor_state",
                    earphone="注意，当前是{}楼，不是{}楼，请您耐心等待。".format(floor, target_floor)
                )
            })
            
        
        # 到达楼层
        append_conversation(conversation, {
            "input": "[底层程序消息]已到达{}楼。".format(target_floor),
            "output": gen_output(
                thought="盲人想去{}楼。当前已到达{}楼，我要提醒盲人等待电梯门开启。".format(target_floor, target_floor),
                method="get_door_state",
                earphone="请注意，当前已到达{}楼，请等待电梯门开启。".format(target_floor),
            )
        })
        
        # 等待电梯门开启
        N = random.randint(0, 5)
        for n in range(N):
            append_conversation(conversation, {
                "input": "[底层程序消息]门没开。",
                "output": gen_output(
                    thought="当前已到达目标楼层。门还没有开，我要继续等待。",
                    method="get_door_state"
                )
            })

        # 门开了
        append_conversation(conversation, {
            "input": "[底层程序消息]门开了。",
            "output": gen_output(
                thought="当前已到达目标楼层。门开了，我要提醒盲人离开电梯。",
                method="move_out",
                earphone="门开了，请离开电梯。"
            )
        })        

        # 离开电梯
        append_conversation(conversation, {
            "input": "[底层程序消息]已离开电梯。",
            "output": gen_output(
                thought="当前已到达目标楼层。盲人离开了电梯，任务完成。",
                method="exit",
                earphone="好的，您已离开电梯，任务完成。"
            )
        })
        
        all_conversation.append({
            "conversation": conversation
        })
        conversation = json.dumps(conversation, ensure_ascii=False)
        len_list.append(len(conversation))
    
    print("Lift dataset:")
    print("Avg len:{}".format(np.mean(len_list)))
    print("Max len:{}".format(np.max(len_list)))
    print("Min len:{}".format(np.min(len_list)))
    return all_conversation


if __name__ == "__main__":
    conversation_train = gen_dataset_lift(10000)
    conversation_valid = gen_dataset_lift(100)
    
    conversation_train = json.dumps(conversation_train, ensure_ascii=False, indent=4)
    with open("gen/dataset_lift_train.jsonl", "w") as f:
        f.write(conversation_train)
    
    conversation_valid = json.dumps(conversation_valid, ensure_ascii=False, indent=4)
    with open("gen/dataset_lift_valid.jsonl", "w") as f:
        f.write(conversation_valid)
    
    
    