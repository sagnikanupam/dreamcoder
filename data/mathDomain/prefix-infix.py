import wolframalpha
import wolframAppID
import pandas as pd

EQ_FILE_ADDRESS = "cognitiveTutorDataset.txt" #change to location of prefix linear equations dataset

class Tree:

  def __init__(self, root, left="None", right="None") -> None:
    #Initialization of tree with root value and left and right subtrees
    self.root = root
    self.left = left
    self.right = right

  def __eq__(self, __o: object) -> bool:
    #Enables equality comparison of trees
    return isinstance(
      __o, Tree
    ) and self.root == __o.root and self.left == __o.left and self.right == __o.right

  def __repr__(self) -> str:
    #String representation of the tree
    return "(" + str(self.root) + " " + str(self.left) + " " + str(
      self.right) + ")"

  def __typerepr__(self) -> str:
    #Shows the types present in the tree, mostly concerned with str/int working, hence the [-6:-1] index range
    leftType = str(type(self.left))
    rightType = str(type(self.right))
    if (leftType == "<class '__main__.Tree'>"):
      leftType = self.left.__typerepr__()
    if (rightType == "<class '__main__.Tree'>"):
      rightType = self.right.__typerepr__()
    return "(" + str(type(
      self.root))[-6:-1] + " " + leftType + " " + rightType + ")"


def isNum(x):
  return (isinstance(x, int) or isinstance(x, float))


def intConvertable(s):
  try:
    int(s)
    return True
  except ValueError:
    return False


def floatConvertable(s):
  try:
    float(s)
    return True
  except ValueError:
    return False


def detreefy(tree):
  #converts tree into prefix equation string
  if tree == "None":
    return ""
  left = detreefy(tree.left)
  right = detreefy(tree.right)
  if left != "":
    left = " " + str(left)
  if right != "":
    right = " " + str(right)
  return "(" + str(tree.root) + str(left) + str(right) + ")"


def matchBracket(string, ind):
  #finds corresponding matching bracket of the bracket in prefix notation
  if string[ind] == "(":
    brCount = 1
    for i in range(ind + 1, len(string)):
      if (string[i] == "("):
        brCount += 1
      if (string[i] == ")"):
        brCount -= 1
      if brCount == 0:
        return i
  elif string[ind] == ")":
    brCount = 1
    for i in range(ind - 1, 0, -1):
      if (string[i] == "("):
        brCount -= 1
      if (string[i] == ")"):
        brCount += 1
      if brCount == 0:
        return i
  return "Error"


def treefy(eq):
  #converts prefix equation string to tree
  #operations must be in ops or "="
  #numbers must be int or floats
  #no space between brackets and operations succeeding them
  #(+ (- (x) (3)) (y))
  if eq == "None":
    return "None"
  newEq = eq[1:-1]
  fstArgInd = newEq.find("(")
  sndArgInd = newEq.rfind(")")
  fstArgMatch = "None"
  sndArgMatch = "None"
  args = [newEq.split(" ")[0]]
  if fstArgInd != -1:
    fstArgMatch = matchBracket(newEq, fstArgInd)
  if sndArgInd != -1:
    sndArgMatch = matchBracket(newEq, sndArgInd)
  if (fstArgInd != -1 and sndArgInd != -1):
    if (fstArgInd != sndArgMatch):
      args.append(newEq[fstArgInd:fstArgMatch + 1])
      args.append(newEq[sndArgMatch:sndArgInd + 1])
    else:
      args.append(newEq[fstArgInd:fstArgMatch + 1])
  if (intConvertable(args[0])):
    args[0] = int(args[0])
  elif (floatConvertable(args[0])):
    args[0] = float(args[0])
  while len(args) < 3:
    args.append("None")
  return Tree(args[0], treefy(args[1]), treefy(args[2]))

class infix_to_prefix:
    '''
    Converts ConPoLe Equations in infix notation to a prefix notation for parsing by DreamSolver's system.
    '''
    precedence={'^':5,'*':4,'/':4,'+':3,'-':3,'(':2,')':1, ' ^':5,' *':4, ' /':4,' +':3,' -':3,' (':2,' )':1}
    
    def __init__(self):
        self.items=[]
        self.size=-1
    
    def push(self,value):
        self.items.append(value)
        self.size+=1
    
    def pop(self):
        if self.isempty():
            return 0
        else:
            self.size-=1
            return self.items.pop()
    
    def isempty(self):
        if(self.size==-1):
            return True
        else:
            return False
    
    def seek(self):
        if self.isempty():
            return False
        else:
            return self.items[self.size]
    
    def is0perand(self,i):
        if i.isalpha() or i in '1234567890':
            return True
        else:
            return False
    
    def reverse(self,expr):
        rev=""
        for i in expr:
            if i == '(':
                i=')'
            elif i == ')':
                i='('
            rev=i+rev
        return rev
    
    def infixtoprefix (self,expr):
        prefix=""
        for ind in range(len(expr)):
            i = expr[ind]
            if self.is0perand(i):
                if ind<len(expr)-1 and expr[ind+1]=='-':
                    prefix += ' )'+i+'-('
                else:
                    prefix += ' )'+i+'('
            elif(i in '+*/^'):
                while(len(self.items)and self.precedence[i] < self.precedence[self.seek()]):
                    prefix+=self.pop()
                self.push(" "+i)
            elif(i == '-'):
                if ind>0 and expr[ind-1]==' ' and ind<len(expr)-1 and expr[ind+1]==' ':
                    while(len(self.items)and self.precedence[i] < self.precedence[self.seek()]):
                        prefix+=self.pop()
                    self.push(" "+i)
            elif i == ')':
                self.push(i)
            elif i == '(':
                o = self.pop()
                while o!=')' and o!=0:
                    prefix += o
                    o = self.pop()
            #end of for
        while len(self.items):
            if(self.seek()=='('):
                self.pop()
            else:
                prefix+=self.pop()
                #print(prefix)
        return prefix

def numberOfArgs(s):
    """
    Computes the number of times the brackets are perfectly matched (i.e. number of `(` = number of `)` ) to count the number of arguments in that string.
    """
    numOpenBrPair = 0
    numMatched = 0
    for i in s:
        if i=="(":
            numOpenBrPair+=1
        elif i==")":
            numOpenBrPair-=1
            if numOpenBrPair==0:
                numMatched+=1
    return numMatched


def bracketize(s):
    '''
    Ensure that the brackets of the generated prefix notation match the format expected by the treefy() function.
    '''
    if len(s) <= 0 or s[0] not in "+-*/^":
        return s
    elif s[0] == "-" and s[1] != " ":
        #print(s)
        return s
    else:
        nextOpInd = max(s.rfind("+ "), s.rfind("- "), s.rfind("* "), s.rfind("/ "), s.rfind("^ ")) 
        ind2 = None
        if nextOpInd==0:
            return "(" + s[0] + " " + s[2:] + ")"
        elif nextOpInd==2 or numberOfArgs(s[nextOpInd:])!=2:
            ind2 = s.rfind("(") 
        else:
            ind2 = nextOpInd
        ind1 = 2
        s1 = s[ind1:ind2]
        s2 = s[ind2:len(s)]
        #print("The split is: ")
        #print(s)
        #print(s1)
        #print(s2)
        return "(" + s[0] + " " + bracketize(s1) + " " + bracketize(s2) + ")"

def infix_to_prefix_conversion(equation):
    """
    Accepts equation string as input, generates a prefix string as output.
    """
    subtree = equation.split('=')
    subtree_rev = [sub[::-1] for sub in subtree]

    obj1 = infix_to_prefix()
    result1 = obj1.infixtoprefix(subtree_rev[0])
    obj2 = infix_to_prefix() 
    result2 = obj2.infixtoprefix(subtree_rev[1])

    if (result1!=False and result2!=False):
        result = '(= ' + bracketize(result1[::-1]) + ' ' + bracketize(result2[::-1]) + ')'  
        result = result.replace("( (", "((")
        result = result.replace(") )", "))") 
        result = result.replace("  ", " ")
        return result
    else:
        return None

if __name__ == "__main__":
            
    df = pd.DataFrame({'Infix_Eq': [], 'Prefix_Eg': [], 'Working': [], 'Infix_Sol': [], 'Prefix_Sol': []})
    
    with open(EQ_FILE_ADDRESS) as equationsFile:
        
        eq_num = 0

        for equation in equationsFile:
            
            appID = wolframAppID.appID() #This function returns the Wolfram Alpha App ID
            client = wolframalpha.Client(appID)
            response = client.query("Solve for x: "+equation)
            solution = list(response.results)[-1].text #Last item of generator response

            for i in '1234567890':
                equation = equation.replace(i+'x', i+' * x')

            prefix_eq = infix_to_prefix_conversion(equation)

            if prefix_eq!=None:
                #print("is",result)
                prefix_sol = None
                if solution is not None and solution!="(no solutions exist)":
                    prefix_sol = infix_to_prefix_conversion(solution)
                df.loc[len(df.index)] = [equation, prefix_eq, detreefy(treefy(prefix_eq))==prefix_eq, solution, prefix_sol]
                eq_num+=1
            print("Equation " + str(eq_num) + "......DONE ")
    df.to_csv('conpoleDatasetPrefix.csv')
    #Manually remove all equations with no solutions and fix the equations with Working column set to FALSE