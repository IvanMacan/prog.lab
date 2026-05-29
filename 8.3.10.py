import math

# ============================================================
# a) x_k = (-1)^k * x^(2k+1) / ((2k-1)! * (2k+1)!)  for k >= 1
# ============================================================
def compute_xk(x, k):
    """Compute the k-th element of the sequence."""
    numerator = ((-1) ** k) * (x ** (2 * k + 1))
    denominator = math.factorial(2 * k - 1) * math.factorial(2 * k + 1)
    return numerator / denominator

print("=" * 60)
print("a) Sequence elements x_k = (-1)^k * x^(2k+1) / ((2k-1)!(2k+1)!)")
print("=" * 60)
x_val = 2.0
for k in range(1, 6):
    print(f"  x_{k} (x={x_val}) = {compute_xk(x_val, k):.10f}")


# ============================================================
# b) S_n = 1 - 1/2 + 1/3 - ... + (-1)^(n-1) * 1/n
# ============================================================
def compute_Sn(n):
    """Compute the alternating harmonic series sum up to n terms."""
    total = 0.0
    for i in range(1, n + 1):
        total += ((-1) ** (i - 1)) / i
    return total

print("\n" + "=" * 60)
print("b) S_n = 1 - 1/2 + 1/3 - ... + (-1)^(n-1) * 1/n")
print("=" * 60)
for n in [5, 10, 100, 1000]:
    print(f"  S_{n:4d} = {compute_Sn(n):.10f}  (ln(2) = {math.log(2):.10f})")


# ============================================================
# c) Determinant of n×n tridiagonal matrix (2 on main diagonal,
#    1 on sub- and super-diagonals, 0 elsewhere)
# ============================================================
def build_tridiagonal(n):
    """Build an n×n tridiagonal matrix."""
    matrix = [[0.0] * n for _ in range(n)]
    for i in range(n):
        matrix[i][i] = 2.0
        if i > 0:
            matrix[i][i - 1] = 1.0
        if i < n - 1:
            matrix[i][i + 1] = 1.0
    return matrix

def determinant(matrix):
    """Compute determinant via Gaussian elimination."""
    n = len(matrix)
    mat = [row[:] for row in matrix]  # copy
    det = 1.0
    for col in range(n):
        # Find pivot
        pivot_row = None
        for row in range(col, n):
            if mat[row][col] != 0:
                pivot_row = row
                break
        if pivot_row is None:
            return 0.0
        if pivot_row != col:
            mat[col], mat[pivot_row] = mat[pivot_row], mat[col]
            det *= -1
        det *= mat[col][col]
        for row in range(col + 1, n):
            factor = mat[row][col] / mat[col][col]
            for j in range(col, n):
                mat[row][j] -= factor * mat[col][j]
    return det

print("\n" + "=" * 60)
print("c) Determinant of n×n tridiagonal matrix")
print("   (2 on diagonal, 1 on sub/super-diagonals)")
print("=" * 60)
for n in [2, 3, 4, 5, 6, 10]:
    mat = build_tridiagonal(n)
    det = determinant(mat)
    print(f"  det(A_{n}) = {det:.2f}")


# ============================================================
# d) Sum: Σ(k=1..n) (a_k / b_k)^k
#    a_0=1, a_1=2,  a_k = a_(k-2) + b_k/2       for k >= 2
#    b_0=5, b_1=5,  b_k = b_(k-2)^2 - a_(k-1)   for k >= 2
# ============================================================
def compute_sum_d(n):
    """Compute the sum Σ (a_k/b_k)^k for k=1..n."""
    # Build a and b arrays (index from 0)
    a = [0.0] * (n + 1)
    b = [0.0] * (n + 1)
    a[0], a[1] = 1.0, 2.0
    b[0], b[1] = 5.0, 5.0
    for k in range(2, n + 1):
        b[k] = b[k - 2] ** 2 - a[k - 1]
        a[k] = a[k - 2] + b[k] / 2

    total = 0.0
    for k in range(1, n + 1):
        if b[k] == 0:
            print(f"  Warning: b_{k} = 0, skipping term")
            continue
        total += (a[k] / b[k]) ** k
    return total

print("\n" + "=" * 60)
print("d) Σ(k=1..n) (a_k/b_k)^k  with given recurrences")
print("=" * 60)
for n in [3, 5, 7]:
    s = compute_sum_d(n)
    print(f"  Sum(n={n}) = {s:.10f}")


# ============================================================
# e) Taylor series for cos(x):  y = 1 - x²/2! + x⁴/4! - ...
#    until |term| < epsilon
# ============================================================
def cos_taylor(x, eps=1e-9):
    """Compute cos(x) via Taylor series with precision eps."""
    total = 0.0
    term = 1.0   # first term: x^0 / 0! = 1
    k = 0
    while abs(term) >= eps:
        total += term
        k += 1
        # Next term: multiply by -x²/((2k)(2k-1))
        term *= -x * x / ((2 * k) * (2 * k - 1))
    return total, k

print("\n" + "=" * 60)
print("e) Taylor series: cos(x) = 1 - x²/2! + x⁴/4! - ...")
print(f"   Precision ε = 1e-9")
print("=" * 60)
test_xs = [0.0, math.pi / 6, math.pi / 4, math.pi / 3,
           math.pi / 2, math.pi, 2 * math.pi]
labels  = ["0", "π/6", "π/4", "π/3", "π/2", "π", "2π"]

print(f"  {'x':>6}  {'Taylor':>18}  {'math.cos':>18}  {'|diff|':>12}  terms")
print("  " + "-" * 72)
for lbl, xv in zip(labels, test_xs):
    my_val, terms = cos_taylor(xv)
    lib_val = math.cos(xv)
    diff = abs(my_val - lib_val)
    print(f"  {lbl:>6}  {my_val:18.12f}  {lib_val:18.12f}  {diff:12.2e}  {terms}")

print("\nAll parts completed successfully.")
