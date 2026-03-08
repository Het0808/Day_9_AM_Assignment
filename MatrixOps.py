# ============================================================
#  matrix_ops.py  —  Day 9 · AM  Part B (Stretch)
#  Matrix operations using nested lists & list comprehensions
# ============================================================


# ── HELPERS ──────────────────────────────────────────────────

def _dims(matrix: list) -> tuple[int, int]:
    """Return (rows, cols) for a 2-D list."""
    return len(matrix), len(matrix[0]) if matrix else 0


def _print_matrix(matrix: list, label: str = "") -> None:
    """Pretty-print a matrix with an optional label."""
    if label:
        print(f"  {label}:")
    col_w = max(len(str(cell)) for row in matrix for cell in row) + 1
    for row in matrix:
        print("  [" + "  ".join(f"{v:>{col_w}}" for v in row) + "  ]")
    print()


# ── 1. MATRIX ADDITION ───────────────────────────────────────

def matrix_add(A: list, B: list) -> list:
    """
    Return element-wise sum of two matrices.
    Raises ValueError if dimensions don't match.
    """
    rows_a, cols_a = _dims(A)
    rows_b, cols_b = _dims(B)

    if rows_a != rows_b or cols_a != cols_b:
        raise ValueError(
            f"Dimension mismatch: ({rows_a}×{cols_a}) + ({rows_b}×{cols_b})"
        )

    # Nested list comprehension: iterate rows then columns
    return [
        [A[i][j] + B[i][j] for j in range(cols_a)]
        for i in range(rows_a)
    ]


# ── 2. MATRIX TRANSPOSE ──────────────────────────────────────

def matrix_transpose(matrix: list) -> list:
    """
    Return the transpose of a matrix.
    Uses zip(*matrix) unpacking inside a nested comprehension.
    """
    # zip(*matrix) groups columns → becomes new rows
    return [list(row) for row in zip(*matrix)]


# ── 3. MATRIX MULTIPLICATION ─────────────────────────────────

def matrix_multiply(A: list, B: list) -> list:
    """
    Return the matrix product A × B using dot-product logic.
    Raises ValueError if inner dimensions don't match (cols_A ≠ rows_B).
    """
    rows_a, cols_a = _dims(A)
    rows_b, cols_b = _dims(B)

    if cols_a != rows_b:
        raise ValueError(
            f"Dimension mismatch: ({rows_a}×{cols_a}) × ({rows_b}×{cols_b}) — "
            f"cols of A ({cols_a}) must equal rows of B ({rows_b})"
        )

    # zip(*B) transposes B so we can iterate over its columns easily
    return [
        [sum(a * b for a, b in zip(row_a, col_b)) for col_b in zip(*B)]
        for row_a in A
    ]


# ── TEST SUITE ────────────────────────────────────────────────

def run_tests() -> None:
    sep = "─" * 50

    # ── Test set 1: 2×2 matrices ────────────────────────────
    print("\n" + "═"*50)
    print("  TEST SET 1 — 2×2 Matrices")
    print("═"*50)

    a = [[1, 2], [3, 4]]
    b = [[5, 6], [7, 8]]

    _print_matrix(a, "Matrix A")
    _print_matrix(b, "Matrix B")

    result_add = matrix_add(a, b)
    print(f"  {sep}")
    print("  matrix_add(A, B)  →  expected [[6,8],[10,12]]")
    _print_matrix(result_add, "Result")
    assert result_add == [[6, 8], [10, 12]], "❌ Addition failed"
    print("  ✅  Addition correct\n")

    result_T = matrix_transpose(a)
    print("  matrix_transpose(A)  →  expected [[1,3],[2,4]]")
    _print_matrix(result_T, "Result")
    assert result_T == [[1, 3], [2, 4]], "❌ Transpose failed"
    print("  ✅  Transpose correct\n")

    result_mul = matrix_multiply(a, b)
    print("  matrix_multiply(A, B)  →  expected [[19,22],[43,50]]")
    _print_matrix(result_mul, "Result")
    assert result_mul == [[19, 22], [43, 50]], "❌ Multiplication failed"
    print("  ✅  Multiplication correct\n")

    # ── Test set 2: 3×3 matrices ────────────────────────────
    print("═"*50)
    print("  TEST SET 2 — 3×3 Matrices")
    print("═"*50)

    c = [[1, 2, 3],
         [4, 5, 6],
         [7, 8, 9]]

    d = [[9, 8, 7],
         [6, 5, 4],
         [3, 2, 1]]

    _print_matrix(c, "Matrix C")
    _print_matrix(d, "Matrix D")

    result_add2 = matrix_add(c, d)
    print("  matrix_add(C, D)  →  all rows should sum to 10")
    _print_matrix(result_add2, "Result")
    assert result_add2 == [[10,10,10],[10,10,10],[10,10,10]], "❌ 3×3 Addition failed"
    print("  ✅  Addition correct\n")

    result_T2 = matrix_transpose(c)
    print("  matrix_transpose(C)  →  columns become rows")
    _print_matrix(result_T2, "Result")
    assert result_T2 == [[1,4,7],[2,5,8],[3,6,9]], "❌ 3×3 Transpose failed"
    print("  ✅  Transpose correct\n")

    result_mul2 = matrix_multiply(c, d)
    print("  matrix_multiply(C, D)")
    _print_matrix(result_mul2, "Result")
    expected_cd = [[30, 24, 18], [84, 69, 54], [138, 114, 90]]
    assert result_mul2 == expected_cd, "❌ 3×3 Multiplication failed"
    print("  ✅  Multiplication correct\n")

    # ── Test set 3: Non-square (2×3) × (3×2) ────────────────
    print("═"*50)
    print("  TEST SET 3 — Non-square  (2×3) × (3×2)")
    print("═"*50)

    e = [[1, 2, 3],
         [4, 5, 6]]           # 2 rows × 3 cols

    f = [[7,  8],
         [9,  10],
         [11, 12]]             # 3 rows × 2 cols

    _print_matrix(e, "Matrix E  (2×3)")
    _print_matrix(f, "Matrix F  (3×2)")

    result_mul3 = matrix_multiply(e, f)   # result should be 2×2
    print("  matrix_multiply(E, F)  →  2×2 result")
    _print_matrix(result_mul3, "Result")
    assert result_mul3 == [[58, 64], [139, 154]], "❌ Non-square multiplication failed"
    print("  ✅  Non-square multiplication correct\n")

    # ── Test set 4: Dimension mismatch error handling ────────
    print("═"*50)
    print("  TEST SET 4 — Graceful Error Handling")
    print("═"*50)

    print("  Attempting matrix_add(2×2, 3×3)  →  should raise ValueError")
    try:
        matrix_add([[1, 2], [3, 4]], [[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    except ValueError as e:
        print(f"  ✅  Caught: {e}\n")

    print("  Attempting matrix_multiply(2×2, 3×2)  →  should raise ValueError")
    try:
        matrix_multiply([[1, 2], [3, 4]], [[1, 2], [3, 4], [5, 6]])
    except ValueError as e:
        print(f"  ✅  Caught: {e}\n")

    print("═"*50)
    print("  🎉  All tests passed!")
    print("═"*50 + "\n")


# ── ENTRY POINT ───────────────────────────────────────────────

if __name__ == "__main__":
    run_tests()
