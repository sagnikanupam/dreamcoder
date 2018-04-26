from ec import explorationCompression, commandlineArguments, Task
from grammar import Grammar
from utilities import eprint, testTrainSplit, numberOfCPUs
from makeTextTasks import makeTasks, delimiters, loadPBETasks
from textPrimitives import primitives
from listPrimitives import bootstrapTarget
from program import *
from recognition import *

import random

class LearnedFeatureExtractor(RecurrentFeatureExtractor):
    def tokenize(self, examples):
        return examples

    def __init__(self, tasks):
        lexicon = {c
                   for t in tasks
                   for xs,y in self.tokenize(t.examples)
                   for c in reduce(lambda u,v: u+v, list(xs) + [y]) }
                
        super(LearnedFeatureExtractor, self).__init__(lexicon = list(lexicon),
                                                      H = 64,
                                                      tasks = tasks,
                                                      bidirectional = True)


if __name__ == "__main__":
    tasks = makeTasks()
    eprint("Generated",len(tasks),"tasks")

    test, train = testTrainSplit(tasks, 0.9)
    eprint("Split tasks into %d/%d test/train"%(len(test),len(train)))

    challenge, challengeCheating = loadPBETasks()
    eprint("Got %d challenge PBE tasks"%len(challenge))

    baseGrammar = Grammar.uniform(primitives + bootstrapTarget())

    evaluationTimeout = 0.0005
    # We will spend five minutes on each challenge problem
    challengeTimeout = 5 * 60
    
    generator = ecIterator(baseGrammar, train,
                           testingTasks = test,
                           outputPrefix = "experimentOutputs/text",
                           evaluationTimeout = evaluationTimeout,
                           compressor="pypy", # 
                           **commandlineArguments(
                               steps = 500,
                               iterations = 10,
                               helmholtzRatio = 0.5,
                               topK = 2,
                               maximumFrontier = 2,
                               structurePenalty = 10.,
                               a = 3,
                               activation = "tanh",
                               CPUs = numberOfCPUs(),
                               featureExtractor = LearnedFeatureExtractor,
                               pseudoCounts = 10.0))

    for result in generator:
        eprint("Evaluating on challenge problems...")
        recognizer = result.recognitionModel
        challengeFrontiers, _ = recognizer.enumerateFrontiers(challenge, likelihoodModel,
                                                              CPUs=numberOfCPUs(),
                                                              solver="ocaml",
                                                              maximumFrontier=1,
                                                              enumerationTimeout=300,
                                                              evaluationTimeout=evaluationTimeout)
        eprint("Challenge problem enumeration results:")
        eprint(Frontier.describe(challengeFrontiers))
