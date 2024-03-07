import os
import json
from lmdeploy import turbomind as tm

from agent.utils import print_history, add_chat_history
from agent import system_prompt_template, chat_prompt_template
from agent import task_prompt, task_funcs


def choose_task():
    print("您好，请选择一个任务情景。")
    print("请输入一个整数，表示相应的情景：")
    print("\t1:盲人和导盲犬在一个长走廊上，长走廊的两侧有不同的房间。盲人说出房间号，导盲犬引导盲人去往目标房间；")
    print("\t2:盲人和导盲犬在电梯门前。盲人说出想要去的楼层，导盲犬引导盲人前往目标楼层；")
    print("\t3:盲人和导盲犬站在路旁，面前是一条马路，马路对面有一个楼梯，上楼梯后可以进入教学楼，导盲犬需要引导盲人通过马路进入对面的教学楼。")
    print("\t0:退出情景模拟。")
    task_id = -1
    while True:
        inp = input("[你的输入] >>> ")
        if not inp.isdigit():
            print("!!!!警告：输入格式错误!!!")
            continue 
        inp = int(inp)
        if inp == 1:
            task_id = inp - 1
            break
        elif inp == 2:
            task_id = inp - 1
            break 
        elif inp == 3:
            task_id = inp - 1
            break
        elif inp == 0:
            exit(0)
        else:
            print("!!!!警告：输入格式错误!!!")
            continue
    return task_id 


def main():
    model_path = "./model/internlm2-chat-1_8b-merged" # 修改成你的路径

    tm_model = tm.TurboMind.from_pretrained(model_path)
    generator = tm_model.create_instance()
    
    task_id = -1
    
    chat_history = []
    response_dict = {}
    os.system('cls' if os.name == 'nt' else 'clear')

    while True:
        if task_id != -1:
            print_history(chat_history, response_dict)
        
        flag = True
        if task_id == -1 or response_dict["method"] == "exit":
            flag = False
            chat_history = []
            response_dict = {}
            task_id = choose_task()
            prompt = system_prompt_template.format(task_prompt[task_id])
            add_chat_history(chat_history, "System", task_prompt[task_id])
        elif response_dict["method"] == "pass":
            inp = input("[你现在可以和机器人说话] >>> ")
            message = "[用户信息]{}".format(inp)
            add_chat_history(chat_history, "User", message)
        elif response_dict["method"] in task_funcs[task_id].keys():
            message = task_funcs[task_id][response_dict["method"]]()
            add_chat_history(chat_history, "System", message)
        else:
            print("!!!发生错误，模型调用了不存在的方法，重置会话...!!!")
            task_id = -1
            continue
        
        if flag:
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
        add_chat_history(chat_history, "Bot", response)


if __name__ == "__main__":
    main() 
