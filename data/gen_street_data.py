import json
import random
import numpy as np

from utils import system_prompt
from utils import gen_output, append_conversation


def gen_dataset_street(num):
    scene_prompt = "接下来你要引导盲人进入道路对面的教学楼。你要先穿过道路，注意行人和来车。"
    function_prompt = [
        {
            "name": "get_surrounding_state",
            "description": "向底层程序获取周边的情况，会向你汇报距离1m以内的行人，距离5m以内的车辆，正前方距离1m以内的台阶。"
        }, {
            "name": "move_forward",
            "description": "向前移动。"
        }, {
            "name": "stop",
            "description": "停止移动。"
        }, {
            "name": "pass",
            "description": "不调用任何方法。"
        }, {
            "name": "climb_mode",
            "description": "普通行动模式下，切换为攀爬模式。"
        }, {
            "name": "common_mode",
            "description": "攀爬模式下，切换为普通行动模式。"
        }, {
            "name": "exit",
            "description": "结束任务。"
        }
    ]
    function_prompt = json.dumps(function_prompt, ensure_ascii=False)
    
    planning = gen_output(
        thought="接下来我要引导盲人进入道路对面的教学楼。在该过程，我会不断通过get_surrounding_state方法获取周边情况，向您提示周边障碍，并在有车辆靠近时提醒您止步等待，同时通过stop方法停止移动，直到安全再通过move_forward向前移动。遇到楼梯时，我会通过climb_mode方法切换为攀爬模式，并在通过楼梯后通过common_mode切换为普通模式。进入教学楼后，通过exit方法结束任务。",
        method="pass",
        earphone="接下来我要引导您进入道路对面的教学楼。请问您准备好了吗？"
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
            "准备好了。",
            "出发吧。",
            "让我们出发吧。"
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
                        thought="通过前面的对话，无法确认盲人是否准备好叻，我要继续询问。",
                        method="pass",
                        earphone="请问我们可以出发了吗？"
                    )
                }, add_noise_prob=0)
        
        # 盲人回答准备好了
        append_conversation(conversation, {
            "input": "[用户消息]" + random.choice(true_answer_list),
            "output": gen_output(
                thought="盲人准备好了，我要开始前进。",
                method="move_forward",
                earphone="好的，让我们出发吧。"
            )
        }, add_noise_prob=0)
        
        # 开始向前移动
        append_conversation(conversation, {
            "input": "[底层程序消息]开始向前移动。",
            "output": gen_output(
                thought="我开始向前移动了，在此过程中，我要时刻关注周围状况。",
                method="get_surrounding_state",
                earphone="我将关注周围状况，并向您提示。"
            )
        })
        
        # 通过路口，经历九九八十一难
        N = random.randint(0, 10)
        for n in range(N):
            # 有行人
            if random.random() > 0.5:
                direct = random.choice(["前方", "左方", "右方"])
                dis = random.random()
                append_conversation(conversation, {
                    "input": "[底层程序消息]{}距离{:.2f}m有行人。".format(direct, dis),
                    "output": gen_output(
                        thought="{}距离我{:.2f}m有行人。我要提醒盲人，以及行人。".format(direct, dis),
                        method="get_surrounding_state",
                        earphone="请注意，{}距离您{:.2f}m有行人。".format(direct, dis),
                        broadcast="您好，请您让一下，谢谢！"
                    )
                })
            
            # 有车辆
            if random.random() > 0.5:
                direct = random.choice(["左方", "右方"])
                dis = random.random() * 5
                append_conversation(conversation, {
                    "input": "[底层程序消息]{}距离{:.2f}m有车辆驶来。".format(direct, dis),
                    "output": gen_output(
                        thought="{}距离我{:.2f}m有车辆驶来，我要提醒盲人停止等待。".format(direct, dis),
                        method="stop",
                        earphone="请注意，{}距离您{:.2f}m有车辆驶来，请停止等待。".format(direct, dis)
                    )
                })
                
                # 停止
                append_conversation(conversation, {
                    "input": "[底层程序消息]已停止运动。",
                    "output": gen_output(
                        thought="我要继续关注车辆状况。",
                        method="get_surrounding_state"
                    )
                })
                
                # 车辆靠近
                dis -= random.random()
                while dis > 0:
                    append_conversation(conversation, {
                        "input": "[底层程序消息]{}距离{:.2f}m有车辆驶来。".format(direct, dis),
                        "output": gen_output(
                            thought="{}距离我{:.2f}m有车辆驶来，我要继续等待。".format(direct, dis),
                            method="get_surrounding_state"
                        )
                    })
                    dis -= random.random()
                
                # 车走了
                append_conversation(conversation, {
                    "input": "[底层程序消息]周围安全。",
                    "output": gen_output(
                        thought="周围已安全，我要提醒盲人继续前进。",
                        method="move_forward",
                        earphone="周围已安全，请继续前进。"
                    )
                })
                
                # 开始前进
                append_conversation(conversation, {
                    "input": "[底层程序消息]开始前进。",
                    "output": gen_output(
                        thought="我将持续关注周围状况，并向盲人提示。",
                        method="get_surrounding_state"
                    )
                })
            
            # 安全
            if random.random() > 0.5:
                append_conversation(conversation, {
                    "input": "[底层程序消息]周围安全。",
                    "output": gen_output(
                        thought="我将持续关注周围状况，并向盲人提示。",
                        method="get_surrounding_state"
                    )
                })
        
        # 到达楼梯
        append_conversation(conversation, {
            "input": "[底层程序消息]前方楼梯。",
            "output": gen_output(
                thought="前方有楼梯，我要切换为攀爬模式。",
                method="climb_mode",
                earphone="请注意，前方有楼梯！"
            )
        })
        
        append_conversation(conversation, {
            "input": "[底层程序消息]已切换为攀爬模式。",
            "output": gen_output(
                thought="我将持续关注周围状况，并向盲人提示。",
                method="get_surrounding_state"
            )
        })
        
        # 通过楼梯
        append_conversation(conversation, {
            "input": "[底层程序消息]离开楼梯。",
            "output": gen_output(
                thought="已离开楼梯，我要切换为普通模式。",
                method="common_mode",
                earphone="您已离开楼梯！"
            )
        })
        
        append_conversation(conversation, {
            "input": "[底层程序消息]已切换为普通模式。",
            "output": gen_output(
                thought="我将持续关注周围状况，并向盲人提示。",
                method="get_surrounding_state"
            )
        })
        
        # 到达
        append_conversation(conversation, {
            "input": "[底层程序消息]已进入教学楼。",
            "output": gen_output(
                thought="我已进入教学楼，停止运动。",
                method="stop"
            )
        })
        
        append_conversation(conversation, {
            "input": "[底层程序消息]已停止运动。",
            "output": gen_output(
                thought="我已引导盲人通过道路进入教学楼，任务完成。",
                method="exit",
                earphone="已引导您通过道路进入教学楼，任务完成。"
            )
        })
        
        all_conversation.append({
            "conversation": conversation
        })
        conversation = json.dumps(conversation, ensure_ascii=False)
        len_list.append(len(conversation))
    
    print("Street dataset:")
    print("Avg len:{}".format(np.mean(len_list)))
    print("Max len:{}".format(np.max(len_list)))
    print("Min len:{}".format(np.min(len_list)))
    return all_conversation


if __name__ == "__main__":
    conversation_train = gen_dataset_street(10000)
    conversation_valid = gen_dataset_street(100)
    
    conversation_train = json.dumps(conversation_train, ensure_ascii=False, indent=4)
    with open("gen/dataset_street_train.jsonl", "w") as f:
        f.write(conversation_train)
    
    conversation_valid = json.dumps(conversation_valid, ensure_ascii=False, indent=4)
    with open("gen/dataset_street_valid.jsonl", "w") as f:
        f.write(conversation_valid)
    
    
    