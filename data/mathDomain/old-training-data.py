
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