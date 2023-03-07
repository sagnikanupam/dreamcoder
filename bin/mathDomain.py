import datetime
import os
import random
import math

import binutil  # required to import from dreamcoder modules

from dreamcoder.ec import commandlineArguments, ecIterator
from dreamcoder.grammar import Grammar
from dreamcoder.program import Primitive
from dreamcoder.task import Task
from dreamcoder.type import arrow, tint, tstr
from dreamcoder.utilities import numberOfCPUs
from dreamcoder.domains.re2.main import StringFeatureExtractor
from dreamcoder.domains.mathDomain.mathDomainPrimitives import mathDomainPrimitives

def type1(a, b, c, d):
    gcd = math.gcd((a+c), (d-b))
    if (a+c)%(d-b)==0:
        k = "(= (x) ("+str((a+c)//(d-b))+"))"
    elif gcd!=1 and gcd!=0:
        k = "(= (x) (/ ("+str((a+c)//gcd)+") ("+str((d-b)//gcd)+")))"
    else:
        k = "(= (x) (/ ("+str(a+c)+") ("+str(d-b)+")))"
    return {"i": "(= (+ (+ ("+str(a)+") (* ("+str(b)+") (x))) ("+str(c)+"))  (* ("+str(d)+") (x)))", "o": k}

def exampleX(x):
    # return {"i": "(= ("+str(x)+") (x))", "o": "(= (x) ("+str(x)+"))"} # swap two sides of equation

    #return {"i": "(= (- (/ (+ (2) (3)) (5)) ("+str(x)+")) (y))", "o": "(= (y) ("+str(1-x)+"))"} #simplification

    if x==1:
        return type1(1, 3, 4, 5)
    if x==2:
        return type1(2, 2, 2, 4)
    if x==3:
        return type1(3, 1, 3, 5)
    if x==4:
        return type1(2, 3, 2, 4)

def get_tstr_task(item):
    return Task(
        item["name"],
        arrow(tstr, tstr),
        [((ex["i"],), ex["o"]) for ex in item["examples"]],
    )


if __name__ == "__main__":

    args = commandlineArguments(
        enumerationTimeout=10, activation='tanh',
        iterations=1, recognitionTimeout=3600,
        a=3, maximumFrontier=10, topK=2, pseudoCounts=30.0,
        helmholtzRatio=0.5, structurePenalty=1.,
        CPUs=numberOfCPUs())
    
    timestamp = datetime.datetime.now().isoformat()
    outdir = 'experimentOutputs/demo/'
    os.makedirs(outdir, exist_ok=True)
    outprefix = outdir + timestamp
    args.update({"outputPrefix": outprefix})

    primitives = mathDomainPrimitives()

    grammar = Grammar.uniform(primitives)

    def ex1(): return exampleX(1)
    def ex2(): return exampleX(2)
    def ex3(): return exampleX(3)
    def ex4(): return exampleX(4)

    training_examples = [
        {"name": "ex1", "examples": [ex1() for _ in range(5000)]},
        {"name": "ex2", "examples": [ex2() for _ in range(5000)]},
        {"name": "ex3", "examples": [ex3() for _ in range(5000)]},
    ]

    training = [get_tstr_task(item) for item in training_examples]

    testing_examples = [
        {"name": "add4", "examples": [ex4() for _ in range(500)]},
    ]
    
    testing = [get_tstr_task(item) for item in testing_examples]
    
    generator = ecIterator(grammar,
                           training,
                           testingTasks=testing,
                           **args)
    for i, _ in enumerate(generator):
        print('ecIterator count {}'.format(i))