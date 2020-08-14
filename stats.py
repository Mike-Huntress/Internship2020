#commonly used stat functions

def standardize(value, count):
    return value[:count].std()

def z_score_calc(x, u, sd):
    
    return (x-u)/sd