### EMNLP Submission 2023: Large Language Models for Propaganda Detection

This repo shows how to replicate the results of our paper: Large Language Models for Propaganda Detection

Further we provide a `reqiurements.txt` file, which allows to install the necessary python packages and dependencies. We tested the installation on a Linux based GPU cluster and a 2021 M1 Macbook Pro. To install the requirements we recommend create a new virtual environment and run:

`pip install -r requirements.txt`

Further the API organization id and API key need to be added to the path

Below we show step-by-step how to replicate our results:

1. create text classification data from the token classification data set. The original dataset can be found [here](https://propaganda.qcri.org/semeval2020-task11/).

`python src/text_classification/helper/create_labels_text_classification.py`

2. split the articles for the fine-tuning of gpt-3 so they fit in the given token limit.

`python src/text_classification/helper/split_text.py`

3. create the .json for fine-tuning file for GPT-3 the python file takes as input one of the three gpt-3 config files e.g. `src/text_classification/gpt/config/gpt3_instruction_base.yaml` this will create the dataset under `src/text_classification/gpt/train-gpt3-json/gpt-3_instruction_base.json`

`python src/text_classification/gpt/create_training_data.py -c src/text_classification/gpt/config/gpt3_instruction_base.yaml`

4. run the fine-tune jobs. First we validate the created .json file and split it into training and validation data, afterwards we train the model. Note for GPT-3 base and chain of thought we solely finetune one model with different prompts at inference.

`bash src/text_classification/gpt/fine-tune-gpt-3.sh`

5. run inference and calculate metrics, for each of the five model combinations use the correct .yaml file. Under  

`python `
 
