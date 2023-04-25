'''
Problem Types Covered in https://github.com/gpoesia/socratic-tutor/blob/master/data/human_solutions.json and https://github.com/gpoesia/socratic-tutor/blob/master/data/cognitive_tutor_templates.txt

Parentheses are present in original problem, square brackets indicate simplification. E.g. (A+Bx) = 3 + 5x and [A+B] = 8 when A=3, B=5

1. (A + Bx + C = Dx, x=[A+C]/[D-B])
2. (A + Bx = Cx + D, x = [D-A]/[B-C])
3. (Ax = B, x = [B/A])
4. (Ax + Bx = C, x = C/[A+B])
5. (A = B + C/x, x = C/[A-B])
6. (A + B = Cx + D + E, x = ([A+B] - [D+E])/C)
7. (Ax/B = C/D, x = [B*C]/[A*D])
8. (x = (A-B)/C, x = [A-B]/C)
9. (Ax = B - Cx + D, x=[B+D]/[A+C])
10. ((A/x)*x = Bx, x=A/B)
11. (Ax + B = C, x=[C-B]/A)

Not Implemented Yet
-12. (Ax + Bx + C = D, x=[D-C]/[A+B])
-13. (A/Bx = C, x = A/[BC])
-14. (Ax + Bx = C + Dx - Ex, x= C/[A+B-D+E])
-15. (Ax + Bx = C + D, x=[C+D]/[A+B])
-16. (A = Bx + C, x=[A-C]/B)
-17. (Ax = B + C, x=[B+C]/A)
-18. (Ax + B = Cx, x=B/[C-A])
-19. (Ax = B + Cx, x=B/[A-C])
-20. (A + B = C/x - D + E, x=C/[A+B+D-E])
'''

import csv
import random

NUM_EQ = 80 #number of equations to be generated for each type
CONSTANT_RANGE = 9 #sets the range of constants used in linear equations to [-CONSTANT_RANGE, CONSTANT_RANGE]
data_file = open('testingEquations.csv', 'w')
 
# create the csv writer object
csv_writer = csv.writer(data_file)
header = ["infix_i", "infix_o", "prefix_i", "prefix_o"]


def reducefract(n, d):
    '''Reduces fractions. n is the numerator and d the denominator.
    Outputs tuple (n', d') where n'/d' is the reduced fraction.'''
    def gcd(n, d):
        while d != 0:
            t = d
            d = n%d
            n = t
        return n if (n!=0) else 1
    greatest=gcd(n,d)
    n/=greatest
    d/=greatest
    return (int(n), int(d))

def outputs(reduced):
    ''' Generates infix and prefix output tuples from reduced fractions. 
    '''
    n = reduced[0]
    d = reduced[1]
    if d==1 or n==0:
        return f"x={n}", f"(= (x) ({n}))"
    else:
        return f"x={n}/{d}", f"(= (x) (/ ({n}) ({d})))" 

term_Ax = []
for integer in range(-CONSTANT_RANGE, CONSTANT_RANGE+1):
    if integer==1:
        term_Ax.append((integer, "(x)", "x"))
    elif integer==0:
        term_Ax.append((integer, "(0)", "0"))  
    else:
        term_Ax.append((integer, f"(* ({integer}) (x))", f"{integer}x"))

term_const = []
for integer in range(-CONSTANT_RANGE, CONSTANT_RANGE+1):
    term_const.append((integer, f"({integer})", f"{integer}"))

term_A_by_x = []
for integer in range(-CONSTANT_RANGE, CONSTANT_RANGE+1):
    if integer==0:
        term_A_by_x.append((integer, "(0)", "0"))  
    else:
        term_A_by_x.append((integer, f"(/ ({integer}) (x))", f"({integer}/x)"))

def type1():
    type_1_list = []
    for A in term_const:
        for B in term_Ax:
            for C in term_const:
                for D in term_Ax:
                    if D[0]!=B[0]: 
                        infix_i = f"(({A[2]}+{B[2]})+{C[2]})={D[2]}"
                        prefix_i = f"(= (+ (+ {A[1]} {B[1]}) {C[1]}) {D[1]})"
                        infix_o, prefix_o = outputs(reducefract(A[0]+C[0], D[0]-B[0]))
                        type_1_list.append([infix_i, infix_o, prefix_i, prefix_o])
    type_1_selected = random.sample(type_1_list, min(len(type_1_list), NUM_EQ))
    for problem in type_1_selected:
        csv_writer.writerow(problem)
                
def type2():
    type_2_list = []
    for A in term_const:
        for B in term_Ax:
            for C in term_Ax:
                for D in term_const:
                    if C[0]!=B[0]:
                        infix_i = f"({A[2]}+{B[2]})=({C[2]}+{D[2]})"
                        prefix_i = f"(= (+ {A[1]} {B[1]}) (+ {C[1]} {D[1]}))"
                        infix_o, prefix_o = outputs(reducefract(D[0]-A[0], B[0]-C[0])) 
                        type_2_list.append([infix_i, infix_o, prefix_i, prefix_o])
    type_2_selected = random.sample(type_2_list, min(len(type_2_list), NUM_EQ))
    for problem in type_2_selected:
        csv_writer.writerow(problem)

def type3():
    type_3_list = []
    for A in term_Ax:
        for B in term_const:
            if A[0]!=0:
                infix_i = f"{A[2]}={B[2]}"
                prefix_i = f"(= {A[1]} {B[1]})"
                infix_o, prefix_o = outputs(reducefract(B[0], A[0]))
                type_3_list.append([infix_i, infix_o, prefix_i, prefix_o])
    type_3_selected = random.sample(type_3_list, min(len(type_3_list), NUM_EQ))
    for problem in type_3_selected:
        csv_writer.writerow(problem) 

def type4():
    type_4_list = []
    for A in term_Ax:
        for B in term_Ax:
            for C in term_const:
                if A[0]+B[0]!=0:
                    infix_i = f"({A[2]}+{B[2]})={C[2]}"
                    prefix_i = f"(= (+ {A[1]} {B[1]}) {C[1]})"
                    infix_o, prefix_o = outputs(reducefract(C[0], A[0]+B[0]))
                    type_4_list.append([infix_i, infix_o, prefix_i, prefix_o])
    type_4_selected = random.sample(type_4_list, min(len(type_4_list), NUM_EQ))
    for problem in type_4_selected:
        csv_writer.writerow(problem)

def type5():
    type_5_list = []
    for A in term_const:
        for B in term_const:
            for C in term_A_by_x:
                if A[0]-B[0]!=0:
                    infix_i = f"{A[2]}=({B[2]}+{C[2]})"
                    prefix_i = f"(= {A[1]} (+ {B[1]} {C[1]}))"
                    infix_o, prefix_o = outputs(reducefract(C[0], A[0]-B[0]))
                    type_5_list.append([infix_i, infix_o, prefix_i, prefix_o])
    type_5_selected = random.sample(type_5_list, min(len(type_5_list), NUM_EQ))
    for problem in type_5_selected:
        csv_writer.writerow(problem)

def type6():
    type_6_list = []
    for A in term_const:
        for B in term_const:
            for C in term_Ax:
                for D in term_const:
                    for E in term_const:
                        if C[0]!=0:
                            infix_i = f"({A[2]}+{B[2]})=(({C[2]}+{D[2]})+{E[2]})"
                            prefix_i = f"(= (+ {A[1]} {B[1]}) (+ (+ {C[1]} {D[1]}) {E[1]}))"
                            infix_o, prefix_o = outputs(reducefract((A[0]+B[0]) - (D[0]+E[0]), C[0]))
                            type_6_list.append([infix_i, infix_o, prefix_i, prefix_o])
    type_6_selected = random.sample(type_6_list, min(len(type_6_list), NUM_EQ))
    for problem in type_6_selected:
        csv_writer.writerow(problem)

def type7():
    type_7_list = []
    for A in term_Ax:
        for B in term_const:
            for C in term_const:
                for D in term_const:
                    if A[0]*D[0]!=0:
                        infix_i = f"({A[2]}/{B[2]})=({C[2]}/{D[2]})"
                        prefix_i = f"(= (/ {A[1]} {B[1]}) (/ {C[1]} {D[1]}))"
                        infix_o, prefix_o = outputs(reducefract(B[0]*C[0], A[0]*D[0]))
                        type_7_list.append([infix_i, infix_o, prefix_i, prefix_o])
    type_7_selected = random.sample(type_7_list, min(len(type_7_list), NUM_EQ))
    for problem in type_7_selected:
        csv_writer.writerow(problem)

def type8():
    type_8_list = []
    for A in term_const:
        for B in term_const:
            for C in term_const:
                if C[0]!=0:
                    infix_i = f"x=({A[2]}-{B[2]})/{C[2]}"
                    prefix_i = f"(= (x) (/ (- {A[1]} {B[1]}) {C[1]}))"
                    infix_o, prefix_o = outputs(reducefract(A[0]-B[0], C[0]))
                    type_8_list.append([infix_i, infix_o, prefix_i, prefix_o])
    type_8_selected = random.sample(type_8_list, min(len(type_8_list), NUM_EQ))
    for problem in type_8_selected:
        csv_writer.writerow(problem)

def type9():
    type_9_list = []
    for A in term_Ax:
        for B in term_const:
            for C in term_Ax:
                for D in term_const:
                    if A[0]+C[0]!=0:
                        infix_i = f"{A[2]}=(({B[2]}-{C[2]})+{D[2]})"
                        prefix_i = f"(= {A[1]} (+ (- {B[1]} {C[1]}) {D[1]}))"
                        infix_o, prefix_o = outputs(reducefract(B[0]+D[0], A[0]+C[0]))
                        type_9_list.append([infix_i, infix_o, prefix_i, prefix_o])
    type_9_selected = random.sample(type_9_list, min(len(type_9_list), NUM_EQ))
    for problem in type_9_selected:
        csv_writer.writerow(problem)

def type10():
    type_10_list = []
    for A in term_A_by_x:
        for B in term_const:
            if B[0]!=0:
                infix_i = f"{A[2]}*x={B[2]}"
                prefix_i = f"(= (* {A[1]} (x)) {B[1]})"
                infix_o, prefix_o = outputs(reducefract(A[0], B[0]))
                type_10_list.append([infix_i, infix_o, prefix_i, prefix_o])
    type_10_selected = random.sample(type_10_list, min(len(type_10_list), NUM_EQ))
    for problem in type_10_selected:
        csv_writer.writerow(problem)

def type11():
    type_11_list = []
    for A in term_Ax:
        for B in term_const:
            for C in term_const:
                if A[0]!=0:
                    infix_i = f"({A[2]}+{B[2]})={C[2]}"
                    prefix_i = f"(= (+ {A[1]} {B[1]}) {C[1]})"
                    infix_o, prefix_o = outputs(reducefract(C[0]-B[0], A[0]))
                    type_11_list.append([infix_i, infix_o, prefix_i, prefix_o])
    type_11_selected = random.sample(type_11_list, min(len(type_11_list), NUM_EQ))
    for problem in type_11_selected:
        csv_writer.writerow(problem)

type1()
type2()
type3()
type4()
type5()
type6()
type7()
type8()
type9()
type10()
type11()
data_file.close()