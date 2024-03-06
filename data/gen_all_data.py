import json
import random

from utils import basic_info, system_prompt
from utils import gen_output
from gen_lift_data import gen_dataset_lift
from gen_room_data import gen_dataset_room
from gen_street_data import gen_dataset_street

gen_dataset_func = [
    gen_dataset_lift,
    gen_dataset_room,
    gen_dataset_street
]


if __name__ == "__main__":
    add_conv = random.choice(basic_info)

    conversation_train = []
    for add_conv in basic_info:
        conversation_train.append({"conversation": [{
            "system": system_prompt, 
            "input": add_conv["input"],
            "output": gen_output(
                thought="我要回答盲人询问我的问题。",
                method="pass",
                earphone=add_conv["output"]
            )
        }]})
    for func in gen_dataset_func:
        conversation_train += func(10000)
    random.shuffle(conversation_train)
    
    conversation_valid = []
    for add_conv in basic_info:
        conversation_valid.append({"conversation": [{
            "system": system_prompt, 
            "input": add_conv["input"],
            "output": gen_output(
                thought="我要回答盲人询问我的问题。",
                method="pass",
                earphone=add_conv["output"]
            )
        }]})
    for func in gen_dataset_func:
        conversation_valid += func(100)
    random.shuffle(conversation_valid)
    
    conversation_train = json.dumps(conversation_train, ensure_ascii=False, indent=4)
    with open("gen/dataset_train.jsonl", "w") as f:
        f.write(conversation_train)
    
    conversation_valid = json.dumps(conversation_valid, ensure_ascii=False, indent=4)
    with open("gen/dataset_valid.jsonl", "w") as f:
        f.write(conversation_valid)