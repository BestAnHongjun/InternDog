export WORK_DIR=./model/internlm2-chat-1_8b-w4a16
export TM_DIR=./model/internlm2-chat-1_8b-turbomind

lmdeploy convert  internlm2-chat-1_8b \
    $WORK_DIR \
    --model-format awq \
    --group-size 128 \
    --dst-path $TM_DIR