from utilities import eprint
from frontier import *
from task import *
from type import *
from program import *
from grammar import *

import gc
import traceback
import subprocess
import threading


def multicoreEnumeration(g, tasks, likelihoodModel, _=None,
                         solver=None,
                         enumerationTimeout=None,
                         CPUs=1,
                         maximumFrontier=None,
                         verbose=True,
                         evaluationTimeout=None):
    '''g: Either a Grammar, or a map from task to grammar.'''
    from time import time

    # We don't use actual threads but instead use the multiprocessing
    # library. This is because we need to be able to kill workers.
    from multiprocessing import Process, Queue

    solvers = {"ocaml": solveForTask_ocaml,
               "pypy": solveForTask_pypy,
               "python": solveForTask_python}
    assert solver in solvers, \
        "You must specify a valid solver. options are ocaml, pypy, or python."
    solver = solvers[solver]

    if not isinstance(g, dict): g = {t: g for t in tasks }
    task2grammar = g

    # Bin the tasks by request type and grammar
    # If these are the same then we can enumerate for multiple tasks simultaneously
    jobs = {}
    for t in tasks:
        k = (task2grammar[t], t.request)
        jobs[k] = jobs.get(k,[]) + [t]

    # Map from task to the shortest time to find a program solving it
    bestSearchTime = {t: None for t in task2grammar}

    lowerBounds = {k: 0. for k in jobs}

    frontiers = {t: Frontier([], task = t) for t in task2grammar }

    # For each job we keep track of how long we have been working on it
    stopwatches = {t: Stopwatch() for t in jobs }

    def numberOfHits(f):
        return sum( e.logLikelihood == 0. for e in f)

    def budgetIncrement(lb):
        if True: return 1.5
        # Very heuristic - not sure what to do here
        if lb < 24.:
            return 1.
        elif lb < 27.:
            return 0.5
        else:
            return 0.25

    def maximumFrontiers(j):
        tasks = jobs[j]
        return {t: maximumFrontier - numberOfHits(frontiers[t]) for t in tasks}

    def allocateCPUs(n, tasks):
        allocation = {t: 0 for t in tasks }
        while n > 0:
            for t in tasks:
                allocation[t] += 1
                n -= 1
                if n == 0: break
        return allocation        

    def refreshJobs():
        ks = jobs.keys()
        for k in ks:
            v = [t for t in jobs[k]
                 if numberOfHits(frontiers[t]) < maximumFrontier
                 and stopwatches[k].elapsed <= enumerationTimeout ]
            if v:
                jobs[k] = v
            else:
                del jobs[k]                

    # Workers put their messages in here
    q = Queue()

    # How many CPUs are we using?
    activeCPUs = 0

    # How many CPUs was each job allocated?
    id2CPUs = {}
    # What job was each ID working on?
    id2job = {}
    nextID = 0

    while True:
        refreshJobs()
        # Don't launch a job that we are already working on
        # We run the stopwatch whenever the job is being worked on
        # freeJobs are things that we are not working on but could be
        freeJobs = [ j for j in jobs if not stopwatches[j].running
                     and stopwatches[j].elapsed < enumerationTimeout - 0.5 ]
        if freeJobs and activeCPUs < CPUs:
            # Allocate a CPU to each of the jobs that we have made the least progress on
            freeJobs.sort(key = lambda j: lowerBounds[j])
            # Launch some more jobs until all of the CPUs are being used
            availableCPUs = CPUs - activeCPUs
            allocation = allocateCPUs(availableCPUs, freeJobs)                
            for j in freeJobs:
                if allocation[j] == 0: continue
                g,request = j
                bi = budgetIncrement(lowerBounds[j])
                thisTimeout = enumerationTimeout - stopwatches[j].elapsed
                launchParallelProcess(wrapInThread(solver),
                                      q = q, g = g, ID = nextID,
                                      elapsedTime = stopwatches[j].elapsed,
                                      CPUs = allocation[j],
                                      tasks = jobs[j],
                                      lowerBound = lowerBounds[j],
                                      upperBound = lowerBounds[j] + bi,
                                      budgetIncrement = bi,
                                      timeout = thisTimeout,
                                      likelihoodModel = likelihoodModel,
                                      evaluationTimeout = evaluationTimeout,
                                      maximumFrontiers = maximumFrontiers(j))
                eprint("(python) Launching %s (%d tasks) w/ %d CPUs. %f <= MDL < %f. Timeout %f."%
                       (request, len(jobs[j]), allocation[j], lowerBounds[j], lowerBounds[j] + bi, thisTimeout))
                id2CPUs[nextID] = allocation[j]
                id2job[nextID] = j
                nextID += 1                

                stopwatches[j].start()
                activeCPUs += allocation[j]
                lowerBounds[j] += bi

        # If nothing is running, and we just tried to launch jobs,
        # then that means we are finished
        if all( not s.running for s in stopwatches.values() ): break
        
        # Wait to get a response
        message = Bunch(q.get())

        if message.result == "failure":
            eprint("PANIC! Exception in child worker:", message.exception)
            eprint(message.stacktrace)
            assert False
        elif message.result == "success":
            # Mark the CPUs is no longer being used and pause the stopwatch
            activeCPUs -= id2CPUs[message.ID]
            stopwatches[id2job[message.ID]].stop()

            newFrontiers, searchTimes = message.value
            for t,f in newFrontiers.iteritems():
                frontiers[t] = frontiers[t].combine(f)
                dt = searchTimes[t]
                if dt is not None:
                    if bestSearchTime[t] is None: bestSearchTime[t] = dt
                    else: bestSearchTime[t] = min(bestSearchTime[t],dt)
        else:
            eprint("Unknown message result:",message.result)
            assert False
            
    return [frontiers[t] for t in tasks ], [bestSearchTime[t] for t in tasks if bestSearchTime[t] is not None ]
            


                
            
        
        

    

def multithreadedEnumeration(g, tasks, likelihoodModel, _=None,
                             solver=None,
                             frontierSize=None,
                             enumerationTimeout=None,
                             CPUs=1,
                             maximumFrontier=None,
                             verbose=True,
                             evaluationTimeout=None):
    '''g: Either a Grammar, or a map from task to grammar.'''
    from time import time

    # We don't use actual threads but instead use the multiprocessing
    # library. This is because we need to be able to kill workers.
    from multiprocessing import Process, Queue

    assert frontierSize is None, "deprecated: frontierSize"

    solvers = {"ocaml": solveForTask_ocaml,
               "pypy": solveForTask_pypy,
               "python": solveForTask_python}
    assert solver in solvers, \
        "You must specify a valid solver. options are ocaml, pypy, or python."
    solver = solvers[solver]

    if not isinstance(g, dict): g = {t: g for t in tasks }
    task2grammar = g

    frontiers = {t: Frontier([], task = t) for t in task2grammar }

    # Tasks which have not yet been solved
    activeTasks = set(task2grammar.keys())

    # Largest lower bound of any workerthat is assigned to a task
    lowerBounds = {t: 0. for t in task2grammar}

    # Map from task to the shortest time to find a program solving it
    bestSearchTime = {t: None for t in task2grammar}

    # For each task we keep track of how long we have been working on it
    stopwatches = {t: Stopwatch() for t in tasks }

    # Total number of evaluated programs
    totalExplored = 0

    # Each worker is assigned a unique ID number
    nextID = 0

    # map from ID to task
    workers = {}

    def numberOfHits(f):
        return sum( e.logLikelihood == 0. for e in f)

    def budgetIncrement(lb):
        # Very heuristic - not sure what to do here
        if lb < 24.:
            return 1.
        elif lb < 27.:
            return 0.5
        else:
            return 0.25

    startTime = time()

    # Workers put their messages in here
    q = Queue()

    while True:
        activeTasks = {t for t in activeTasks
                       if len(frontiers[t]) < maximumFrontier \
                       and stopwatches[t].elapsed <= enumerationTimeout }

        finished = len(activeTasks) == 0

        if not finished:
            while len(workers) < CPUs:
                # Sort the tasks by lower bound. Prioritize lower
                # lower bounds to explore shorter programs first
                for t in sorted(activeTasks, key = lambda t: lowerBounds[t])[:CPUs-len(workers)]:
                    thisTimeout = enumerationTimeout - stopwatches[t].elapsed
                    if not stopwatches[t].running: stopwatches[t].start()
                    eprint("Launching [%s] w/ lb = %f, timeout = %f"%(t,lowerBounds[t],thisTimeout))
                    bi = budgetIncrement(lowerBounds[t])
                    launchParallelProcess(wrapInThread(solver),
                                          q = q, ID = nextID,
                                          elapsedTime = stopwatches[t].elapsed,
                                          g = task2grammar[t],
                                          task = t,
                                          lowerBound = lowerBounds[t],
                                          upperBound = lowerBounds[t] + bi,
                                          budgetIncrement = bi,
                                          timeout = thisTimeout,
                                          likelihoodModel = likelihoodModel,
                                          evaluationTimeout = evaluationTimeout,
                                          maximumFrontier = maximumFrontier - numberOfHits(frontiers[t]))
                    lowerBounds[t] += bi
                    workers[nextID] = t
                    nextID += 1

        if len(workers) > 0:
            message = Bunch(q.get())
            ID = message.ID
            if message.result == "fork":
                assert False, "Forking message is deprecated"
            elif message.result == "failure":
                eprint("PANIC! Exception in child worker:", message.exception)
                eprint(message.stacktrace)
                assert False
            elif message.result == "success":
                frontier, searchTime, explored = message.value
                task = workers[ID]

                totalExplored += explored
                if totalExplored > 0:
                    eprint("(python) Explored %d programs in %s sec. %d programs/sec. CPU load: %s."%
                           (totalExplored,
                            int(time() - startTime),
                            int(float(totalExplored)/(time() - startTime)),
                            CPULoad()))

                if searchTime is not None:
                    if bestSearchTime[task] is None:
                        eprint("(python) Got first solution to %s after %s wall clock seconds"%(task,int(searchTime+0.5)))
                        bestSearchTime[task] = searchTime
                    else: bestSearchTime[task] = min(searchTime, bestSearchTime[task])
                frontiers[task] = frontiers[task].combine(frontier)

                # Remove the finished worker
                del workers[ID]

                # stop it stopwatch if the task is no longer being
                # worked on
                if not any( task == _task for _task in workers.values() ):
                    stopwatches[task].stop()

        if finished and len(workers) == 0 and q.empty(): break

    eprint("Completed multithreaded enumeration for",len(tasks),"tasks in",int(time() - startTime),"s")
    pps = float(totalExplored)/(time() - startTime)
    eprint("program evaluations per second:",int(pps))
    eprint("program evaluations per CPU second:",int(pps/CPUs))

    return [frontiers[t] for t in tasks], [bestSearchTime[t] for t in tasks if bestSearchTime[t] is not None ]






def wrapInThread(f):
    """
    Returns a function that is designed to be run in a thread/threadlike process.
    Result will be either put into the q
    """

    def _f(*a,**k):
        q = k.pop("q")
        ID = k.pop("ID")

        try:
            r = f(*a,**k)
            q.put({"result": "success",
                   "ID": ID,
                   "value": r})
        except Exception as e:
            q.put({"result": "failure",
                   "exception": e,
                   "stacktrace": traceback.format_exc(),
                   "ID": ID})
            return
    return _f

def solveForTask_ocaml(_ = None,
                       elapsedTime = 0.,
                       CPUs=1,
                       g = None, tasks = None,
                       lowerBound = None, upperBound = None, budgetIncrement = None,
                       timeout = None,
                       likelihoodModel = None, # FIXME: unused
                       evaluationTimeout = None, maximumFrontiers = None):
    import json
    message = {"DSL": {"logVariable": g.logVariable,
                       "productions": [ {"expression": str(p), "logProbability": l}
                                            for l,_,p in g.productions ]},
               "tasks": [{
                   "examples": [{"inputs": list(xs), "output": y} for xs,y in t.examples ],
                   "name": t.name,
                   "maximumFrontier": maximumFrontiers[t]}
                   for t in tasks ],
               
               "programTimeout": evaluationTimeout,
               "nc": CPUs,
               "timeout": timeout,
               "lowerBound": lowerBound,
               "upperBound": upperBound,
               "budgetIncrement": budgetIncrement,
               "verbose": False}
    task = tasks[0]
    if hasattr(task, 'BIC'):
        message["parameterPenalty"] = task.BIC*math.log(len(task.examples))
    if hasattr(task, 'likelihoodThreshold') and task.likelihoodThreshold is not None:
        message["lossThreshold"] = -task.likelihoodThreshold
    if hasattr(task, 'maxParameters') and task.maxParameters is not None:
        message["maxParameters"] = task.maxParameters

    message = json.dumps(message)
    # with open("pipe", "w") as f:
        # f.write(message)
    try:
        process = subprocess.Popen("./solver",
                                   stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE)
        response, error = process.communicate(message)
        response = json.loads(response)
    except OSError as exc:
        raise exc

    pc = 0 # TODO
    frontiers = {}
    searchTimes = {}
    for t in tasks:
        solutions = response[t.name]
        # Remove all entries that do not type correctly
        # This can occur because the solver tries to infer the type
        # Sometimes it infers a type that is too general
        solutions = [r for r in solutions if Program.parse(r["program"]).canHaveType(t.request) ]
        frontier = Frontier([FrontierEntry(program = p,
                                           logLikelihood = e["logLikelihood"],
                                           logPrior = g.logLikelihood(t.request, p))
                             for e in solutions
                             for p in [Program.parse(e["program"])] ],
                            task = t)
        frontiers[t] = frontier
        if frontier.empty: searchTimes[t] = None
        else: searchTimes[t] = min(e["time"] for e in solutions) + elapsedTime
        
    return frontiers, searchTimes

def solveForTask_pypy(_ = None,
                      elapsedTime = 0.,
                      g = None, task = None,
                      lowerBound = None, upperBound = None, budgetIncrement = None,
                      timeout = None,
                      likelihoodModel = None,
                      evaluationTimeout = None, maximumFrontier = None):
    return callCompiled(enumerateForTask,
                        g,task,likelihoodModel,
                        timeout = timeout,
                        evaluationTimeout = evaluationTimeout,
                        maximumFrontier = maximumFrontier,
                        budgetIncrement = budgetIncrement,
                        lowerBound = lowerBound,
                        upperBound = upperBound)

def solveForTask_python(_ = None,
                        elapsedTime = 0.,
                        g = None, task = None,
                        lowerBound = None, upperBound = None, budgetIncrement = None,
                        timeout = None,
                        likelihoodModel = None,
                        evaluationTimeout = None, maximumFrontier = None):
    return enumerateForTask(g,task,likelihoodModel,
                            timeout = timeout,
                            evaluationTimeout = evaluationTimeout,
                            maximumFrontier = maximumFrontier,
                            budgetIncrement = budgetIncrement,
                            lowerBound = lowerBound, upperBound = upperBound)

class EnumerationTimeout(Exception): pass
def enumerateForTask(g, task, likelihoodModel, _ = None,
                     verbose=False,
                     timeout=None,
                     evaluationTimeout=None,
                     frontierSize=None,
                     lowerBound = 0.,
                     upperBound = 100.,
                     budgetIncrement=1.0, maximumFrontier = 10**2):
    assert (timeout is not None) or (frontierSize is not None), \
        "enumerateForTask: You must provide either a timeout or a frontier size."

    from time import time

    timeUntilFirstSolution = None
    frontier = []
    starting = time()
    previousBudget = lowerBound
    budget = lowerBound + budgetIncrement
    try:
        totalNumberOfPrograms = 0
        while len(frontier) < maximumFrontier:
            numberOfPrograms = 0
            for prior,_,p in g.enumeration(Context.EMPTY, [], task.request,
                                           maximumDepth = 99,
                                           upperBound = budget,
                                           lowerBound = previousBudget):
                descriptionLength = -prior
                # Shouldn't see it on this iteration
                assert descriptionLength <= budget
                # Should already have seen it
                assert descriptionLength > previousBudget

                numberOfPrograms += 1
                totalNumberOfPrograms += 1

                success, likelihood = likelihoodModel.score(p, task)
                if success:
                    if verbose:
                        eprint("Hit",task.name,"with the program",p,"which has prior",prior,"after",time() - starting,"seconds")
                    if frontier == []: timeUntilFirstSolution = time() - starting
                    frontier.append(FrontierEntry(program = p,
                                                  logPrior = prior,
                                                  logLikelihood = likelihood))

                if timeout is not None and time() - starting > timeout:
                    raise EnumerationTimeout
            if verbose:
                eprint("Enumerated %d programs of satisfying:"%(numberOfPrograms),
                       "%d < MDL <= %d."%(int(previousBudget),int(budget)))

            previousBudget = budget
            budget += budgetIncrement
            if verbose:
                eprint("\tTotal elapsed time: %d seconds. Total number of programs evaluated: %d. Task: %s."% \
                       (time() - starting, totalNumberOfPrograms, task))
            if frontierSize is not None and totalNumberOfPrograms > frontierSize: break
            if budget > upperBound: break
    except EnumerationTimeout:
        if verbose:
            eprint("Timeout triggered after",time() - starting,"seconds for task",task)

    frontier = Frontier(frontier,
                        task = task).topK(maximumFrontier)

    return frontier, timeUntilFirstSolution, numberOfPrograms

def solveSingleTask(grammar, task, maximumBudget = 15):
    if isinstance(task, DifferentiableTask):
        rememberOld = True
        history = set([])
    else: rememberOld = False
    for budget in range(2, maximumBudget):
        for _,_,p in grammar.enumeration(Context.EMPTY, [], task.request, budget):
            if rememberOld:
                if p in history: continue
                history.add(p)
            l = task.logLikelihood(p)
            if valid(l): return l,p
    return None

def benchmarkSynthesisTimes(result, tasks, _ = None, timeout = None, CPUs = None):
    if result.parameters['useRecognitionModel']:
        assert hasattr(result, 'recognitionModel') and result.recognitionModel is not None, \
            "Checkpoint was trained using a recognition model but it does not have a saved recognition model."

    times = parallelMap(CPUs, lambda task: benchmarkSynthesisTime(result, task, timeout), tasks)
    timeouts = sum(t == None for t in times)
    successes = sum(t != None for t in times)
    if successes > 0:
        average = sum(t[0] for t in times if t != None)/float(successes)
        deviation = (sum( (t[0] - average)**2 for t in times if t != None )/float(successes))**0.5
        standardError = deviation/(float(successes)**0.5)
    eprint("BENCHMARK:")
    eprint("Solves %d/%d = %d%%"%(successes, len(tasks), int(100.*successes/len(tasks))))
    if successes > 0:
        eprint("Synthesis time %f +/- %f sec"%(average, standardError))
        average = sum(t[1] for t in times if t != None)/float(successes)
        deviation = (sum( (t[1] - average)**2 for t in times if t != None )/float(successes))**0.5
        standardError = deviation/(float(successes)**0.5)
        eprint("Expected log P[t|p] =",average,"+/-",standardError)

def benchmarkSynthesisTime(result, task, timeout):
    grammar = result.grammars[-1]

    from likelihoodModel import AllOrNothingLikelihoodModel
    from time import time
    import signal

    startTime = time()
    if result.parameters['useRecognitionModel']:
        # Because grammar induction is the last step of EC, the
        # recognition model is actually trained for the second to last
        # grammar
        grammar = result.grammars[-2]
        features = result.recognitionModel.featureExtractor.featuresOfTask(task)
        variables, productions = result.recognitionModel(features)
        grammar = Grammar(variables.data[0],
                          [ (productions.data[k],t,p)
                            for k,(_,t,p) in enumerate(grammar.productions) ])

    elapsed = time() - startTime
    frontier = callCompiled(enumerateForTask,
                            grammar, task, AllOrNothingLikelihoodModel,
                            maximumFrontier = 1,
                            timeout = timeout - elapsed)
    dt = time() - startTime
    if dt > timeout or len(frontier) == 0: return None
    l = solution.entries[0].logLikelihood
    p = solution.entries[0].program
    eprint("Solved",task,"w/",p,"(log likelihood of task given program:",l,").","in time",dt)
    return dt,l

