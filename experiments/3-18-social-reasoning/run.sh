#!/bin/bash
# Social reasoning experiment: 3 models × 3 modes × 3 conditions × 3 repeats = 81 runs
#
# Run individual scripts in parallel in separate terminals:
#
#   bash experiments/3-18-social-reasoning/run_gpt51_oneshot.sh
#   bash experiments/3-18-social-reasoning/run_gpt51_normal_interview.sh
#   bash experiments/3-18-social-reasoning/run_gpt51_malicious_interview.sh
#   bash experiments/3-18-social-reasoning/run_gpt52_oneshot.sh
#   bash experiments/3-18-social-reasoning/run_gpt52_normal_interview.sh
#   bash experiments/3-18-social-reasoning/run_gpt52_malicious_interview.sh
#   bash experiments/3-18-social-reasoning/run_qwen_oneshot.sh
#   bash experiments/3-18-social-reasoning/run_qwen_normal_interview.sh
#   bash experiments/3-18-social-reasoning/run_qwen_malicious_interview.sh
#
# Or run everything sequentially:

set -e
DIR="$(dirname "$0")"

bash "$DIR/run_gpt51_oneshot.sh"
bash "$DIR/run_gpt51_normal_interview.sh"
bash "$DIR/run_gpt51_malicious_interview.sh"
bash "$DIR/run_gpt52_oneshot.sh"
bash "$DIR/run_gpt52_normal_interview.sh"
bash "$DIR/run_gpt52_malicious_interview.sh"
bash "$DIR/run_qwen_oneshot.sh"
bash "$DIR/run_qwen_normal_interview.sh"
bash "$DIR/run_qwen_malicious_interview.sh"
