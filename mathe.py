import math
import numpy as np


np.set_printoptions(precision=18, linewidth=200)


cnames = ["Price", "Style", "Reliability"]
ctypes = ["Min", "Max", "Max"]

# temporary criteria weights for testing
temp_ci = [
    [1, 7, 1],
    [1/7, 1, 2],
    [1, 0.5, 1]
]

anames = ["Ford", "Toyota", "Renault"]

# raw criteria values as if entered by a user
rawm = [
    [20000, 5, 5],
    [25000, 7, 9],
    [21000, 6, 8]
]


def eigen(matrix):
    """
    Returns the eigenvector.
    Returns 1-dimensional array with size equal to the count of rows.
    """

    row_count = len(matrix)
    # result = [1 for i in range(row_count)]
    result = np.ones(row_count)
    total = 0
    for i in range(row_count):
        for j in range(row_count):
            result[i] *= matrix[i][j]
        result[i] = math.pow(result[i], 1/row_count)
        total += result[i]
    # normalizing
    for i in range(row_count):
        result[i] /= total
    return result


# TODO implement methods normalize_to_one and nomralize_with_l2
# after finding a way to test them, they are currently unused
# in the previous megamatrix codebase

# TODO multyply_matrix (dot product) and transpose are built into the
# the np array

def normalize_with_linear_transformation(imatrix, ctypes):
    # remove this once non-numpy arrays are no longer being used
    matrix = np.array(imatrix, np.float64)

    # replaced the bulky dimension checks with checking for a 0 in the shape tuple
    if 0 in matrix.shape:
        return

    maxvec = matrix.max(axis=0)

    for i in range(len(imatrix)):
        if ctypes[i] == "Min":
            for j in range(len(imatrix)):
                matrix[j][i] *= -1

    return matrix / maxvec


def weight(matrix, weights):

    alternatives_count = len(matrix)
    criteria_count = len(matrix[0])

    result = [0 for i in range(alternatives_count)]
    for i in range(alternatives_count):
        for j in range(criteria_count):
            result[i] += matrix[i][j] * weights[j]
    return result


def wsmdemo():
    importance = eigen(temp_ci)
    normalized = normalize_with_linear_transformation(rawm)
    sums = np.dot(normalized, importance)
    print(sums)


# te = buildMM()
# ahp(te)
'''
for c in criteria_names:
    print(c)
    print()
    print(te[c])
    print()
'''


# ahpreal()
# print(eigen(temp_ci))

# print(normalize_with_linear_transformation(rawm))
print()
# print(_normalize(rawm))
print()
# print(eigen(temp_ci))
print()
# ahpreal()


# functions used for topsys
# lim
def _idealize(matrix, ctypes):
    result_i = []
    result_ai = []
    mn = matrix.min(0)
    mx = matrix.max(0)
    for k, ctype in enumerate(lim):
        if ctype == "Min":
            result_i.append(mn[k])
            result_ai.append(mx[k])
        elif ctype == "Max":
            result_i.append(mx[k])
            result_ai.append(mn[k])
    return (result_i, result_ai)


# currently using the criteria weights being used in ahp, temp_ci for topsis testing

###################################

def _normalize(matrix):
    return np.array(matrix) / np.sqrt(np.sum(np.square(np.transpose(matrix)), axis=1))


'''
matrix
--------
root ( sum( transposed^2 ) )
'''


def _distantize(matrix, vector):
    return np.sqrt(np.power(matrix - vector, 2).sum(1))


'''
root ( ((matrix-vector)^2).sumOfAxis1 //horizontal )
'''


def _weighten(matrix, vector):
    return matrix*vector


def _idealize(matrix, lim):
    result_i = []
    result_ai = []
    mn = matrix.min(0)
    mx = matrix.max(0)
    for k, v in enumerate(lim):
        if v < 0:
            result_i.append(mn[k])
            result_ai.append(mx[k])
        elif v > 0:
            result_i.append(mx[k])
            result_ai.append(mn[k])
    return (result_i, result_ai)


def topsis(crit_alt_matrix, crit_weight , crit_lim  ):
    # calc
    normalized = _normalize(crit_alt_matrix)
    weightened = _weighten(normalized, crit_weight)
    ideal, anti_ideal = _idealize(weightened, crit_lim)
    dist_ideal = _distantize(weightened, ideal)
    dist_anti_ideal = _distantize(weightened, anti_ideal)

    result = dist_anti_ideal / (dist_ideal + dist_anti_ideal)

    print("Result")
    print()
    print(result)
    print()
    print()

    result_mn = (dist_anti_ideal / (dist_ideal + dist_anti_ideal)).min()
    result_mx = (dist_anti_ideal / (dist_ideal + dist_anti_ideal)).max()

    print("Result min")
    print(result_mn)
    print()
    print("Result max")
    print(result_mx)
    print()
    print()



def topsis_test_input():
    crit_name = ["Style", "Reliability", "Economy", "Price"]
    crit_weight = [
        0.1,  # Style
        0.4,  # Reliability
        0.4,  # Economy
        0.2  # Price
    ]
    crit_lim = [
        1,  # Style
        1,  # Reliability
        1,  # Economy
        -1  # Price
    ]
    alt_name = ["Honda", "Saturn", "Ford", "Mazda"]
    crit_alt_matrix = [
        # S  R  E  P
        [7, 9, 9, 8],  # Honda
        [8, 7, 8, 7],  # Saturn
        [9, 6, 8, 9],  # Ford
        [6, 7, 8, 6]   # Mazda
    ]

    topsis(crit_alt_matrix, crit_weight, crit_lim)


# topsis()

def wsm(criteria_importance, raw_alternative_data, ctypes):
    importance = eigen(criteria_importance)
    normalized = normalize_with_linear_transformation(raw_alternative_data, ctypes)
    sums = np.dot(normalized, importance)
    print(sums)

# Function to create megamatrix for ahp
def createMegaMatrix(criteria_names, raw_alternative_data):
    mm = {}
    for ci, criteria_names in enumerate(criteria_names):
        mm_component = []
        for i in range(len(raw_alternative_data)):
            component_row = []
            for j in range(len(raw_alternative_data)):
                component_row.append( raw_alternative_data[i][ci]/raw_alternative_data[j][ci] )

            mm_component.append(component_row)

        mm[criteria_names] = mm_component

    return mm

def ahp():
    criteria_names = ["Expenses", "Operability", "Reliability", "Flexibility"]
    criteria_importance = [
        # E  #O   #R  #F
        [1, 1/3, 5,  1],  # Expenses
        [3, 1,   5,  1],  # Operability
        [1/5, 1/5, 1, 1/5],  # Reliability
        [1, 1, 5, 1]  # Flexibility
    ]

    _importance = eigen(criteria_importance)
    
    # Random raw data to simulate the megamatrix creation
    raw_alternative_data = [
        [1000, 200, 5, 10],
        [500, 700, 15, 20],
        [750, 250, 9, 17]
    ]

    # Matrices comparing each ALL alternatives by ONE criterion
    
    megamatrix = {}
    megamatrix["Expenses"] = [
        [1, 5, 9],
        [1/5, 1, 3],
        [1/9, 1/3, 1]
    ]

    megamatrix["Operability"] = [
        [1, 1, 5],
        [1, 1, 3],
        [1/5, 1/3, 1]
    ]
    megamatrix["Reliability"] = [
        [1, 1/3, 1/9],
        [3, 1, 1/3],
        [9, 3, 1]
    ]
    megamatrix["Flexibility"] = [
        [1, 1/9, 1/5],
        [9, 1, 2],
        [5, 1/2, 1]
    ]
    
    #megamatrix = createMegaMatrix(criteria_names, raw_alternative_data);


    _eigen_alt_data = []


    for cname in criteria_names:
        temp = eigen(megamatrix[cname])
        _eigen_alt_data.append(temp)

    _eigen_alt_data = np.array(_eigen_alt_data).transpose()
    
    #for row in _eigen_alt_data:
    #    print(row)

    weighted = np.dot(_eigen_alt_data, _importance)
    print(weighted)
    
    #print() used to compare whether wsm and ahp find the correct sorting order with random data
    #wsm(criteria_importance, raw_alternative_data, ["Min", "Max", "Max", "Max"])

## UNCOMMENT NEXT TO TEST RAW INPUT

#ahp()
topsis_test_input()
#wsmdemo()