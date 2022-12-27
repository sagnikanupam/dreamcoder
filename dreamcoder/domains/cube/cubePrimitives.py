import binutil  # required to import from dreamcoder modules

from dreamcoder.grammar import Grammar
from dreamcoder.program import Primitive
from dreamcoder.type import arrow, tint, tstr

# Configuration_faces : Up|Front|Right|Back|Left|Down
# Up 123 -> Back 321, Up 369 -> Right 321, Up 789 -> Front 123, Up 147 -> Left 123

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

def cubePrimitives():
    return [
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