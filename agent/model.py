import json
from lmdeploy import turbomind as tm
from agent.config import model_path


tm_model = tm.TurboMind.from_pretrained(model_path)
generator = tm_model.create_instance()


def chat(prompt):
    input_ids = tm_model.tokenizer.encode(prompt)
    for outputs in generator.stream_infer(session_id=0, input_ids=[input_ids]):
        res = outputs[1]
    response = tm_model.tokenizer.decode(res)
    try:
        response_dict = json.loads(response)
    except ValueError:
        response = "{\"thought\":\"" + response 
        response_dict = json.loads(response)
    prompt += response + "<|im_end|>\n"
    return prompt, response, response_dict
