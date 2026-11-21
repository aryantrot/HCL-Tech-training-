import csv
import os

COLLEGES = {
    "ABES": {
        "location": "Ghaziabad",
        "teaching": 78.0,
        "research": 65.0,
        "placements": 82.5,
        "perception": 75.0,
        "nirf_ref": 151,
    },
    "Bennett": {
        "location": "Greater Noida",
        "teaching": 82.0,
        "research": 76.0,
        "placements": 80.0,
        "perception": 84.0,
        "nirf_ref": 85,
    },
    "Amity": {
        "location": "Noida",
        "teaching": 85.0,
        "research": 82.0,
        "placements": 81.5,
        "perception": 90.0,
        "nirf_ref": 32,
    },
    "Galgotia": {
        "location": "Greater Noida",
        "teaching": 74.0,
        "research": 70.0,
        "placements": 78.0,
        "perception": 81.0,
        "nirf_ref": 101,
    },
    "GL Bajaj": {
        "location": "Greater Noida",
        "teaching": 79.5,
        "research": 64.0,
        "placements": 84.0,
        "perception": 76.5,
        "nirf_ref": 151,
    },
}

METRICS = ["teaching", "research", "placements", "perception"]


def compute_score(entry: dict, weights: dict) -> float:
    total_w = sum(weights.values())
    if total_w <= 0:
        return 0.0
    weighted_total = sum(entry[m] * weights[m] for m in METRICS)
    return round(weighted_total / total_w, 2)


def ask_weights() -> dict:
    print("\nSet priority weights (0 to 10). Press Enter for default:")
    defaults = {
        "teaching": 3,
        "research": 2,
        "placements": 4,
        "perception": 2,
    }
    weights = {}

    for m in METRICS:
        raw = input(f"  {m.capitalize()} [default {defaults[m]}]: ").strip()
        if not raw:
            weights[m] = defaults[m]
            continue
        try:
            val = float(raw)
            if val < 0:
                print("  -> Weight cannot be negative; using default.")
                weights[m] = defaults[m]
            else:
                weights[m] = val
        except ValueError:
            print("  -> Enter a valid number; using default.")
            weights[m] = defaults[m]

    return weights


def show_colleges() -> None:
    print("\n--- Colleges in Dataset ---")
    for idx, (name, info) in enumerate(COLLEGES.items(), start=1):
        print(
            f"{idx}. {name:<12} | {info['location']:<14} | NIRF Ref: #{info['nirf_ref']}"
        )


def pick_colleges() -> list[str]:
    names = list(COLLEGES.keys())
    show_colleges()
    raw = input("\nEnter numbers to compare (e.g., 1, 3, 5) or type 'all': ").strip()

    if raw.lower() == "all":
        return names

    chosen = []
    for part in raw.split(","):
        part = part.strip()
        if not part.isdigit():
            continue
        i = int(part) - 1
        if 0 <= i < len(names) and names[i] not in chosen:
            chosen.append(names[i])

    if len(chosen) < 2:
        print("Select at least 2 colleges. Comparing all 5 by default.")
        return names

    return chosen


def build_ranking(selected: list[str], weights: dict) -> list[dict]:
    table = []
    for name in selected:
        info = COLLEGES[name]
        score = compute_score(info, weights)
        table.append(
            {
                "college": name,
                "location": info["location"],
                "nirf_ref": info["nirf_ref"],
                "teaching": info["teaching"],
                "research": info["research"],
                "placements": info["placements"],
                "perception": info["perception"],
                "custom_score": score,
            }
        )

    table.sort(key=lambda row: row["custom_score"], reverse=True)
    for pos, row in enumerate(table, start=1):
        row["rank"] = pos
    return table


def display_table(rows: list[dict]) -> None:
    print("\n=== Comparison Result (Ranked by Custom Score) ===")
    header = (
        f"{'Rank':<5} {'College':<12} {'Score':<7} {'NIRF':<6} "
        f"{'Teach':<6} {'Res':<6} {'Place':<6} {'Perc':<6}"
    )
    print(header)
    print("-" * len(header))

    for r in rows:
        print(
            f"#{r['rank']:<4} {r['college']:<12} {r['custom_score']:<7.2f} "
            f"#{r['nirf_ref']:<5} {r['teaching']:<6.1f} {r['research']:<6.1f} "
            f"{r['placements']:<6.1f} {r['perception']:<6.1f}"
        )

    top = rows[0]
    top_place = max(rows, key=lambda x: x["placements"])
    top_res = max(rows, key=lambda x: x["research"])

    print("\nHighlights:")
    print(f"  * Best overall match: {top['college']} ({top['custom_score']}/100)")
    print(f"  * Best placement score: {top_place['college']} ({top_place['placements']}/100)")
    print(f"  * Best research score: {top_res['college']} ({top_res['research']}/100)")


def add_college_entry() -> None:
    print("\n--- Add Another College ---")
    name = input("Short college name: ").strip()
    if not name or name in COLLEGES:
        print("Invalid or duplicate name.")
        return

    location = input("City/Location: ").strip() or "NCR"
    try:
        nirf_ref = int(input("NIRF Reference Rank (number): ").strip())
        teaching = float(input("Teaching (0-100): ").strip())
        research = float(input("Research (0-100): ").strip())
        placements = float(input("Placements (0-100): ").strip())
        perception = float(input("Perception (0-100): ").strip())
    except ValueError:
        print("Please enter valid numbers. Entry skipped.")
        return

    COLLEGES[name] = {
        "location": location,
        "teaching": teaching,
        "research": research,
        "placements": placements,
        "perception": perception,
        "nirf_ref": nirf_ref,
    }
    print(f"Added '{name}' to current session.")


def save_csv(rows: list[dict], filename: str = "comparison_output.csv") -> None:
    cols = [
        "rank",
        "college",
        "location",
        "custom_score",
        "nirf_ref",
        "teaching",
        "research",
        "placements",
        "perception",
    ]
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=cols)
        writer.writeheader()
        writer.writerows(rows)
    print(f"\nExported to: {os.path.abspath(filename)}")


def main() -> None:
    print("==========================================================")
    print(" College Ranking Comparison Tool | HCLTech Training Mini-Project")
    print("==========================================================")

    latest_rows = []

    while True:
        print("\n1. Compare colleges")
        print("2. View all colleges")
        print("3. Add a college")
        print("4. Export last result to CSV")
        print("5. Exit")

        choice = input("\nEnter choice (1-5): ").strip()

        if choice == "1":
            selected = pick_colleges()
            weights = ask_weights()
            latest_rows = build_ranking(selected, weights)
            display_table(latest_rows)
        elif choice == "2":
            show_colleges()
        elif choice == "3":
            add_college_entry()
        elif choice == "4":
            if not latest_rows:
                print("Run option 1 first before exporting.")
            else:
                fname = input("File name [comparison_output.csv]: ").strip()
                save_csv(latest_rows, fname or "comparison_output.csv")
        elif choice == "5":
            print("Closing tool.")
            break
        else:
            print("Choose a valid option from 1 to 5.")


if __name__ == "__main__":
    main()