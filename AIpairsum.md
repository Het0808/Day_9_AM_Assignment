# ============================================================
#  interview_ready.py  —  Day 9 · AM  Part C (Interview Ready)
#  Q1: Shallow vs Deep Copy
#  Q2: List Rotation
#  Q3: Debug — Mutating a list while iterating
# ============================================================

import copy

# ════════════════════════════════════════════════════════════
#  Q1 — SHALLOW COPY vs DEEP COPY
# ════════════════════════════════════════════════════════════
"""
CONCEPTUAL ANSWER
─────────────────

A Python list stores references (pointers) to objects, not the
objects themselves.  When you copy a list you must decide how
deeply that copy should reach.

┌──────────────────────────────────────────────────────────┐
│  SHALLOW COPY  (copy.copy  /  lst[:]  /  list(lst))      │
│  • Creates a NEW outer list object                       │
│  • But the elements inside still point to the SAME       │
│    objects as the original                               │
│  • Problem: mutating a nested object affects BOTH lists  │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│  DEEP COPY    (copy.deepcopy)                            │
│  • Recursively creates NEW objects for every level       │
│  • Original and copy are 100 % independent               │
│  • Use whenever the list contains mutable nested objects │
└──────────────────────────────────────────────────────────┘
"""

def demo_shallow_vs_deep():
    print("=" * 56)
    print("  Q1  —  Shallow Copy vs Deep Copy")
    print("=" * 56)

    original = [["Alice", 88], ["Bob", 92], ["Carol", 79]]

    # ── Shallow copy ──────────────────────────────────────
    shallow = original[:]          # same as copy.copy(original)

    # The outer list is a new object → True
    print(f"\n  original is shallow  →  {original is shallow}")        # False ✓

    # But the inner lists share the SAME objects
    print(f"  original[0] is shallow[0]  →  {original[0] is shallow[0]}")  # True ← the trap

    # Mutating a nested object through the shallow copy …
    shallow[0][1] = 999            # change Alice's mark via shallow

    print(f"\n  After  shallow[0][1] = 999 :")
    print(f"    shallow   → {shallow}")
    print(f"    original  → {original}")   # Alice's mark changed here too! ←BUG

    # ── Deep copy ─────────────────────────────────────────
    original2 = [["Alice", 88], ["Bob", 92], ["Carol", 79]]
    deep      = copy.deepcopy(original2)

    print(f"\n  original2[0] is deep[0]  →  {original2[0] is deep[0]}")  # False ✓

    deep[0][1] = 999
    print(f"\n  After  deep[0][1] = 999 :")
    print(f"    deep       → {deep}")
    print(f"    original2  → {original2}")  # original2 is unchanged ✓

    print("""
  WHY SHALLOW COPY FAILS
  ─────────────────────
  Memory model (simplified):

    original ──►  [ ref0, ref1, ref2 ]
                     │
    shallow  ──►  [ ref0, ref1, ref2 ]
                     │
                     └──► ["Alice", 88]   ← same object!

  Both lists hold the same inner-list reference.
  Changing a value inside that inner list is visible
  through both the original and the shallow copy.

  WHEN DEEP COPY IS REQUIRED
  ──────────────────────────
  • Nested lists / dicts / sets inside your list
  • Any mutable object that must be truly independent
  • Creating "snapshots" of state (undo/redo, game state, etc.)
  • Passing data to a function that must not mutate the caller's data
""")


# ════════════════════════════════════════════════════════════
#  Q2 — LIST ROTATION
# ════════════════════════════════════════════════════════════

def rotate_list(lst: list, k: int) -> list:
    """
    Rotate lst to the right by k positions using slicing.

    rotate_list([1,2,3,4,5], 2)  →  [4,5,1,2,3]

    Slicing trick:
        [-k:]  grabs the last k elements  →  [4, 5]
        [:-k]  grabs everything before    →  [1, 2, 3]
        concatenating gives               →  [4, 5, 1, 2, 3]

    Edge cases handled:
        k > len(lst)  → k %= n  (full rotations are no-ops)
        k == 0        → returns original unchanged
        empty list    → returns []
    """
    n = len(lst)
    if n == 0 or k == 0:
        return lst[:]                  # return a copy, never mutate

    k %= n                             # normalise: k=7 on len-5 == k=2
    return lst[-k:] + lst[:-k]        # slicing: tail + head


def demo_rotate():
    print("=" * 56)
    print("  Q2  —  List Rotation")
    print("=" * 56)

    tests = [
        ([1, 2, 3, 4, 5], 2,  [4, 5, 1, 2, 3]),
        ([1, 2, 3, 4, 5], 0,  [1, 2, 3, 4, 5]),   # no rotation
        ([1, 2, 3, 4, 5], 5,  [1, 2, 3, 4, 5]),   # full rotation
        ([1, 2, 3, 4, 5], 7,  [4, 5, 1, 2, 3]),   # k > len
        ([42],            3,  [42]),               # single element
        ([],              2,  []),                 # empty list
    ]

    for lst, k, expected in tests:
        result = rotate_list(lst, k)
        status = "✅" if result == expected else "❌"
        print(f"\n  rotate_list({lst}, k={k})")
        print(f"    result   → {result}")
        print(f"    expected → {expected}  {status}")

    print("""
  HOW THE SLICING WORKS  (k=2, lst=[1,2,3,4,5])
  ──────────────────────────────────────────────
    lst[-2:]      →  [4, 5]      last k elements (the "tail")
    lst[:-2]      →  [1, 2, 3]   everything before (the "head")
    tail + head   →  [4, 5, 1, 2, 3]  ✓
""")


# ════════════════════════════════════════════════════════════
#  Q3 — DEBUG: Mutating a list while iterating over it
# ════════════════════════════════════════════════════════════

def demo_debug():
    print("=" * 56)
    print("  Q3  —  Debug: Mutating a List During Iteration")
    print("=" * 56)

    print("""
  BUGGY CODE
  ──────────
    nums = [1, 2, 3, 4, 5, 6, 7, 8]
    for num in nums:
        if num % 2 == 0:
            nums.remove(num)
    print(nums)   # expected [1,3,5,7] — got [1,3,5,7,8] or worse

  WHY THE BUG HAPPENS
  ────────────────────
  Python's for-loop uses an internal index counter starting at 0.
  When remove() deletes an element, every element after it shifts
  one position to the LEFT — but the counter keeps stepping RIGHT.
  The loop effectively "skips" the element that slid into the
  deleted slot.

  Step-by-step with [2, 4, 6, 8]:
    index=0  num=2  → remove 2  → list becomes [4, 6, 8]
    index=1  num=6  → remove 6  → list becomes [4, 8]
                                   (4 was skipped entirely!)
    index=2  → out of range, loop ends
  Result: [4, 8]  — completely wrong!

  CORRECT SOLUTIONS
  ─────────────────
  1. List comprehension (preferred — clean and Pythonic):
       nums = [n for n in nums if n % 2 != 0]

  2. Iterate over a copy, modify the original:
       for num in nums[:]:          # nums[:] is a shallow copy
           if num % 2 == 0:
               nums.remove(num)

  3. filter() builtin:
       nums = list(filter(lambda n: n % 2 != 0, nums))
""")

    # ── Reproduce the bug ──────────────────────────────────
    buggy = [2, 4, 6, 8]
    buggy_copy = buggy[:]
    for num in buggy_copy:
        if num % 2 == 0:
            buggy.remove(num)
    print(f"  Buggy result  on [2,4,6,8]  →  {buggy}")
    print(f"  Expected                    →  []")

    buggy2 = [1, 2, 3, 4, 5, 6, 7, 8]
    for num in list(buggy2):        # iterating original shows skip
        if num % 2 == 0:
            buggy2.remove(num)
    print(f"\n  Buggy result  on [1..8]    →  {buggy2}")
    print(f"  Expected                   →  [1, 3, 5, 7]")

    # ── Fix 1: list comprehension ──────────────────────────
    fixed1 = [1, 2, 3, 4, 5, 6, 7, 8]
    fixed1 = [n for n in fixed1 if n % 2 != 0]
    print(f"\n  Fix 1 (comprehension)       →  {fixed1}  ✅")

    # ── Fix 2: iterate over a copy ─────────────────────────
    fixed2 = [1, 2, 3, 4, 5, 6, 7, 8]
    for num in fixed2[:]:
        if num % 2 == 0:
            fixed2.remove(num)
    print(f"  Fix 2 (iterate copy)        →  {fixed2}  ✅")

    # ── Fix 3: filter ──────────────────────────────────────
    fixed3 = list(filter(lambda n: n % 2 != 0, [1,2,3,4,5,6,7,8]))
    print(f"  Fix 3 (filter)              →  {fixed3}  ✅\n")


# ════════════════════════════════════════════════════════════
#  ENTRY POINT
# ════════════════════════════════════════════════════════════

if __name__ == "__main__":
    demo_shallow_vs_deep()
    demo_rotate()
    demo_debug()
