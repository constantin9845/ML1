import os
import numpy as np
import random
import shutil


def clean(source):

    source = source
    dest = f'validation_set'

    if os.path.exists(f'validation_set'):
        shutil.rmtree(f'validation_set')

    try:
        source_list = os.listdir(source)
    except:
        print('Could not find data set')
        exit(1)

    try:
        os.makedirs(f'validation_set')
    except:
        pass

    # Clean Data points -> store in clean_data folder
    for type in source_list:

        t = os.path.join(source,type)
        samples = os.listdir(t)

        try:
            os.mkdir(os.path.join(dest,type))
        except:
            pass


        for sample in samples:

            f = open(os.path.join(source,type,sample))
            text = f.read()

            target = os.path.join(dest,type,sample)

            with open(target, "w") as destination:

                for line in text.split('#'):
                    if(len(line) > 10):
                        temp = line.split(',')[6].replace('/',',')
                        destination.write('('+temp+')'+'\n')


input = 'data'

clean(input)


