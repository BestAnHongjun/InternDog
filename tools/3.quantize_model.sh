export HF_MODEL=./model/internlm2-chat-1_8b-merged
export WORK_DIR=./model/internlm2-chat-1_8b-w4a16

lmdeploy lite auto_awq \
   $HF_MODEL \
  --calib-dataset 'ptb' \
  --calib-samples 128 \
  --calib-seqlen 2048 \
  --w-bits 4 \
  --w-group-size 128 \
  --work-dir $WORK_DIR