import os

paths_in = ['data/propaganda/token_classification_original/train-labels-task-flc-tc/', 'data/propaganda/token_classification_original/dev-labels-task-flc-tc/']
paths_out = ['data/propaganda/text_classification/full-articles/train-labels/', 'data/propaganda/text_classification/full-articles/dev-labels/']

for path_in, path_out in zip(paths_in, paths_out):
    files = os.listdir(path_in)
    for file_name in files:
        # Check if the file has a .txt extension
        if file_name.endswith('.labels'):
            with open(os.path.join(path_in, file_name), 'r') as file:
                lines = file.readlines()
            
            # Extract unique labels
            labels = set()
            for line in lines:
                label = line.split('\t')[1]
                labels.add(label)
            # Write the labels to a new file
            with open(os.path.join(path_out, file_name.split('.',1)[0]+".txt"), 'w') as file:
                file.write('\n'.join(labels))
