import csv
import re

def extract_regions(title):
    # 1. Remove everything after 'and abbot of' or similar patterns
    title = re.split(r'\band\s+abbot of\b|\babbot of\b', title, flags=re.IGNORECASE)[0]

    # 2. Extract part after 'bishop of' or 'metropolitan of' (case insensitive)
    match = re.search(r'(bishop|metropolitan) of (.+)', title, re.IGNORECASE)
    if not match:
        return []

    regions_part = match.group(2)

    # 3. Replace " and " (with spaces) with comma to treat as delimiter
    regions_part = re.sub(r'\s+and\s+', ',', regions_part, flags=re.IGNORECASE)

    # 4. Split by commas or ampersands
    parts = re.split(r',|&', regions_part)

    # 5. Clean whitespace and filter empty strings
    regions = [p.strip() for p in parts if p.strip()]

    return regions

def main():
    input_file = "data/bishops.csv"
    output_file = "data/bishop_map_data.csv"

    skip_terms = ["general bishop", "pope", "bishop & abbot"]
    filtered_bishops = []

    with open(input_file, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            title_lower = row["title"].lower()
            if any(term in title_lower for term in skip_terms):
                continue

            regions = extract_regions(row["title"])
            if not regions:
                continue

            regions_str = ", ".join(regions)

            filtered_bishops.append({
                "name": row["name"],
                "regions": regions_str
            })

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        fieldnames = ["name", "regions"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(filtered_bishops)

    print(f"✅ Saved bishop map data to {output_file}")

if __name__ == "__main__":
    main()
