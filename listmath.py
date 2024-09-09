''' One dimensional list math '''
import math

def islist(lam):
    return isinstance(lam, list)
def samelen(alpha, beta):
    return len(alpha) == len(beta)

def unary_minus(lam):
    return [-l for l in lam]

def add(alpha, beta):
    return [a + b for a, b in zip(alpha, beta)]
def sub(alpha, beta):
    return [a - b for a, b in zip(alpha, beta)]
def mul(alpha, beta):
    return [a * b for a, b in zip(alpha, beta)]
def div(alpha, beta):
    return [a / b for a, b in zip(alpha, beta)]
def mod(alpha, h): 
    return [a % h for a in alpha]
def pow(alpha, beta):
    return [a ** b for a, b in zip(alpha, beta)]
def scale(alpha, h):
    return [a * h for a in alpha]

def sqrt(lam):
    return [math.sqrt(l) for l in lam]
def square(lam):
    return [l * l for l in lam]

def sin(lam): 
    return [math.sin(l) for l in lam]
def cos(lam): 
    return [math.cos(l) for l in lam]
def tan(lam):
    return [math.tan(l) for l in lam]
def atan2(alpha, beta):
    return [math.atan2(a, b) for a, b in zip(alpha, beta)]

def dot(alpha, beta):
    return sum(a * b for a, b in zip(alpha, beta))

def equal(alpha, beta):
    return [a == b for a, b in zip(alpha, beta)]
def close(alpha, beta, tolerance=1e-4):
    return [abs(a - b) < tolerance for a, b in zip(alpha, beta)]
