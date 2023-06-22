##### README file for the PTC corpus Version 2

Contents

1. About the Propaganda Techniques Corpus (PTC)
2. The tasks
3. Folder content and Data format
4. Citation
5. Changes in Version 2


About the Propaganda Techniques Corpus (PTC)
--------------------------------------------
​
This is the README file for the Propaganda Techniques Corpus (PTC). 
The dataset can be downloaded at https://propaganda.qcri.org/ptc/
The website offers a permanent leaderboard to allow researchers both to advertise their progress and to be up-to-speed with the state of the art on the tasks offered. 
The corpus was initially distributed as part of the SemEval 2020 task 11 shared task. 

PTC is a corpus of texts annotated with 18 fine-grained propaganda techniques.
PTC was manually annotated by six professional annotators (both unitized and labeled) considering the following 18 propaganda techniques:
​
* Loaded Language
* Name Calling,Labeling
* Repetition
* Exaggeration,Minimization
* Doubt
* Appeal to fear-prejudice
* Flag-Waving
* Causal Oversimplification
* Slogans
* Appeal to Authority
* Black-and-White Fallacy
* Thought-terminating Cliches
* Whataboutism
* Reductio ad Hitlerum
* Red Herring
* Bandwagon
* Obfuscation,Intentional Vagueness,Confusion
* Straw Men

For a descrition of the techniques, refer to the paper in the -Citation- section. 
Given the relatively low frequency of some of the techniques in the corpus, we decided to merge similar underrepresented techniques into one superclass:
​
For example, "Bandwagon" and "Reductio ad Hitlerum" are combined into "Bandwagon,Reductio ad Hitlerum".
Similarly, "Straw Men", "Red Herring" and "Whataboutism" are merged into "Whataboutism,Straw_Men,Red_Herring"
​
We further eliminated "Obfuscation,Intentional Vagueness,Confusion" as there were only 11 annotated cases in the whole corpus. Those two changes aim to simplify task TC (see below). 
​
Tasks
--------------------------------------------
Among the different tasks that the corpus can enable, SemEval 2020 Task 11 focuses on the following ones:
​
 - Task SI, Propaganda Spans Identification.
Given a plain-text document, identify the fragments that contain a propaganda technique. This is a binary sequence tagging task.
​
 - Task TC, Propaganda Technique Labeling.
Given a text fragment identified as propaganda and its document context, identify the propaganda technique at hand. This is a multi-label multi-class classification problem.
​
 - Task FLC, Fragment Level Classification. 
This task puts together task SI and TC: given a plain-text document, identify both the text-fragments in which a propaganda technique is used and the technique being used. This is a multi-label multi-class sequence tagging task. 


Folder content and Data format
--------------------------------------------

This is the content of the compressed archive:

.
├── train-articles/	
├── train-labels-task-si/	
├── dev-articles/	
├── train-labels-task-flc-tc/
├── dev-labels-task-flc-tc/
├── dev-labels-task-si/
├── test-articles/	
├── README.md		
├── dev-task-flc-tc.labels 
├── dev-task-si.labels
├── test-task-tc-template.out
├── train-task-flc-tc.labels
└── train-task-si.labels


-- Input News Articles 

   [ folders train-articles/, dev-articles/, test-articles/ ]

Folders "train-articles/", "dev-articles/", "test-articles/" contain input articles 
in plain text format for the training, development and test set, respectively. 
The articles were retrieved with newspaper3k library. 
The title is in the first row, followed by an empty row. 
The content of the article starts from the third row, one sentence per 
line (sentence splitting was performed automatically using teh NLTK sentence splitter).
In total, the training and the development partitions of PTC 
include 446 articles (~400k tokens) from 48 news outlets.


-- Gold Labels Files

   [ folders train-labels-task-si/ train-labels-task-flc-tc/ dev-labels-task-si/ dev-labels-task-flc-tc/ 
     files train-task-si.labels train-task-flc-tc.labels dev-task-si.labels dev-task-flc-tc.labels ]

Training and Development sets gold labels for task SI, FLC/TC. 
The gold files are tab separated. 
The gold file for tasks FLC/TC includes the following columns:
​
Col 1. Article ID
Col 2. The propaganda technique applied in the instance.
Col 3. The starting offset of the propaganda instance (inclusive)
Col 4. The ending offset of the propaganda instance (exclusive)
​
The annotation file for task SI is identical, except that it does not include Col 2 above.
​
Col 1. Article ID
Col 2. The starting offset of the propaganda instance (inclusive)
Col 3. The ending offset of the propaganda instance (exclusive)

Note that different propaganda techniques can overlap, either fully or partially.

Each *.labels file contains the annotations for all articles for a task in a single file. 
For example, the file train-task-si.labels contains all the gold labels for task si for the
training set (files in folder train-labels-task-si/) in one file. 


-- Template file for computing predictions for task TC

   [ test-task-tc-template.out ]
   
Template output file for the test set for task TC. This is necessary to provide
the input spans which need to be classified for the task. Each line of the file 
indicates in col 3,4 an input span. 
Predictions for task TC are obtained by replacing the ? in col 2 with one of the techniques. 

Overlapping techniques: if the exact same span is associated with multiple techniques, 
the corresponding span will appear multiple times in the .out file. 
You can print all the techniques appearing in the same span in any order (the evaluation 
scripts will consider the best match). For example, the gold spans 

123456	Loaded_Language	  10   20
123456	Repetition	  10   20

will match perfectly with 

123456	Repetition	  10   20
123456	Loaded_Language	  10   20  


Citation 
--------------------------------------------
​
Please cite the following publication when using the PTC corpus:
​
G. Da San Martino, S. Yu, A. Barrón-Cedeño, R. Petrov and P. Nakov, “Fine-Grained Analysis of Propaganda in News Articles”, to appear at Conference on Empirical Methods in Natural Language Processing (EMNLP 2019), Hong Kong, China, November 3-7, 2019.
​
@InProceedings{EMNLP19DaSanMartino,
author = {Da San Martino, Giovanni and
Yu, Seunghak and
Barr\'{o}n-Cede\~no, Alberto and
Petrov, Rostislav and
Nakov, Preslav},
title = {Fine-Grained Analysis of Propaganda in News Articles},
booktitle = {Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and 9th International Joint Conference on Natural Language Processing, EMNLP-IJCNLP 2019, Hong Kong, China, November 3-7, 2019},
series = {EMNLP-IJCNLP 2019},
year = {2019},
address = {Hong Kong, China},
month = {November},
}

A copy of the paper describing the corpus is available at https://propaganda.qcri.org/fine-grained-propaganda/index.html



Changes in version 2
--------------------------------------------

The annotations have been revised, with respect to the first version distributed for the SemEval 2020 Task 11 shared task, and modified as follows:

1) All annotations whose starting offset was beyond the lenght of the corresponding article were deleted (1 instance)
2) All annotations whose ending offset was beyond the length of the article were trimmed such that they would end at the end of the article (2 instances)
3) In order to move towards standardised annotation boundaries, 
   all annotations were trimmed in order not to start or end with any of the following characters: " ", "\n", ".", ",", ":", ";" (456 instances)
4) We checked overlapping annotations for inconsistencies (~270 annotations modified) 
