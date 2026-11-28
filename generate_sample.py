"""Student Budget Tracker - Sample Data Generator
This script generates sample transaction records.
The records include income and expenses from September to November 2026."""

import json
import random
from pathlib import Path

# File location
DATA_FILE = Path(__file__).parent / "data" / "sample.json"

# Standard categories
categories = [
    "Food",
    "Shopping",
    "Transportation",
    "Entertainment",
    "Education",
    "Other"
]

natures = ["Necessary", "Unplanned", "Impulse"]

# Target records for each month
monthly_targets = {
    "2026-09": {"income": 3, "expense": 17},
    "2026-10": {"income": 3, "expense": 17},
    "2026-11": {"income": 4, "expense": 16}
}

# Load existing records
records = []

if DATA_FILE.exists():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        existing_records = json.load(file)

    for record in existing_records:
        month = record["date"][:7]
        if month in monthly_targets:
            records.append(record)
        else:
            print("Skipped invalid or out-of-range date:", record["date"])

# Find next available ID
next_id = max((record["id"] for record in records), default=0) + 1

# Generate missing records
for month, targets in monthly_targets.items():
    for record_type, target_count in targets.items():

        current_count = sum(
            1 for record in records
            if record["date"].startswith(month)
            and record["type"] == record_type
        )

        if current_count > target_count:
            raise ValueError("Too many existing records for " + month)

        for i in range(target_count - current_count):

            day = random.randint(1, 28)
            date = f"{month}-{day:02d}"

            if record_type == "income":
                amount = round(random.uniform(200, 1500), 2)
                category = "Other"
                nature = "Necessary"
            else:
                amount = round(random.uniform(5, 160), 2)
                category = random.choice(categories)
                nature = random.choice(natures)

            record = {
                "id": next_id,
                "date": date,
                "type": record_type,
                "amount": amount,
                "category": category,
                "nature": nature
            }

            records.append(record)
            next_id += 1

# Sort records by date
records.sort(key=lambda record: record["date"])

# Save records
DATA_FILE.parent.mkdir(exist_ok=True)

with open(DATA_FILE, "w", encoding="utf-8") as file:
    json.dump(records, file, indent=4)

print("Sample data saved")
print("Total records:", len(records))
print("Income records:", sum(r["type"] == "income" for r in records))
print("Expense records:", sum(r["type"] == "expense" for r in records))