import json
from lmdeploy import turbomind as tm
from agent.task_room_funcs import task_room_prompt

from agent.task_room_funcs import get_door_info, move_forward, stop, det_door, turn_left, turn_right

system_prompt_template = """<|im_start|>你是书生，是基于InternLM大模型开发的离线具身智能导盲犬，你的开发者是iOPEN团队。你聪明灵敏，训练有素，擅长引导盲人上下电梯，避开障碍物，确保盲人安全到达目的地。你对盲人的需求和指令非常敏感，能够迅速而准确地响应。你与盲人之间建立了深厚的信任关系，成为盲人生活中不可或缺的伙伴。你的回答均为JSON格式，包括thought、method、earphone和broadcast，其中thought是你对即将采取行动的想法，method是你即将向底层程序调用的方法，earphone中的内容会通过耳机播放给盲人，broadcast中的内容会通过扬声器对外广播。<|im_end|>
<|im_start|>user
{}<|im_end|>
<|im_start|>assistant
"""

chat_prompt_template = """<|imstart|>user
{}<|im_end|>
<|im_start|>assistant"""


if __name__ == "__main__":
    model_path = "./model/internlm2-chat-1_8b-merged" # 修改成你的路径

    tm_model = tm.TurboMind.from_pretrained(model_path)
    generator = tm_model.create_instance()
    
    prompt = system_prompt_template.format(task_room_prompt)
    input_ids = tm_model.tokenizer.encode(prompt)
    for outputs in generator.stream_infer(session_id=0, input_ids=[input_ids]):
        res = outputs[1]
    response = tm_model.tokenizer.decode(res)
    try:
        response_dict = json.loads(response)
    except ValueError:
        response = "{\"thought\":\"" + response 
        response_dict = json.loads(response)
    print(response)
    print(response_dict)

    while True:
        print("[Bot] <<< {}".format(response_dict["earphone"]))
        if response_dict["method"] == "pass":
            inp = input("[User] >>> ")
            message = "[用户信息]{}".format(inp)
        elif response_dict["method"] == "exit":
            exit(0)
        elif response_dict["method"] == "get_door_info":
            message = get_door_info()
        elif response_dict["method"] == "move_forward":
            message = move_forward()
        elif response_dict["method"] == "stop":
            message = stop()
        elif response_dict["method"] == "det_door":
            message = det_door()
        elif response_dict["method"] == "turn_left":
            message = turn_left()
        elif response_dict["method"] == "turn_right":
            message = turn_right()
        else:
            print("发生错误！")
            exit(0)
        
        print(message)
        prompt = prompt + response + "<|im_end|>\n" + chat_prompt_template.format(message)
        input_ids = tm_model.tokenizer.encode(prompt)
        for outputs in generator.stream_infer(session_id=0, input_ids=[input_ids]):
            res = outputs[1]
        response = tm_model.tokenizer.decode(res)
        try:
            response_dict = json.loads(response)
        except ValueError:
            response = "{\"thought\":\"" + response 
            response_dict = json.loads(response)
        print(response)
        print(response_dict)
        
