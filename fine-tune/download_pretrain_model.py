#模型下载
from modelscope import snapshot_download
model_dir = snapshot_download('Shanghai_AI_Laboratory/internlm2-chat-1_8b-sft', cache_dir="model")
print(model_dir)