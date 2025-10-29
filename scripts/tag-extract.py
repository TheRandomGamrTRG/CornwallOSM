import json
from collections import Counter

# Path to your GeoJSON file
input_file = input('input file name here:')

with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

tag_counter = Counter()

for feature in data["features"]:
    props = feature.get("properties", {})
    for key, value in props.items():
        # Skip if value is None, empty string, or just whitespace
        if value is None:
            continue
        if isinstance(value, str) and value.strip() == "":
            continue
        tag_counter[key] += 1

print("Tag frequencies in this GeoJSON file (ignoring empty values):")
for tag, count in tag_counter.most_common():
    print(f"{tag}: {count}")
