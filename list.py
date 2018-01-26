from ec import explorationCompression, commandlineArguments
from utilities import eprint
from listPrimitives import primitives
from grammar import Grammar

import cPickle as pickle

if __name__ == "__main__":
    try:
        with open("data/list_tasks.pkl") as f:
            tasks = pickle.load(f)
    except Exception as e:
        from makeListTasks import main
        main()
        with open("data/list_tasks.pkl") as f:
            tasks = pickle.load(f)

    eprint("Got {} list tasks".format(len(tasks)))

    baseGrammar = Grammar.uniform(primitives)
    explorationCompression(baseGrammar, tasks,
                           outputPrefix="experimentOutputs/list",
                           **commandlineArguments(frontierSize=20000,
                                                  activation='sigmoid',
                                                  a=2,
                                                  topK=2,
                                                  CPUs=4,
                                                  iterations=10,
                                                  pseudoCounts=10.0))
