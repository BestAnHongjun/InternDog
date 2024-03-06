import json
import random

from gen_lift_data import gen_dataset_lift
from gen_room_data import gen_dataset_room
from gen_street_data import gen_dataset_street

gen_dataset_func = [
    gen_dataset_lift,
    gen_dataset_room,
    gen_dataset_street
]


if __name__ == "__main__":
    conversation_train = []
    for func in gen_dataset_func:
        conversation_train += func(10000)
    conversation_train = random.shuffle(conversation_train)
    
    conversation_valid = []
    for func in gen_dataset_func:
        conversation_valid += func(100)
    conversation_valid = random.shuffle(conversation_valid)
    
    conversation_train = json.dumps(conversation_train, ensure_ascii=False, indent=4)
    with open("gen/dataset_train.jsonl", "w") as f:
        f.write(conversation_train)
    
    conversation_valid = json.dumps(conversation_valid, ensure_ascii=False, indent=4)
    with open("gen/dataset_valid.jsonl", "w") as f:
        f.write(conversation_valid)