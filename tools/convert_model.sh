export CUDA_VISIBLE_DEVICES=2
rm -rf model/hf
mkdir model/hf
export MKL_SERVICE_FORCE_INTEL=1
export MKL_THREADING_LAYER=GNU
xtuner convert pth_to_hf ./internlm2_1_8b_qlora_lift_e3.py ./work_dirs/internlm2_1_8b_qlora_lift_e3/iter_61000.pth ./model/hf
