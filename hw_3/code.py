import numpy as np
import numbers
import copy


# Easy
class matrix:
    def __init__(self, value):
        self.value = value
        self.shape = len(value), len(value[0])  # в __init__ всегда передаём двумерный список
    
    def cbc_operation(self, mat, operation):  # component-by-component operation
        if self.shape != mat.shape:
            raise ValueError(f'Inappropriate dimensions: {self.shape} != {mat.shape}.')
        result = [[None] * self.shape[1] for _ in range(self.shape[0])]
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                result[i][j] = operation(self.value[i][j], mat.value[i][j])
        return matrix(result)
    
    def __add__(self, mat): return self.cbc_operation(mat, lambda x, y: x + y)
    
    def __mul__(self, mat): return self.cbc_operation(mat, lambda x, y: x * y)
    
    def __matmul__(self, mat):
        if self.shape[1] != mat.shape[0]:
            raise ValueError(f'Inappropriate dimensions {self.shape}, {mat.shape}: {self.shape[1]} != {mat.shape[0]}.')
        result = [[0] * mat.shape[1] for _ in range(self.shape[0])]
        for i in range(self.shape[0]):
            for j in range(mat.shape[1]):
                for s in range(self.shape[1]):
                    result[i][j] += self.value[i][s] * mat.value[s][j]
        return matrix(result)
    
    def __repr__(self): return repr(np.matrix(self.value))
    
    def __str__(self): return str(np.matrix(self.value))


# Hard
class HashMixin:
    mod = 5  # По этому модулю берём хеш (он маленький, чтобы было проще искать коллизии)
    hash_list = []
    for _ in range(mod):
        hash_list.append([None] * mod)

    # Обобщение полиномиального хеша для строк на матрицы
    # Почитать можно тут: https://habr.com/ru/post/142589/ (п. "Хеши в матрицах")
    # Можно реализовать без квадратной матрицы, но это не особо улучшит что-либо
    def __hash__(self):
        p, q = 1 << 32, 1 << 32
        pow1, pow2 = [1] * self.shape[0], [1] * self.shape[1]
        result = [[0] * self.shape[1] for _ in range(self.shape[0])]
        result[0][0] = self.value[0][0] % __class__.mod
        for i in range(1, self.shape[0]):
            pow1[i] = (pow1[i - 1] * p) % __class__.mod
            result[i][0] = (result[i - 1][0] + self.value[i][0] * pow1[i]) % __class__.mod
        for j in range(1, self.shape[1]):
            pow2[j] = (pow2[j - 1] * q) % __class__.mod
            result[0][j] = (result[0][j - 1] + self.value[0][j] * pow2[j]) % __class__.mod
        for i in range(1, self.shape[0]):
            for j in range(1, self.shape[1]):
                result[i][j] = (result[i - 1][j] + result[i][j - 1] - result[i - 1][j - 1] + self.value[i][j]) % __class__.mod
        return int(result[-1][-1])

class hashable_matrix(matrix, HashMixin):
    def __matmul__(self, mat):
        self_hash, mat_hash = hash(self), hash(mat)
        if __class__.hash_list[self_hash][mat_hash] is None:
            __class__.hash_list[self_hash][mat_hash] = super().__matmul__(mat)
        else:
            print('The hashed value of the matrix multiplication was returned')
        return __class__.hash_list[self_hash][mat_hash]


# Medium
class OperationsMixin(np.lib.mixins.NDArrayOperatorsMixin):
    _HANDLED_TYPES = (np.ndarray, numbers.Number)
    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        out = kwargs.get('out', ())
        for x in inputs + out:
            if not isinstance(x, self._HANDLED_TYPES + (ArrayLike,)):
                return NotImplemented
        inputs = tuple(x.value if isinstance(x, ArrayLike) else x for x in inputs)
        if out:
            kwargs['out'] = tuple(x.value if isinstance(x, ArrayLike) else x for x in out)
        result = getattr(ufunc, method)(*inputs, **kwargs)
        if type(result) is tuple:
            return tuple(type(self)(x) for x in result)
        elif method == 'at':
            return None
        else:
            return type(self)(result)

class StrMixin:
    def __str__(self): return str(self.value)

class ReprMixin:
    def __repr__(self): return '%s(%s)' % (type(self).__name__, self.value)

class WriteMixin:
    def write(self, filename):
        with open(filename, 'w') as f:
            f.write(str(self))

class ValueMixin:
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, x):
        self._value = np.asarray(x)

class ArrayLike(OperationsMixin, ReprMixin, StrMixin, ValueMixin, WriteMixin):
    def __init__(self, value):
        self.value = value




# Генерация артефактов для задачи Easy
np.random.seed(0)
a = matrix(np.random.randint(0, 10, (10, 10)))
b = matrix(np.random.randint(0, 10, (10, 10)))
add = a + b
mul = a * b
matmul = a @ b
for oper, value in [('+', add), ('*', mul), ('@', matmul)]:
    filename = 'matrix' + oper + '.txt'
    with open(filename, 'w') as f:
        f.write(str(value))

# Генерация артефактов для задачи Medium
np.random.seed(0)
a = ArrayLike(np.random.randint(0, 10, (10, 10)))
b = ArrayLike(np.random.randint(0, 10, (10, 10)))
add = a + b
mul = a * b
matmul = a @ b
for oper, value in [('+_', add), ('*_', mul), ('@_', matmul)]:
    value.write('matrix' + oper + '.txt')

# Генерация артефактов для задачи Hard
np.random.seed(0)
hash_A = None
while hash_A is None or hash_A != hash_C:
    A = hashable_matrix(np.random.randint(0, 10, (3, 3)))
    C = hashable_matrix(np.random.randint(0, 10, (3, 3)))
    hash_A, hash_C = hash(A), hash(C)
B = hashable_matrix(np.random.randint(0, 10, (3, 3)))
D = copy.copy(B)
A, B, C, D = [np.array(matr.value) for matr in [A, B, C, D]]
AB = A @ B
CD = C @ D
h = hash(hashable_matrix(AB)), hash(hashable_matrix(CD))
for name, var in [('A', A), ('B', B), ('C', C), ('D', D), ('AB', AB), ('CD', CD), ('hash', h)]:
    with open(name + '.txt', 'w') as f:
        f.write(str(var))
