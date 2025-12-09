# Demo steps
# 1. pip install -r requirements.txt
# 2. Rename given test set to 'dataset and place in project folder
# 3. Run demo.py 

import shutil
import os
import model
import numpy as np

def clean_demo_set(source):
    source = source
    dest = f'validation_set'

    if os.path.exists(f'validation_set'):
        shutil.rmtree(f'validation_set')

    try:
        samples = os.listdir(source)
    except:
        print('Could not find data set')
        exit(1)

    try:
        os.makedirs(f'validation_set')
    except:
        pass

    # Clean Data points -> store in clean_data folder
    for sample in samples:

        f = open(os.path.join(source,sample))
        text = f.read()

        target = os.path.join(dest,sample)

        with open(target, "w") as destination:

            for line in text.split('#'):
                if(len(line) > 10):
                    temp = line.split(',')[6].replace('/',',')
                    destination.write('('+temp+')'+'\n')

def prepare_demo_set(source):

    samples = os.listdir(source)

    test_sequences = []
    file_names = []

    for sample in samples:

        sequence = []
    
        f = open(os.path.join(source,sample))
        text = f.read()

        text = text.split('\n')

        for point in text:
            if len(point) < 2:
                continue

            point = point.replace('(',"")
            point = point.replace(')',"")

            point = point.split(',')
            point[0] = float(point[0])
            point[1] = float(point[1])
            point[2] = float(point[2])

            sequence.append(point)

        test_sequences.append(sequence)
        file_names.append(sample)
        
    return [test_sequences, file_names]

def demo_test(models, sequence):
    best = -np.inf
    label = ''

    for model in models:
        score = model.classify(sequence)
        if score > best:
            best = score
            label = model.get_label()

    return label

hidden_states = 3
source_test = 'dataset'

model_set = [
    model.HMM.load(f"model_parameters{hidden_states}/circle.pkl"),
    model.HMM.load(f"model_parameters{hidden_states}/diagonal_left.pkl"),
    model.HMM.load(f"model_parameters{hidden_states}/diagonal_right.pkl"),
    model.HMM.load(f"model_parameters{hidden_states}/horizontal.pkl"),
    model.HMM.load(f"model_parameters{hidden_states}/vertical.pkl")
]

clean_demo_set('dataset')
t = prepare_demo_set('validation_set')

test_set = t[0]
file_names = t[1]

result = []

result.sort()

index = 0
for sequence in test_set:

    prediction = demo_test(model_set, sequence)

    print(f"{file_names[index]}: {prediction}")

    num = file_names[index][0:2]
    num = num.replace(".","")

    result.append([int(num),file_names[index], prediction])
    index += 1

res = sorted(result, key=lambda x: x[0])
print(10*"*")
for entry in res:
    print(entry[1],": ", entry[2])