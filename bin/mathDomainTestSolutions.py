import dreamcoder.domains.mathDomain.mathDomainPrimitives as mdp

s = "(= (0) (+ (+ (- (0) (* (4) (x))) (* (2) (x))) (4)))"
s_1 = mdp._simplify(mdp._rrotate(mdp._add(mdp._rrotate(mdp._simplify(mdp._dist(mdp._rrotate(s, 3), 5),0), 2), 4), 8), 0)
#s_1 = mdp._simplify(mdp._rrotate(mdp._add(mdp._simplify(mdp._rrotate(mdp._rrotate(mdp._sub(mdp._swap(mdp._swap(s, 1), 8), 7), 1), 10), 0), 3), 1),0)

#s_1 = mdp._rrotate()

print(mdp._genSub(s_1))
print(s_1)