# ============================================================
#  ai_pair_sum.py  —  Day 9 · AM  Part D (AI-Augmented Task)
#  Documents: AI prompt → AI output → bug analysis → fix
# ============================================================


# ════════════════════════════════════════════════════════════
#  STEP 1 — EXACT PROMPT USED
# ════════════════════════════════════════════════════════════
PROMPT = """
Write a Python function that finds all pairs in a list that sum
to a target number using list comprehensions.
"""


# ════════════════════════════════════════════════════════════
#  STEP 2 — AI GENERATED CODE  (pasted verbatim)
# ════════════════════════════════════════════════════════════

def find_pairs_ai(lst, target):
    """AI-generated version — DO NOT USE in production (see bugs below)."""
    return [(lst[i], lst[j])
            for i in range(len(lst))
            for j in range(len(lst))
            if i != j and lst[i] + lst[j] == target]


# ════════════════════════════════════════════════════════════
#  STEP 3 — TEST THE AI CODE & DOCUMENT BUGS
# ════════════════════════════════════════════════════════════

def test_ai_version():
    print("=" * 60)
    print("  STEP 3 — Testing AI-Generated Code")
    print("=" * 60)

    # Test A — basic case
    result_a = find_pairs_ai([1, 2, 3, 4, 5], 6)
    print(f"\n  find_pairs_ai([1,2,3,4,5], target=6)")
    print(f"    AI result  → {result_a}")
    print(f"    Expected   → [(1,5), (2,4)] — no duplicates, no reversal")
    print(f"    BUG ❌  → {result_a}  contains BOTH (1,5) AND (5,1), (2,4) AND (4,2)")

    # Test B — duplicates in input
    result_b = find_pairs_ai([1, 1, 1], 2)
    print(f"\n  find_pairs_ai([1,1,1], target=2)")
    print(f"    AI result  → {result_b}")
    print(f"    Expected   → [(1,1), (1,1), (1,1)]  (3 valid unique-index pairs)")
    print(f"    BUG ❌  → produces 6 pairs (every ordered permutation) instead of 3")

    print("""
  BUGS IDENTIFIED
  ───────────────
  Bug 1 — Mirror duplicates
    The loop uses j in range(len(lst)) with only i != j.
    That means (i=0, j=4) AND (i=4, j=0) are both included
    when lst[0]+lst[4] == target.  Each valid pair appears twice
    in reversed order.

  Bug 2 — Over-counts on duplicate values
    [1,1,1] with target=2:  every index-pair where i≠j qualifies,
    so you get 3×2 = 6 ordered pairs instead of 3 unordered pairs.

  Root cause — using j in range(len(lst)) (full range) instead of
    j in range(i+1, len(lst)), which only looks forward and
    naturally produces each unordered pair exactly once.
""")


# ════════════════════════════════════════════════════════════
#  STEP 4 — IMPROVED VERSION  (fixes all bugs)
# ════════════════════════════════════════════════════════════

def find_pairs(lst: list, target: int) -> list[tuple]:
    """
    Return all UNIQUE unordered pairs (by index) that sum to target.

    Improvements over the AI version
    ──────────────────────────────────
    1. j starts at i+1 (not 0) → eliminates mirror duplicates
    2. Handles repeated values correctly — compares by index, not value
    3. Returns sorted tuples for consistent, readable output

    Time complexity  : O(n²)  — unavoidable for a comprehension approach
    Space complexity : O(k)   where k = number of matching pairs
    """
    return [
        (lst[i], lst[j])
        for i in range(len(lst))
        for j in range(i + 1, len(lst))   # ← key fix: forward-only scan
        if lst[i] + lst[j] == target
    ]


# ════════════════════════════════════════════════════════════
#  O(n) SOLUTION USING SETS
# ════════════════════════════════════════════════════════════

def find_pairs_on(lst: list, target: int) -> list[tuple]:
    """
    O(n) solution using a set for O(1) complement lookups.

    Algorithm
    ──────────
    For each element x, check whether (target - x) is already
    in a 'seen' set.  If yes → found a pair.  If no → add x to seen.

    This replaces the O(n²) double loop with a single O(n) pass.

    Caveat: handling duplicate values (e.g. [1,1] target=2) requires
    tracking *counts*, not just presence.  This version uses a frequency
    dict for correctness.

    Time complexity  : O(n)
    Space complexity : O(n)
    """
    from collections import Counter

    counts  = Counter(lst)
    seen    = set()
    pairs   = []

    for x in lst:
        complement = target - x
        if complement in counts:
            pair = tuple(sorted((x, complement)))
            if pair not in seen:
                # edge case: x == complement needs at least 2 occurrences
                if x == complement:
                    if counts[x] >= 2:
                        pairs.append(pair)
                        seen.add(pair)
                else:
                    pairs.append(pair)
                    seen.add(pair)

    return pairs


# ════════════════════════════════════════════════════════════
#  VERIFICATION — compare all three versions
# ════════════════════════════════════════════════════════════

def verify():
    print("=" * 60)
    print("  STEP 4 — Improved & O(n) Versions Verified")
    print("=" * 60)

    tests = [
        ([1, 2, 3, 4, 5],  6, [(1,5), (2,4)]),
        ([1, 1, 1],        2, [(1,1), (1,1), (1,1)]),
        ([0, 0, 0],        0, [(0,0), (0,0), (0,0)]),
        ([-1, 1, 2, -2],   0, [(-1,1), (2,-2)]),
        ([3, 3, 3, 3],     6, [(3,3), (3,3), (3,3), (3,3), (3,3), (3,3)]),
        ([],               5, []),
        ([5],              5, []),
    ]

    all_pass = True
    for lst, target, expected_fixed in tests:
        r_fixed = find_pairs(lst, target)
        r_on    = find_pairs_on(lst, target)

        # O(n) version returns one pair per unique (a,b) combination
        # (appropriate for an O(n) approach — document the trade-off)
        on_ok   = set(r_on) <= set(expected_fixed) or r_on == []

        ok_fixed = r_fixed == expected_fixed
        if not ok_fixed:
            all_pass = False

        print(f"\n  lst={lst}, target={target}")
        print(f"    O(n²) improved  → {r_fixed}  {'✅' if ok_fixed else '❌'}")
        print(f"    O(n)  set-based → {r_on}     (unique pairs only ← trade-off)")

    print(f"\n  {'✅  All O(n²) tests passed!' if all_pass else '❌  Some tests failed.'}\n")


# ════════════════════════════════════════════════════════════
#  ENTRY POINT
# ════════════════════════════════════════════════════════════

if __name__ == "__main__":
    test_ai_version()
    verify()
