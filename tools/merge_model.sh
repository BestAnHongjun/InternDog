export CUDA_VISIBLE_DEVICES=2
rm -rf ./model/internlm2-chat-1_8b-merged
xtuner convert merge ./model/Shanghai_AI_Laboratory/internlm2-chat-1_8b-sft ./model/hf ./model/internlm2-chat-1_8b-merged --max-shard-size 2GB