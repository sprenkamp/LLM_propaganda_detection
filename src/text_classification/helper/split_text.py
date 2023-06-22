import os
import nltk
import pandas as pd


paths_in = ['data/propaganda/token_classification_original/train-articles/', 'data/propaganda/token_classification_original/dev-articles/']
paths_out = ['data/propaganda/text_classification/split-articles/train-articles/', 'data/propaganda/text_classification/split-articles/dev-articles/']

def write_to_file(text, file_name, labels, label_file_name):
    with open(file_name, 'w', encoding="utf-8") as f:
        f.write(text)

    with open(label_file_name, 'w', encoding="utf-8") as f:
        labels = list(set(labels))
        for label in labels:
            f.write(f'{label}\n')

for path_in, path_out in zip(paths_in, paths_out):
    files = os.listdir(path_in)
    files.sort()
    for file_name in files:
        chunk_size = 1500  # adjust this value as needed
        with open(path_in+file_name, 'r') as f:
            text = f.read()
        if path_in.endswith('train-articles/'):    
            label_df = pd.read_csv(path_in.replace('train-articles', 'train-labels-task-flc-tc') + file_name.split(".")[0]+".task-flc-tc.labels", sep='\t', header=None, names=['filename', 'label', 'start', 'end'])
        else:
            label_df = pd.read_csv(path_in.replace('dev-articles', 'dev-labels-task-flc-tc') + file_name.split(".")[0]+".task-flc-tc.labels", sep='\t', header=None, names=['filename', 'label', 'start', 'end'])

        # split the text into sentences
        sentences = nltk.sent_tokenize(text)

        subfile_index = 1
        subfile_sentences = []
        upper_boundary = 0
        lower_boundary = 0
        for sentence in sentences:
            sentence_length = len(sentence)
            if upper_boundary + sentence_length + 1 > chunk_size:  # +1 for the space between sentences
                # write the current chunk to a file
                subfile_text = ' '.join(subfile_sentences)
                if subfile_index == 1:
                    labels = label_df[label_df['end'] <= upper_boundary].label.values
                else:
                    labels = label_df[(label_df['start'] > lower_boundary)&(label_df['end'] <= upper_boundary)].label.values
                # print("subfile_index:", subfile_index, "boundaries:", lower_boundary, upper_boundary, "chunksize:", chunk_size)
                if path_out.endswith('train-articles/'): 
                    write_to_file(subfile_text, f'{path_out}{file_name.split(".")[0]}_{subfile_index}.txt', labels , f'{path_out.replace("train-articles", "train-labels")}{file_name.split(".")[0]}_{subfile_index}.txt')
                else:
                    write_to_file(subfile_text, f'{path_out}{file_name.split(".")[0]}_{subfile_index}.txt', labels , f'{path_out.replace("dev-articles", "dev-labels")}{file_name.split(".")[0]}_{subfile_index}.txt')
                # start a new chunk
                lower_boundary = upper_boundary
                subfile_sentences = [sentence]
                upper_boundary += sentence_length + 1
                subfile_index += 1
                chunk_size = upper_boundary + 1500
            else:
                # add the sentence to the current chunk
                subfile_sentences.append(sentence)
                upper_boundary += sentence_length + 1  # +1 for the space between sentences

        # don't forget the last chunk
        if subfile_sentences:
            subfile_text = ' '.join(subfile_sentences)
            labels = label_df[(label_df['end'] > lower_boundary)].label.values
            #print("subfile_index:", subfile_index, "boundaries:", lower_boundary, upper_boundary, "chunksize:", chunk_size)
            if path_out.endswith('train-articles/'): 
                write_to_file(subfile_text, f'{path_out}{file_name.split(".")[0]}_{subfile_index}.txt', labels , f'{path_out.replace("train-articles", "train-labels")}{file_name.split(".")[0]}_{subfile_index}.txt')
            else:
                write_to_file(subfile_text, f'{path_out}{file_name.split(".")[0]}_{subfile_index}.txt', labels , f'{path_out.replace("dev-articles", "dev-labels")}{file_name.split(".")[0]}_{subfile_index}.txt')
