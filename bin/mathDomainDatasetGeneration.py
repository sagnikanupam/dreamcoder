'''
Generate a random subset of equations.
'''

from pathlib import Path
import random
import binutil 
import pandas as pd

TESTING_DATASET_FILEPATH = Path.cwd()/'data'/'mathDomain'/'conpoleDatasetPrefix.csv'

df_test = pd.read_csv(TESTING_DATASET_FILEPATH)
df_new = df_test.sample(n=100)
equations_new = df_new["Infix_Eq"].values.tolist()

df_lm = pd.read_csv("bin/generatedLemmaSolutions-CScores.csv")
df_cp = pd.read_csv("bin/generatedConpoleSolutions-CScores.csv")

lm_soleq = df_lm['eqn'].values.tolist()
cp_soleq = df_cp['eqn'].values.tolist()

lm_eqn_no = []
lm_eqn = []
lm_soln = []
lm_metrics = []

cp_eqn_no = []
cp_eqn = []
cp_soln = []
cp_metrics = []

for equation in equations_new:
    if equation in lm_soleq:
        lm_ind = lm_soleq.index(equation)
        lm_eqn_no.append(df_lm.loc[lm_ind]["Equation Number"])
        lm_eqn.append(df_lm.loc[lm_ind]["eqn"])
        lm_soln.append(df_lm.loc[lm_ind]["soln"])
        lm_metrics.append(df_lm.loc[lm_ind]["metrics"])
    if equation in cp_soleq:
        cp_ind = cp_soleq.index(equation)
        cp_eqn_no.append(df_cp.loc[lm_ind]["Equation Number"])
        cp_eqn.append(df_cp.loc[lm_ind]["eqn"])
        cp_soln.append(df_cp.loc[lm_ind]["soln"])
        cp_metrics.append(df_cp.loc[lm_ind]["metrics"])
#print(df_new.head)
df_new.to_csv(Path.cwd()/'data'/'mathDomain'/'conpoleDatasetPrefixRandom.csv', index=False)
df_lm_rand = pd.DataFrame()
df_lm_rand["Equation Number"] = lm_eqn_no
df_lm_rand["eqn"] = lm_eqn
df_lm_rand["soln"] = lm_soln
df_lm_rand["metrics"] = lm_metrics

df_cp_rand = pd.DataFrame()
df_cp_rand["Equation Number"] = cp_eqn_no
df_cp_rand["eqn"] = cp_eqn
df_cp_rand["soln"] = cp_soln
df_cp_rand["metrics"] = cp_metrics
df_lm_rand.to_csv(Path.cwd()/'bin'/'generatedLemmaSolutions-CScores_rand.csv')
df_cp_rand.to_csv(Path.cwd()/'bin'/'generatedConpoleSolutions-CScores_rand.csv')