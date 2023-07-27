# Dataset Guide

This is a guide to the various .csv files present in this folder. CSV files affiliated with the
DreamSolver project are of two types: they are either datasets of equations, or files recording 
which problems DreamSolver/ConPole/Lemma were able to solve successfully.

Files formatted as `dsXofYsoln[Date].csv` (for example, `ds209of284soln7-10-2023`) refer to
DreamSolver attempting to solve a set equations on a certain date, where X = number of successfully solved equations
while Y = total number of equations attempted to be solved. All situations where Y = 284 refer to the
284 questions in the Cognitive Tutor Dataset provided by Poesia et al. in the ConPoLe repository. The
format of these .csv files is a column named 'output' followed by the terminal output of the most successful
result in that training experiment. Note that these do not contain enough information to replicate the experiment
since the training datasets may have been different (e.g. 209 relied on passing the 284 equations as testing and using 
trainingEquationsModified with 123 training equations for training).

- `ds134of284soln5-15-2023formatted.csv` is the result of running `mathDomainSolnProcessing.dsSolnFormat('ds134of284soln5-15-2023.csv', 'conpoleDatasetPrefix.csv', 'ds134of284soln5-15-2023formatted.csv')`
- `ds134of284soln5-15-2023evaluated.csv` is the result of running `mathDomainSolnProcessing.dsSolnEval('ds134of284soln5-15-2023formatted.csv', 'ds134of284soln5-15-2023evaluated.csv')`

For ConPoLe and Lemma solutions, `generatedConPoLeSolutions-CScores.csv`are the result
of running `clSolnEval('mathDomainSolnProcessing.generatedConpoleSolutions.csv', 'generatedConpoleSolutions-CScores.csv')` for computing C-Scores on ConPoLe solutions, and similarly, one can construct `generatedLemmaSolutions-CScores.csv` by using `mathDomainSolnProcessing.clSolnEval` to evaluate Lemma solutions. The files with a `_rand` prefix store the solutions to all the equations ConPoLe or Lemma were able to solve from a random subset of 100 equations of the original ConPoLe equation dataset as per the process in `mathDomainDatasetGeneration.py`

