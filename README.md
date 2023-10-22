### Large Language Models for Propaganda Detection

This repository demonstrates how to reproduce the results of our paper: Large Language Models for Propaganda Detection.

We provide a `requirements.txt` file that contains the necessary Python packages and dependencies. The installation has been tested on a Linux-based GPU cluster and a 2021 M1 MacBook Pro. To install the requirements, we recommend creating a new virtual environment and running the following command:

```shell
pip install -r requirements.txt
```

Additionally, you need to add the API organization ID and API key to the environment variables:

```shell
export OPENAI_ORGANIZATION="your_organization"
export OPENAI_API_KEY="your_api_key"
```

Below, we outline the step-by-step process to replicate our results:

1. Create text classification data from the token classification dataset. The original dataset can be found [here](https://propaganda.qcri.org/semeval2020-task11/).

```shell
python src/text_classification/helper/create_labels_text_classification.py
```

2. Split the articles for fine-tuning the GPT-3 model to fit within the token limit.

```shell
python src/text_classification/helper/split_text.py
```

3. Create the `.json` file for GPT-3 fine-tuning using one of the three GPT-3 config files, e.g., `src/text_classification/gpt/config/gpt3_instruction_base.yaml`. This will generate the dataset under `src/text_classification/gpt/train-gpt3-json/gpt-3_instruction_base.json`.

```shell
python src/text_classification/gpt/create_training_data.py -c src/text_classification/gpt/config/gpt3_instruction_base.yaml
```

4. Run the fine-tuning jobs. First, validate the created `.json` file and split it into training and validation data. Then, train the model. Note that for GPT-3 base and chain of thought, we only fine-tune one model with different prompts at inference.

```shell
bash src/text_classification/gpt/fine-tune-gpt-3.sh
```

5. Run inference and calculate metrics for each of the five model combinations using the corresponding `.yaml` file. The results will be saved under `src/text_classification/gpt/results`. For the GPT-3 models, this process requires training your own model (step 4) and adapting the `model_name` accordingly within the provided `.yaml` file.

```shell
python src/text_classification/gpt/inference.py -c src/text_classification/gpt/config/gpt4_base.yaml
```

By following these steps, you should be able to replicate our results as described in the paper.
