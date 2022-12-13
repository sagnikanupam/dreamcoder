import datetime
import os
import random

import binutil  # required to import from dreamcoder modules

from dreamcoder.ec import commandlineArguments, ecIterator
from dreamcoder.grammar import Grammar
from dreamcoder.program import Primitive
from dreamcoder.task import Task
from dreamcoder.type import arrow, tint, tstr
from dreamcoder.utilities import numberOfCPUs

# Configuration_faces : Up|Front|Right|Back|Left|Down
# Up 123 -> Back 321, Up 369 -> Right 321, Up 789 -> Front 123, Up 147 -> Left 123
solved_conf = "rrrrrrrrr|bbbbbbbbb|wwwwwwwww|ggggggggg|yyyyyyyyy|ooooooooo"

def cc_rotate(s):
    return s[6] + s[3] + s[0] + s[7] + s[4] + s[1] + s[8] + s[5] + s[2]

# Primitives
def _rotate_front(s): 
    [U, F, R, B, L, D] = s.split('|')
    
    F = cc_rotate(F)
    
    temp = U[6:]
    U = U[:6] + L[8] + L[5] + L[2]
    temp2 = R[0] + R[3] + R[6]
    R = temp[0] + R[1] + R[2] + temp[1] + R[4] + R[5] + temp[2] + R[7] + R[8]
    temp = D[2] + D[1] + D[0]
    D = temp2 + D[3:]    
    L = L[0] + L[1] + temp[0] + L[3] + L[4] + temp[1] + L[6] + L[7] + temp[2]

    return "|".join([U, F, R, B, L, D])

def _rotate_back(s): 
    [U, F, R, B, L, D] = s.split('|')
    
    B = cc_rotate(B)
    
    temp = U[2] + U[1] + U[0]
    U = R[2] + R[5] + R[8] + U[3:]
    temp2 = L[6] + L[3] + L[0]
    L = temp[0] + L[1] + L[2] + temp[1] + L[4] + L[5] + temp[2] + L[7] + L[8]
    temp = D[6] + D[7] + D[8]
    D = D[:6] + temp2    
    R = R[0] + R[1] + temp[0] + R[3] + R[4] + temp[1] + R[6] + R[7] + temp[2]

    return "|".join([U, F, R, B, L, D])

def _rotate_left(s): 
    [U, F, R, B, L, D] = s.split('|')
    
    L = cc_rotate(L)
    
    temp = U[0] + U[3] + U[6]
    U = B[8] + U[1] + U[2] + B[5] + U[4] + U[5] + B[2] + U[7] + U[8]
    temp2 = F[0] + F[3] + F[6]
    F = temp[0] + F[1] + F[2] + temp[1] + F[4] + F[5] + temp[2] + F[7] + F[8]
    temp = D[8] + D[5] + D[2]
    D = D[0] + D[1] + temp2[0] + D[3] + D[4] + temp2[1] + D[6] + D[7] + temp2[2]    
    B = B[0] + B[1] + temp[0] + B[3] + B[4] + temp[1] + B[6] + B[7] + temp[2]

    return "|".join([U, F, R, B, L, D])

def _rotate_right(s): 
    [U, F, R, B, L, D] = s.split('|')
    
    R = cc_rotate(R)
    
    temp = U[8] + U[5] + U[2]
    U = U[0] + U[1] + F[2] + U[3] + U[4] + F[5] + U[6] + U[7] + F[8]
    temp2 = B[6] + B[3] + B[0]
    B = temp[0] + B[1] + B[2] + temp[1] + B[4] + B[5] + temp[2] + B[7] + B[8]
    temp = D[0] + D[3] + D[6]
    D = temp2[0] + D[1] + D[2] + temp2[1] + D[4] + D[5] + temp2[2] + D[7] + D[8]  
    F = F[0] + F[1] + temp[0] + F[3] + F[4] + temp[1] + F[6] + F[7] + temp[2]

    return "|".join([U, F, R, B, L, D])

def _rotate_up(s): 
    [U, F, R, B, L, D] = s.split('|')
    
    U = cc_rotate(U)
    
    temp = F[:3]
    F = R[:3] + F[3:]
    temp2 = L[:3]
    L = temp + L[3:]
    temp = B[:3]
    B = temp2 + B[3:]    
    R = temp + R[3:]

    return "|".join([U, F, R, B, L, D])

def _rotate_down(s): 
    [U, F, R, B, L, D] = s.split('|')
    
    D = cc_rotate(D)
    
    temp = F[6:]
    F = F[:6] + L[6:]
    temp2 = R[6:]
    R = R[:6] + temp
    temp = B[6:]
    B = B[:6] + temp2    
    L = L[:6] + temp

    return "|".join([U, F, R, B, L, D])

def _op_prime(s, f):
    return f(f(f(s)))

def _rotate_up_prime(s):
    return _op_prime(s, _rotate_up)

def _rotate_down_prime(s):
    return _op_prime(s, _rotate_down)

def _rotate_front_prime(s):
    return _op_prime(s, _rotate_front)

def _rotate_back_prime(s):
    return _op_prime(s, _rotate_back)

def _rotate_left_prime(s):
    return _op_prime(s, _rotate_left)

def _rotate_right_prime(s):
    return _op_prime(s, _rotate_right)

fs = [_rotate_front, _rotate_back, _rotate_left, _rotate_right, _rotate_up, _rotate_down, _rotate_front_prime, _rotate_back_prime, _rotate_left_prime, _rotate_right_prime, _rotate_up_prime, _rotate_down_prime]

def config_from_indices(inds):
    conf = solved_conf
    for i in range(len(inds)):
        conf = fs[inds[i]](conf)
    return {"i": conf, "o": solved_conf}

def get_tstr_task(item):
    return Task(
        item["name"],
        arrow(tstr, tstr),
        [((ex["i"],), ex["o"]) for ex in item["examples"]],
    )


if __name__ == "__main__":

    # Options more or less copied from list.py

    args = commandlineArguments(
        enumerationTimeout=120, activation='tanh',
        iterations=3, recognitionTimeout=3600,
        a=3, maximumFrontier=10, topK=2, pseudoCounts=30.0,
        helmholtzRatio=0.5, structurePenalty=1.,
        CPUs=numberOfCPUs())

    timestamp = datetime.datetime.now().isoformat()
    outdir = 'experimentOutputs/demo/'
    os.makedirs(outdir, exist_ok=True)
    outprefix = outdir + timestamp
    args.update({"outputPrefix": outprefix})

    # Create list of primitives

    primitives = [
        Primitive("cubeF", arrow(tstr, tstr), _rotate_front),
        Primitive("cubeB", arrow(tstr, tstr), _rotate_back),
        Primitive("cubeL", arrow(tstr, tstr), _rotate_left),
        Primitive("cubeR", arrow(tstr, tstr), _rotate_right),
        Primitive("cubeU", arrow(tstr, tstr), _rotate_up),
        Primitive("cubeD", arrow(tstr, tstr), _rotate_down),
        Primitive("cubeFp", arrow(tstr, tstr), _rotate_front_prime),
        Primitive("cubeBp", arrow(tstr, tstr), _rotate_back_prime),
        Primitive("cubeLp", arrow(tstr, tstr), _rotate_left_prime),
        Primitive("cubeRp", arrow(tstr, tstr), _rotate_right_prime),
        Primitive("cubeUp", arrow(tstr, tstr), _rotate_up_prime),
        Primitive("cubeDp", arrow(tstr, tstr), _rotate_down_prime)
    ]

    # Create grammar

    grammar = Grammar.uniform(primitives)

    def scrambleN(n):
        # returns a randomized sequence of n integers corresponding to n random moves
        inds = []
        for i in range(n):
            inds.append(random.randint(0, len(fs)-1))
        return inds

    def kScrambles(k, n):
        # returns a list of k n-length scrambled configs
        scrambles = []
        for i in range(k):
            scrambles.append(scrambleN(n))
        return scrambles

    kTrain = 10    # Training data
    nMax = 15
    datasetScrambles = []
    for i in range(1, nMax):
        datasetScrambles += kScrambles(min((len(fs)**i), kTrain), i)
    print("Total Dataset Length is: " + str(len(datasetScrambles)) + " Training: " + str(len(datasetScrambles)-kTrain))
    training_examples = []
    for i in range(len(datasetScrambles)-kTrain):
        training_examples.append({"name": "scramble"+str(i), "examples": [config_from_indices(datasetScrambles[i]) for _ in range(5000)]})
    
    training = [get_tstr_task(item) for item in training_examples]

    # Testing data
    testing_examples = []
    
    for i in range(len(datasetScrambles)-kTrain, len(datasetScrambles)):
        testing_examples.append({"name": "scramble"+str(i), "examples": [config_from_indices(datasetScrambles[i]) for _ in range(5000)]})

    testing = [get_tstr_task(item) for item in testing_examples]

    # EC iterate

    generator = ecIterator(grammar,
                           training,
                           testingTasks=testing,
                           **args)
    for i, _ in enumerate(generator):
        print('ecIterator count {}'.format(i))