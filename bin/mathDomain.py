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

TRAINING_DATASET_FILEPATH = Path.cwd()/'data'/'mathDomain'/'trainingEquations.csv'
print(f"Training Dataset From: {TRAINING_DATASET_FILEPATH}")
training_data = pd.read_csv(TRAINING_DATASET_FILEPATH) #pandas dataframe containing training data
NUM_TR = training_data.shape[0] #number of training examples
print(f"Number of Equations Used For Training: {NUM_TR}")
TESTING_DATASET_FILEPATH = Path.cwd()/'data'/'mathDomain'/'testingEquations.csv'
print(f"Testing Dataset From: {TESTING_DATASET_FILEPATH}")
testing_data = pd.read_csv(TESTING_DATASET_FILEPATH, header=None) #pandas dataframe containing testing data
NUM_TE = testing_data.shape[0] #number of training examples
print(f"Number of Equations Used For Testing: {NUM_TE}")

def train_pair_X(x):
  input_output_dict = {"i": training_data.iat[x, 0], "o": training_data.iat[x, 1]}
  return input_output_dict

def test_pair_X(x):
  input_output_dict = {"i": testing_data.iat[x, 2], "o": testing_data.iat[x, 3]}
  return input_output_dict

def get_tstr_task(item):
    return Task(
        item["name"],
        arrow(tstr, tstr),
        [((ex["i"],), ex["o"]) for ex in item["examples"]],
    )

if __name__ == "__main__":

    args = commandlineArguments(
        enumerationTimeout=180, activation='tanh',
        iterations=5, recognitionTimeout=3600,
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
    
    training_equations_list = [train_pair_X(k) for k in range(NUM_TR)] #generate {"i":, "o":} dicts for the different training examples
    training_examples = [{"name": "tr"+str(k), "examples": [training_equations_list[k] for _ in range(5000)]} for k in range(NUM_TR)]

    training = [get_tstr_task(item) for item in training_examples]

    testing_equations_list = [test_pair_X(k) for k in range(NUM_TE)] #generate {"i":, "o":} dicts for the different testing examples
    testing_examples = [{"name": "te"+str(k), "examples": [testing_equations_list[k] for _ in range(5000)]} for k in range(NUM_TE)]

    #testing_examples = [
    #    {"name": "add4", "examples": [ex4() for _ in range(500)]},
    #]
    
    testing = [get_tstr_task(item) for item in testing_examples]
    
    generator = ecIterator(grammar,
                           training,
                           testingTasks=testing,
                           **args)
    for i, _ in enumerate(generator):
        print('ecIterator count {}'.format(i))


    '''
    [
        {"name": "ex0", "examples": [ex0() for _ in range(5000)]},
        {"name": "ex1", "examples": [ex1() for _ in range(5000)]},
        {"name": "ex2", "examples": [ex2() for _ in range(5000)]},
        {"name": "ex3", "examples": [ex3() for _ in range(5000)]},
        {"name": "ex4", "examples": [ex4() for _ in range(5000)]},
        {"name": "ex5", "examples": [ex5() for _ in range(5000)]},
        {"name": "ex6", "examples": [ex6() for _ in range(5000)]},
        {"name": "ex7", "examples": [ex7() for _ in range(5000)]},
        {"name": "ex8", "examples": [ex8() for _ in range(5000)]},
        {"name": "ex9", "examples": [ex9() for _ in range(5000)]},
        {"name": "ex10", "examples": [ex10() for _ in range(5000)]},
        {"name": "ex11", "examples": [ex11() for _ in range(5000)]},
        {"name": "ex12", "examples": [ex12() for _ in range(5000)]},
        {"name": "ex13", "examples": [ex13() for _ in range(5000)]},
        {"name": "ex14", "examples": [ex14() for _ in range(5000)]},
        {"name": "ex15", "examples": [ex15() for _ in range(5000)]},
        {"name": "ex16", "examples": [ex16() for _ in range(5000)]},
        {"name": "ex17", "examples": [ex17() for _ in range(5000)]},
    ]
    def ex0(): return exampleX(0)
    def ex1(): return exampleX(1)
    def ex2(): return exampleX(2)
    def ex3(): return exampleX(3)
    def ex4(): return exampleX(4)
    def ex5(): return exampleX(5)
    def ex6(): return exampleX(6)
    def ex7(): return exampleX(7)
    def ex8(): return exampleX(8)
    def ex9(): return exampleX(9)
    def ex10(): return exampleX(10)
    def ex11(): return exampleX(11)
    def ex12(): return exampleX(12)
    def ex13(): return exampleX(13)
    def ex14(): return exampleX(14)
    def ex15(): return exampleX(15)
    def ex16(): return exampleX(16)
    def ex17(): return exampleX(17)
    '''

    '''
  # return {"i": "(= ("+str(x)+") (x))", "o": "(= (x) ("+str(x)+"))"} # swap two sides of equation

  # return {"i": "(= (- (/ (+ (2) (3)) (5)) ("+str(x)+")) (y))", "o": "(= (y) ("+str(1-x)+"))"} #simplification
  s = type1(1, 3, 4, 5)
  inp = s["i"]
  out = s["o"]

  if x==0:
    return {
        "i": "(= (* (x) (2)) (5))", "o": "(= (x) (/ (5) (2)))" 
    }
  if x==1:
    return {
        "i": "(= (* (3) (x)) (5))", "o": "(= (x) (/ (5) (3)))" 
    }
  if x==2:
    return {
        "i": "(= (+ (x) (5)) (5))", "o": "(= (x) (0))" 
    }
  if x==3:
    return {
        "i": "(= (+ (5) (x)) (8))", "o": "(= (x) (3))" 
    }
  if x == 4:
    return {
        "i": "(= (+ (* (x) (3)) (4)) (5))", 
        "o": "(= (x) (/ (1) (3)))"
    }
  if x == 5:
    return {
        "i": "(= (+ (+ (* (x) (3)) (4)) (7)) (5))", 
        "o": "(= (x) (-2))"
    }
  if x == 6:
    return {
        "i": "(= (* (x) (6)) (* (x) (4)))", 
        "o": "(= (x) (0))"
    }
  if x == 7:
    return {
        "i": "(= (0) (+ (* (x) (2)) (* (x) (7))))", 
        "o": "(= (x) (0))"
    } 
  if x == 8:
    return {
    "i": "(= (* (5) (x)) (+ (+ (2) (* (3) (x))) (4)))",
    "o": "(= (x) (3))"
  }
  if x == 9:
    return {
        "i": "(= (5) (* (x) (2)))", "o": "(= (x) (/ (5) (2)))" 
    }
  if x == 10:
    return {
        "i": "(= (5) (* (3) (x)))", "o": "(= (x) (/ (5) (3)))" 
    }
  if x == 11:
    return {
        "i": "(= (5) (+ (x) (5)))", "o": "(= (x) (0))" 
    }
  if x == 12:
    return {
        "i": "(= (8) (+ (5) (x)))", "o": "(= (x) (3))" 
    }
  if x == 13:
    return {
        "i": "(= (5) (+ (* (x) (3)) (4)))", 
        "o": "(= (x) (/ (1) (3)))"
    }
  if x == 14:
    return {
        "i": "(= (5) (+ (+ (* (x) (3)) (4)) (7)))", 
        "o": "(= (x) (-2))"
    }
  if x == 15:
    return {
        "i": "(= (* (x) (4)) (* (x) (6)))", 
        "o": "(= (x) (0))"
    }
  if x == 16:
    return {
        "i": "(= (+ (* (x) (2)) (* (x) (7))) (0))", 
        "o": "(= (x) (0))"
    } 
  if x == 17:
    return {
    "i": "(= (+ (+ (2) (* (3) (x))) (4)) (* (5) (x)))",
    "o": "(= (x) (3))"
  }
  if x==18:
    return {
    "i": "(= (/ (3) (x)) (5))",
    "o": "(= (x) (/ (3) (5)))"
    }
  if x==19:
    return {
    "i": "(= (5) (/ (3) (x)))",
    "o": "(= (x) (/ (3) (5)))"    
    }
  if x==20:
    return {
        "i": "(= (- (x) (5)) (5))", "o": "(= (x) (10))" 
    }
  if x==21:
    return {
        "i": "(= (5) (- (x) (5)))", "o": "(= (x) (10))" 
    }
    '''
    '''
    def type1(a, b, c, d):
  gcd = math.gcd((a + c), (d - b))
  if (a + c) % (d - b) == 0:
    k = "(= (x) (" + str((a + c) // (d - b)) + "))"
  elif gcd != 1 and gcd != 0:
    k = "(= (x) (/ (" + str((a + c) // gcd) + ") (" + str(
      (d - b) // gcd) + ")))"
  else:
    k = "(= (x) (/ (" + str(a + c) + ") (" + str(d - b) + ")))"
  return {
    "i":
    "(= (+ (+ (" + str(a) + ") (* (" + str(b) + ") (x))) (" + str(c) +
    ")) (* (" + str(d) + ") (x)))",
    "o":
    k
  }
    '''