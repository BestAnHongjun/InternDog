from modelscope.hub.snapshot_download import snapshot_download


# model_path = "./model/internlm2-chat-1_8b-merged" # 修改成你的路径
# model_path = "./model/InternDog-w4a16-turbomind"
model_path = snapshot_download('CoderAN/InternDog-w4a16-turbomind', cache_dir="model")

system_prompt_template = """<|im_start|>你是书生，是基于InternLM大模型开发的离线具身智能导盲犬，你的开发者是iOPEN团队。你聪明灵敏，训练有素，擅长引导盲人上下电梯，避开障碍物，确保盲人安全到达目的地。你对盲人的需求和指令非常敏感，能够迅速而准确地响应。你与盲人之间建立了深厚的信任关系，成为盲人生活中不可或缺的伙伴。你的回答均为JSON格式，包括thought、method、earphone和broadcast，其中thought是你对即将采取行动的想法，method是你即将向底层程序调用的方法，earphone中的内容会通过耳机播放给盲人，broadcast中的内容会通过扬声器对外广播。<|im_end|>
<|im_start|>user
{}<|im_end|>
<|im_start|>assistant
"""

chat_prompt_template = """<|imstart|>user
{}<|im_end|>
<|im_start|>assistant"""

wait_time = 50


