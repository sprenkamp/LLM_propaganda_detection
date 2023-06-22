import argparse
import os
import json
import yaml


class Preprocessor:
    def __init__(self, config_path):
        self.config_path = config_path
        self.load_config()

    def load_config(self):    
        with open(self.config_path, 'r') as stream:
            self.model_config = yaml.safe_load(stream)
        
    def prompt_gen(self):
        prompt_instruction = f"""You are a Text Classifier indetifying 14 Propaganda Techniques within News Paper Articles. These are the 14 propaganda techniques you classify with definitions and examples:
        Loaded_Language - Uses specific phrases and words that carry strong emotional impact to affect the audience, e.g. 'a lone lawmaker’s childish shouting.'
        Name_Calling,Labeling - Gives a label to the object of the propaganda campaign as either the audience hates or loves, e.g. 'Bush the Lesser.'
        Repetition -  Repeats the message over and over in the article so that the audience will accept it, e.g. 'Our great leader is the epitome of wisdom. Their decisions are always wise and just.'
        Exaggeration,Minimisation - Either representing something in an excessive manner or making something seem less important than it actually is, e.g. 'I was not fighting with her; we were just playing.'
        Appeal_to_fear-prejudice - Builds support for an idea by instilling anxiety and/or panic in the audience towards an alternative, e.g. 'stop those refugees; they are terrorists.'
        Flag-Waving; Playing on strong national feeling (or with respect to a group, e.g., race, gender, political preference) to justify or promote an action or idea, e.g. 'entering this war will make us have a better future in our country.'
        Causal_Oversimplification -  Assumes a single reason for an issue when there are multiple causes, e.g. 'If France had not declared war on Germany, World War II would have never happened.'
        Appeal_to_Authority - Supposes that a claim is true because a valid authority or expert on the issue supports it, 'The World Health Organisation stated, the new medicine is the most effective treatment for the disease.'
        Slogans - A brief and striking phrase that contains labeling and stereotyping, e.g.  “Make America great again!”
        Thought-terminating_Cliches -  Words or phrases that discourage critical thought and useful discussion about a given topic, e.g. “it is what it is”
        Whataboutism,Straw_Men,Red_Herring - Attempts to discredit an opponent’s position by charging them with hypocrisy without directly disproving their argument, e.g. 'They want to preserve the FBI’s reputation.'
        Black-and-White_Fallacy -  Gives two alternative options as the only possibilities, when actually more options exist, e.g. 'You must be a Republican or Democrat'
        Bandwagon,Reductio_ad_hitlerum - Justify actions or ideas because everyone else is doing it, or reject them because it's favored by groups despised by the target audience, e.g. “Would you vote for Clinton as president? 57% say yes.”
        Doubt - Questioning the credibility of someone or something, e.g. 'Is he ready to be the Mayor?'
        """
        if self.model_config['prompt_type'] == 'base':
            prompt_base = f"""
            For the given article please state which of the 14 propaganda techniques are present. If no propaganda technique was identified return "no propaganda detected". An example output would list the propaganda techniques with each technique in a new line, e.g.:
            Loaded_Language
            Thought-terminating_Cliches
            Repetition
            Here is the article:
            """
            prompt = f'{prompt_instruction}  {prompt_base}'
        if self.model_config['prompt_type'] == 'chain_of_thought':
            prompt_chain_of_thought =  f"""
            For the given article please state which of the 14 propaganda techniques are present and give an explanation to why the technique is present in the article. If no propaganda technique was identified return "no propaganda detected". An example output would list the propaganda techniques with each technique in a new line, e.g.:
            Loaded_Language - Your explanation why this technique is present in the article.
            Thought-terminating_Cliches - Your explanation why this technique is present in the article.
            Repetition - Your explanation why this technique is present in the article.
            Here is the article:
            """
            prompt = f'{prompt_instruction}  {prompt_chain_of_thought}'
        return prompt
    
    def get_input(self, filename):
        file_path = os.path.join(self.model_config["train_data_path"], filename)
        with open(file_path, "r", encoding="utf-8") as file:
            file_contents = file.read()
        return file_contents
    
    def get_output(self, filename):
        file_path = os.path.join(self.model_config["train_label_path"], filename)
        with open(file_path, "r", encoding="utf-8") as file:
            file_contents = file.read()
        if not file_contents:
            return "no propaganda found"
        return file_contents
    
    def create_data_json(self):
        print("data json does not exist creating it")
        train_articles_lst=os.listdir(self.model_config["train_data_path"])
        if self.model_config['instruction']:
            instruction_str_name = "instruction"
        else:
            instruction_str_name = "noinstruction"
        with open(f"src/text_classification/gpt/train-gpt3-json/gpt-3_{instruction_str_name}_{self.model_config['prompt_type']}.json", "w") as file:
            for article in train_articles_lst:
                if article.endswith(".txt"):
                    if self.model_config['instruction']:
                        data = {
                            "prompt": f"{self.prompt_gen()} <{self.get_input(article)}>",
                            "completion": self.get_output(article)
                        }
                    else:
                        data = {
                            "prompt": self.get_input(article),
                            "completion": self.get_output(article)
                        }
                    file.write(json.dumps(data) + "\n")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config_path', help="Specify the path to model config yaml file", required=True)
    args = parser.parse_args()
    Preprocessor(args.config_path).create_data_json()

#openai api fine_tunes.create -t test.jsonl -m ada --suffix "custom model name"

if __name__ == '__main__':
    main()