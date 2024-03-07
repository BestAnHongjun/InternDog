import os
import gradio as gr

import agent
from agent.config import system_prompt_template
from agent.task_funcs import task_prompt, task_funcs
from agent.task_lift_funcs import return_to_web_demo
from agent.utils import processor, chat, analysis_response


def user_chat(msg, chat_history, chat_history_clear, prompt, task_id):
    msg = "[用户消息]" + msg 
    return processor(msg, chat_history, chat_history_clear, task_funcs, prompt, task_id)
    

def select(scene):
    task_id = -1
    if scene == "Room":
        task_id = 0
    elif scene == "Lift":
        task_id = 1
    else:
        task_id = 2
    prompt = system_prompt_template.format(task_prompt[task_id])
    prompt, response, response_dict = chat(prompt)
    message = analysis_response(response_dict)
    chat_history = [(task_prompt[task_id], response)]
    chat_history_clear = [("模拟{}情景。".format(scene), response_dict["earphone"])]
    return return_to_web_demo(
        message, chat_history, chat_history_clear, prompt, task_id,
        controller_pass=gr.update(visible=True)
    )


def common(msg, chat_history, chat_history_clear, prompt, task_id):
    return processor(msg, chat_history, chat_history_clear, task_funcs, prompt, task_id)


with gr.Blocks() as demo:
    with gr.Row():
        with gr.Tab("您与导盲犬的对话"):
            chatbot_clear = gr.Chatbot(height=500, label="历史消息")
        with gr.Tab("原始细节"):
            chatbot = gr.Chatbot(height=500, label="历史消息")
    with gr.Row():
        with gr.Column(scale=4):
            with gr.Tab("InternDog当前状态"):
                model_res = gr.Markdown(value="")
            user_msg = gr.Textbox(label="与InternDog对话", interactive=False, placeholder="请先通过右侧选择一个模拟情景。")
            user_msg_submit = gr.Button(value="提交", interactive=False)
        with gr.Column(scale=2):
            # select界面
            with gr.Group() as controller_select:
                with gr.Tab("底层程序模拟器"):
                    gr.Markdown(value="当前调用方法：`select`")
                    gr.Markdown(value="请选择一个模拟情景：\n * Room:盲人和导盲犬在一个长走廊上，长走廊的两侧有不同的房间。盲人说出房间号，导盲犬引导盲人去往目标房间；\n * Lift:盲人和导盲犬在电梯门前。盲人说出想要去的楼层，导盲犬引导盲人前往目标楼层；\n * Street:盲人和导盲犬站在路旁，面前是一条马路，马路对面有一个楼梯，上楼梯后可以进入教学楼，导盲犬需要引导盲人通过马路进入对面的教学楼。")
                    controller_select_radio = gr.Radio(["Room", "Lift", "Street"], label="情景选择", value="Room", interactive=True)
                    controller_select_submit = gr.Button(value="确认场景")
                    
            # pass界面
            with gr.Group(visible=False) as controller_pass:
                with gr.Tab("底层程序模拟器"):
                    gr.Markdown(value="当前调用方法：`pass`")
                    gr.Markdown(value="模型没有对底层程序发起实质性请求，底层程序后台运行中...<br>您现在可以通过左侧对话框与InternDog对话。")
                    
            # 一般任务
            with gr.Group(visible=False) as controller_common:
                with gr.Tab("底层程序模拟器"):
                    controller_common_method = gr.Markdown(value="模型向底层程序调用了`move_in`方法。")
                    controller_common_prompt = gr.Markdown(visible=False)
                    controller_common_task_id = gr.Number(visible=False)
                    controller_common_message = gr.Markdown(visible=False)
                    controller_common_submit = gr.Button(value="确认")
                    
            # Lift任务 - get_door_state
            with gr.Group(visible=False) as controller_lift_get_door_state:
                with gr.Tab("底层程序模拟器"):
                    gr.Markdown(value="当前调用方法：`get_door_state`")
                    gr.Markdown(value="InternDog正在检测电梯门是否开启！<br>现在，由您来充当底层程序。您可以将检测结果告诉InternDog。<br>电梯门开了吗？")
                    controller_lift_get_door_state_radio = gr.Radio(["门开了", "门没开"], label="请选择状态", value="门没开", interactive=True)
                    controller_lift_get_door_state_submit = gr.Button(value="提交选择")
            
            # Lift任务 - get_floor_state
            with gr.Group(visible=False) as controller_lift_get_floor_state:
                with gr.Tab("底层程序模拟器"):
                    gr.Markdown(value="当前调用方法：`get_floor_state`")
                    gr.Markdown(value="InternDog正在检测当前电梯到达的楼层！<br>现在，由您来充当底层程序。您可以将检测结果告诉InternDog。<br>现在到几楼了？")
                    controller_lift_get_floor_state_number = gr.Number(label="输入1-99之间的整数，表示楼层", interactive=True, minimum=1, maximum=99, step=1, value=1)
                    controller_lift_get_floor_state_submit = gr.Button(value="提交")
            
            # Room任务 - get_door_info
            with gr.Group(visible=False) as controller_room_get_door_info:
                with gr.Tab("底层程序模拟器"):
                    gr.Markdown(value="当前调用方法：`get_door_info`")
                    gr.Markdown(value="InternDog刚刚检测到了门牌！<br>现在，由您来充当底层程序。您可以决定InternDog看到的门牌信息。<br>InternDog看到的门牌号是？")
                    controller_room_get_door_info_number = gr.Number(label="输入101-1090之间的整数，表示门牌号", interactive=True, minimum=101, maximum=1090, step=1, value=101)
                    controller_room_get_door_info_direct = gr.Radio(label="该门牌在导盲犬的左侧还是右侧？", choices=["左侧", "右侧"], value="左侧", interactive=True)
                    controller_room_get_door_info_submit = gr.Button(value="提交")
            
            # Room任务 - det_door
            with gr.Group(visible=False) as controller_room_det_door:
                with gr.Tab("底层程序模拟器"):
                    gr.Markdown(value="当前调用方法：`det_door`")
                    gr.Markdown(value="InternDog正在走廊中向前移动，并在移动的过程中检测左右两边是否有门牌。<br>现在，由您来充当底层程序。您可以决定InternDog是否检测到门牌。<br>InternDog检测到门牌了吗？")
                    controller_room_det_door_radio = gr.Radio(["检测到了", "没检测到"], label="请选择状态", value="没检测到", interactive=True)
                    controller_room_det_door_submit = gr.Button(value="提交选择")
            
            # Street任务 - get_surrounding_state
            with gr.Group(visible=False) as controller_street_get_surrounding_state:
                with gr.Tab("底层程序模拟器"):
                    gr.Markdown(value="当前调用方法：`get_surrounding_state`")
                    gr.Markdown(value="InternDog正在探测周边环境状况。<br>现在，由您来充当底层程序。您可以将探测结果告诉InternDog。")
                    controller_street_get_surrounding_state_1 = gr.Button(value="周围安全")
                    controller_street_get_surrounding_state_2 = gr.Button(value="周围1m内有人")
                    controller_street_get_surrounding_state_3 = gr.Button(value="周围5m内有车")
                    controller_street_get_surrounding_state_4 = gr.Button(value="前方有楼梯")
                    controller_street_get_surrounding_state_5 = gr.Button(value="已离开楼梯")
                    controller_street_get_surrounding_state_6 = gr.Button(value="已进入教学楼")
    
    outputs_list = [
        model_res, user_msg, user_msg_submit, chatbot, chatbot_clear,
        controller_select, controller_pass, 
        controller_common, controller_common_method, controller_common_message,
        controller_common_prompt, controller_common_task_id,
        controller_lift_get_door_state, controller_lift_get_floor_state,
        controller_room_get_door_info, controller_room_det_door,
        controller_street_get_surrounding_state
    ]
    
    # 用户对话
    user_msg_submit.click(fn=user_chat, inputs=[user_msg, chatbot, chatbot_clear, controller_common_prompt, controller_common_task_id], outputs=outputs_list)
    
    # select界面
    controller_select_submit.click(fn=select, inputs=[controller_select_radio], outputs=outputs_list)
    
    # 一般任务界面
    controller_common_submit.click(fn=common, inputs=[controller_common_message, chatbot, chatbot_clear, controller_common_prompt, controller_common_task_id], outputs=outputs_list)
    
    # Lift任务 - get_door_state
    controller_lift_get_door_state_submit.click(fn=agent.task_funcs.web_lift_get_door_state, inputs=[controller_lift_get_door_state_radio, chatbot, chatbot_clear, controller_common_prompt, controller_common_task_id], outputs=outputs_list)
    
    # Lift任务 - get_floor_state
    controller_lift_get_floor_state_submit.click(fn=agent.task_funcs.web_lift_get_floor_state, inputs=[controller_lift_get_floor_state_number, chatbot, chatbot_clear, controller_common_prompt, controller_common_task_id], outputs=outputs_list)
                
    # Room任务 - get_door_info
    controller_room_get_door_info_submit.click(fn=agent.task_funcs.web_room_get_door_info, inputs=[controller_room_get_door_info_number, controller_room_get_door_info_direct, chatbot, chatbot_clear, controller_common_prompt, controller_common_task_id], outputs=outputs_list)
    
    # Room任务 - det_door
    controller_room_det_door_submit.click(fn=agent.task_funcs.web_room_det_door, inputs=[controller_room_det_door_radio, chatbot, chatbot_clear, controller_common_prompt, controller_common_task_id], outputs=outputs_list)
    
    # Street任务 - get_surrounding_state
    controller_street_get_surrounding_state_1.click(fn=agent.task_funcs.web_street_get_surrounding_state, inputs=[controller_street_get_surrounding_state_1, chatbot, chatbot_clear, controller_common_prompt, controller_common_task_id], outputs=outputs_list)
    controller_street_get_surrounding_state_2.click(fn=agent.task_funcs.web_street_get_surrounding_state, inputs=[controller_street_get_surrounding_state_2, chatbot, chatbot_clear, controller_common_prompt, controller_common_task_id], outputs=outputs_list)
    controller_street_get_surrounding_state_3.click(fn=agent.task_funcs.web_street_get_surrounding_state, inputs=[controller_street_get_surrounding_state_3, chatbot, chatbot_clear, controller_common_prompt, controller_common_task_id], outputs=outputs_list)
    controller_street_get_surrounding_state_4.click(fn=agent.task_funcs.web_street_get_surrounding_state, inputs=[controller_street_get_surrounding_state_4, chatbot, chatbot_clear, controller_common_prompt, controller_common_task_id], outputs=outputs_list)
    controller_street_get_surrounding_state_5.click(fn=agent.task_funcs.web_street_get_surrounding_state, inputs=[controller_street_get_surrounding_state_5, chatbot, chatbot_clear, controller_common_prompt, controller_common_task_id], outputs=outputs_list)
    controller_street_get_surrounding_state_6.click(fn=agent.task_funcs.web_street_get_surrounding_state, inputs=[controller_street_get_surrounding_state_6, chatbot, chatbot_clear, controller_common_prompt, controller_common_task_id], outputs=outputs_list)


if __name__ == "__main__":
    os.environ["no_proxy"] = "localhost,127.0.0.1,::1"
    demo.launch()
