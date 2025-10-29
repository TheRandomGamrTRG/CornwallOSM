import json

# Input GeoJSON file
input_file = "AddressPoints_5738876143412506367.geojson"

# Optional output file
output_file = "Tag-Extract-Raw.txt"

# Choose Tag
tagchosen = input('What tag:')

with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# Collect all STREET_LNG values
street_names = set()  # use set to get unique names
for feature in data["features"]:
    props = feature.get("properties", {})
    street = props.get(tagchosen)
    if street and street.strip():  # skip empty values
        street_names.add(street.strip())

# Print the unique street names
print(f"Found {len(street_names)} unique STREET_LNG values:")
for name in sorted(street_names):
    print(name)

# Optionally write to a text file
with open(output_file, "w", encoding="utf-8") as f:
    for name in sorted(street_names):
        f.write(name + "\n")

print(f"Street names saved to {output_file}") 