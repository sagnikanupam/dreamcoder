import datetime
import os
import random
import math
import pandas as pd

import binutil  # required to import from dreamcoder modules
from pathlib import Path
from dreamcoder.ec import commandlineArguments, ecIterator
from dreamcoder.grammar import Grammar
from dreamcoder.program import Primitive
from dreamcoder.task import Task
from dreamcoder.type import arrow, tint, tstr
from dreamcoder.utilities import numberOfCPUs
from dreamcoder.domains.re2.main import StringFeatureExtractor
from dreamcoder.domains.mathDomain.mathDomainPrimitives import mathDomainPrimitives

TRAINING_DATASET_FILEPATHS = [Path.cwd()/'data'/'mathDomain'/'augmentedIteration5-08-01-23.csv']

#print(f"Training Dataset From: {TRAINING_DATASET_FILEPATHS}")
#Check Header on Training Dataset before passing as argument
training_data_list = [pd.read_csv(dataset) for dataset in TRAINING_DATASET_FILEPATHS] #pandas dataframe containing training data
training_data = pd.concat([data for data in training_data_list], ignore_index=True)
NUM_TR = training_data.shape[0] #number of training examples
#print(f"Number of Equations Used For Training: {NUM_TR}")
#print(training_data)

TESTING_DATASET_FILEPATH = Path.cwd()/'data'/'mathDomain'/'conpoleDatasetPrefix.csv'
#print(f"Testing Dataset From: {TESTING_DATASET_FILEPATH}")
testing_data = pd.read_csv(TESTING_DATASET_FILEPATH) #pandas dataframe containing testing data
NUM_TE = testing_data.shape[0] #number of training examples
#print(f"Number of Equations Used For Testing: {NUM_TE}")

def index_pair_X(x):
   return {"i": 0, "o": x}

def train_pair_X(x):
  input_output_dict = {"i":str(training_data.iat[x, 2]), "o": str(training_data.iat[x, 5])}
  return input_output_dict

def test_pair_X(x):
  input_output_dict = {"i": str(testing_data.iat[x, 2]), "o": str(testing_data.iat[x, 5])}
  return input_output_dict

def get_tstr_task(item):
    return Task(
        item["name"],
        arrow(tstr, tstr),
        [((ex["i"],), ex["o"]) for ex in item["examples"]],
    )

def get_tint_task(item):
   return Task(
      item["name"],
      arrow(tint, tint),
      [((ex["i"],), ex["o"]) for ex in item["examples"]],
    )

if __name__ == "__main__":
    print("Training on: " + str(NUM_TR) + " examples.")
    print("Testing on: " + str(NUM_TE) + " examples.")
    args = commandlineArguments(
        enumerationTimeout=1800, activation='tanh',
        iterations=10, recognitionTimeout=3600,
        a=3, maximumFrontier=10, topK=2, pseudoCounts=30.0,
        helmholtzRatio=0.5, structurePenalty=1.,
        CPUs=numberOfCPUs(), featureExtractor=StringFeatureExtractor, recognition_0=["examples"])
    
    timestamp = datetime.datetime.now().isoformat()
    outdir = 'experimentOutputs/demo/'
    os.makedirs(outdir, exist_ok=True)
    outprefix = outdir + timestamp
    args.update({"outputPrefix": outprefix})

    primitives = mathDomainPrimitives()

    grammar = Grammar.uniform(primitives)
    
    training_equations_list = [train_pair_X(k) for k in range(NUM_TR)] 
    
    print("Example of training equation: " + str(training_equations_list[0]))
    #generate {"i":, "o":} dicts for the different training examples
    training_examples = [{"name": "tr"+str(k), "examples": [training_equations_list[k] for _ in range(5000)]} for k in range(NUM_TR)]

    testing_equations_list = [test_pair_X(k) for k in range(NUM_TE)] #generate {"i":, "o":} dicts for the different testing examples
    testing_examples = [{"name": "te"+str(k), "examples": [testing_equations_list[k] for _ in range(5000)]} for k in range(NUM_TE)]

    index_equations_list = [index_pair_X(k) for k in range(11, 25)]
    index_equations_list = [eq for eq in index_equations_list]
    index_equations_list += index_equations_list
    index_examples = [{"name": "in"+str(k), "examples": [index_equations_list[k] for _ in range(5000)]} for k in range(len(index_equations_list))]

    training = [get_tstr_task(item) for item in training_examples] #+ [get_tint_task(item) for item in index_examples]
    #+ [get_tstr_task(item_2) for item_2 in testing_examples]

    print("Example of testing equation: " + str(testing_equations_list[0]))

    #testing_examples = [
    #    {"name": "add4", "examples": [ex4() for _ in range(500)]},
    #]
    
    testing = [get_tstr_task(item) for item in testing_examples]
    #testing_2 = []

    generator = ecIterator(grammar,
                           training,
                           testingTasks=testing,
                           **args)
    for i, _ in enumerate(generator):
        print('ecIterator count {}'.format(i))
