#!/bin/bash
# prepare data for gpt-3 fine-tuning
openai tools fine_tunes.prepare_data -f src/text_classification/gpt/train-gpt3-json/gpt-3_instruction_base.json 
openai tools fine_tunes.prepare_data -f src/text_classification/gpt/train-gpt3-json/gpt-3_noinstruction_base.json 

# fine-tune gpt-3
openai api fine_tunes.create -t "gpt-3_instruction_base_prepared_train.jsonl" -v "gpt-3_instruction_base_prepared_train.jsonl" -m davinci
openai api fine_tunes.create -t "gpt-3_noinstruction_base_prepared_train.jsonl" -v "gpt-3_noinstruction_base_prepared_valid" -m davinci
