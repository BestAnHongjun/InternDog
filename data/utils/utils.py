import json
import random

from .basic import basic_info


def gen_output(thought, method, earphone="", broadcast=""):
    output = {
        "thought": thought,
        "method": method,
        "earphone": earphone,
        "broadcast": broadcast
    }
    output = json.dumps(output, ensure_ascii=False)
    return output


def append_conversation(history_conversation, new_conversation, add_noise_prob=0.5):
    if random.random() < add_noise_prob:
        add_conv = random.choice(basic_info)
        history_conversation.append({
            "input": add_conv["input"],
            "output": gen_output(
                thought="我要回答盲人询问我的问题。",
                method="pass",
                earphone=add_conv["output"]
            )
        })
    history_conversation.append(new_conversation)
    