import json

# Input/output file paths
input_file = input('Input file name:')
output_file = input('Output file name:')

# Mapping from city fields to OSM tags
mapping = {
    "ST_NUMBER": "addr:housenumber",
    "STREET_LNG": "addr:street",
    "CITY": "addr:city",
    "PROVINCE": "addr:province",
    "POSTAL": "addr:postcode",
    "COUNTRY": "addr:country",
    "UNIT": "addr:unit",
    "BUILDING": "building:name"
}

with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

for feature in data["features"]:
    props = feature.get("properties", {})
    
    # Build a fresh set of properties with only mapped tags
    new_props = {}
    for old, new in mapping.items():
        value = props.get(old)
        if value is None:
            continue
        if isinstance(value, str) and value.strip() == "":
            continue
        new_props[new] = value
    
    feature["properties"] = new_props

# Write out the cleaned GeoJSON
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Converted GeoJSON written to {output_file}")
