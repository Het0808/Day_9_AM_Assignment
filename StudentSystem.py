# ============================================================
#  Student Management System — Day 9 · AM  (Lists Deep Dive)
#  Demonstrates: append, sorted(key=), list comprehensions,
#                slicing, pop, file read/write
# ============================================================

import os

# ── 1. INITIAL DATA ──────────────────────────────────────────
# Each record: [name, subject, marks]
records = [
    ["Aman",    "Math",    88],
    ["Priya",   "Physics", 91],
    ["Rahul",   "Math",    76],
    ["Sneha",   "Chemistry", 85],
    ["Vikram",  "Physics", 78],
    ["Divya",   "Math",    93],
    ["Karan",   "Chemistry", 70],
    ["Meera",   "Physics", 88],
    ["Arjun",   "Chemistry", 95],
    ["Nisha",   "Math",    82],
]

FILE_PATH = "students.txt"


# ── 2. FUNCTIONS ──────────────────────────────────────────────

def add_student(name: str, subject: str, marks: int) -> None:
    """Append a new record; reject duplicate name+subject combos."""
    # Check for duplicate using list comprehension
    duplicates = [r for r in records if r[0].lower() == name.lower()
                                     and r[1].lower() == subject.lower()]
    if duplicates:
        print(f"  ⚠️  '{name}' already has a record for {subject}.")
        return
    records.append([name, subject, marks])   # ← append demonstrated
    print(f"  ✅  Added: {name} | {subject} | {marks}")


def get_toppers(subject: str) -> list:
    """Return the top-3 students for a subject, sorted by marks (desc)."""
    subject_records = [r for r in records if r[1].lower() == subject.lower()]
    if not subject_records:
        print(f"  ⚠️  No records found for subject '{subject}'.")
        return []
    sorted_records = sorted(subject_records, key=lambda x: x[2], reverse=True)
    return sorted_records[:3]   # ← slicing demonstrated


def class_average(subject: str) -> float | None:
    """Return average marks for a subject using list comprehension."""
    marks_list = [m[2] for m in records if m[1].lower() == subject.lower()]  # ← comprehension
    if not marks_list:
        print(f"  ⚠️  No records found for subject '{subject}'.")
        return None
    return sum(marks_list) / len(marks_list)


def above_average_students() -> list:
    """Return students whose marks exceed the overall class average."""
    if not records:
        return []
    all_marks = [r[2] for r in records]          # ← comprehension
    overall_avg = sum(all_marks) / len(all_marks)
    # Nested logic inside comprehension
    above = [r for r in records if r[2] > overall_avg]
    return above, round(overall_avg, 2)


def remove_student(name: str) -> None:
    """Remove ALL records for a student without using remove() in a loop."""
    before = len(records)
    # Rebuild list via comprehension — no remove() inside a loop ✓
    new_records = [r for r in records if r[0].lower() != name.lower()]
    removed = before - len(new_records)

    if removed == 0:
        print(f"  ⚠️  No records found for '{name}'.")
        return

    # Demonstrate pop(): drain the old list, then refill
    while records:
        records.pop()               # ← pop demonstrated
    records.extend(new_records)     # restore filtered data

    print(f"  🗑️   Removed {removed} record(s) for '{name}'.")


# ── 3. FILE I/O ───────────────────────────────────────────────

def save_to_file() -> None:
    """Write all records to students.txt on exit."""
    with open(FILE_PATH, "w") as f:
        f.write("Name,Subject,Marks\n")
        for r in records:
            f.write(f"{r[0]},{r[1]},{r[2]}\n")
    print(f"\n  💾  Records saved to '{FILE_PATH}'.")


def load_from_file() -> None:
    """Load records from students.txt if it exists (file read demonstrated)."""
    if not os.path.exists(FILE_PATH):
        return
    with open(FILE_PATH, "r") as f:
        lines = f.readlines()[1:]   # skip header — slicing on a list ✓
    loaded = []
    for line in lines:
        parts = line.strip().split(",")
        if len(parts) == 3:
            loaded.append([parts[0], parts[1], int(parts[2])])
    if loaded:
        records.clear()
        records.extend(loaded)
        print(f"  📂  Loaded {len(loaded)} records from '{FILE_PATH}'.\n")


# ── 4. DISPLAY HELPERS ────────────────────────────────────────

def print_table(data: list, title: str = "") -> None:
    if title:
        print(f"\n  {'─'*40}")
        print(f"  {title}")
        print(f"  {'─'*40}")
    if not data:
        print("  (no records to display)")
        return
    print(f"  {'Name':<14} {'Subject':<12} {'Marks':>5}")
    print(f"  {'─'*14} {'─'*12} {'─'*5}")
    for r in data:
        print(f"  {r[0]:<14} {r[1]:<12} {r[2]:>5}")


def print_menu() -> None:
    print("\n" + "═"*44)
    print("   🎓  STUDENT MANAGEMENT SYSTEM")
    print("═"*44)
    print("  1 · Add student")
    print("  2 · Show toppers (by subject)")
    print("  3 · Show class average (by subject)")
    print("  4 · Show above-average students")
    print("  5 · Remove student")
    print("  6 · List all students")
    print("  7 · Exit")
    print("═"*44)


# ── 5. MENU-DRIVEN CLI ────────────────────────────────────────

def main() -> None:
    load_from_file()

    while True:
        print_menu()
        choice = input("  Enter choice (1-7): ").strip()

        if choice == "1":
            # ── Add student ──
            name    = input("  Name    : ").strip().title()
            subject = input("  Subject : ").strip().title()
            try:
                marks = int(input("  Marks   : ").strip())
                if not (0 <= marks <= 100):
                    raise ValueError
            except ValueError:
                print("  ⚠️  Marks must be an integer 0–100.")
                continue
            add_student(name, subject, marks)

        elif choice == "2":
            # ── Show toppers ──
            subject = input("  Subject (Math / Physics / Chemistry): ").strip().title()
            toppers = get_toppers(subject)
            print_table(toppers, f"Top 3 — {subject}")

        elif choice == "3":
            # ── Class average ──
            subject = input("  Subject (Math / Physics / Chemistry): ").strip().title()
            avg = class_average(subject)
            if avg is not None:
                print(f"\n  📊  Average marks for {subject}: {avg:.2f}")

        elif choice == "4":
            # ── Above-average students ──
            result = above_average_students()
            if result:
                above, overall_avg = result
                print(f"\n  Overall class average: {overall_avg}")
                print_table(above, "Students Scoring Above Average")

        elif choice == "5":
            # ── Remove student ──
            name = input("  Name to remove: ").strip().title()
            remove_student(name)

        elif choice == "6":
            # ── List all ──
            print_table(records, "All Students")

        elif choice == "7":
            # ── Exit + save ──
            save_to_file()
            print("  👋  Goodbye!\n")
            break

        else:
            print("  ⚠️  Invalid choice. Please enter 1–7.")


if __name__ == "__main__":
    main()
