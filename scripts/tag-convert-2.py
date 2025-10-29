import json

# Mappings
suffix_map = {
    "ST": "Street",
    "AVE": "Avenue",
    "AV": "Avenue",
    "RD": "Road",
    "BLVD": "Boulevard",
    "DR": "Drive",
    "LN": "Lane",
    "CT": "Court",
    "PL": "Place",
}
dir_map = {
    "N": "North", "S": "South", "E": "East", "W": "West",
    "NE": "Northeast", "NW": "Northwest",
    "SE": "Southeast", "SW": "Southwest",
}
province_map = {"ON": "Ontario"}
country_map = {"CA": "Canada"}

# Helper: safely get and clean a property
def safe_get(props, key):
    value = props.get(key)
    if value is None:
        return ""
    return str(value).strip()

def normalize_street(street, suffix, direction):
    parts = []
    if street:
        parts.append(street.title())  # Regular Title Case
    if suffix and suffix in suffix_map:
        parts.append(suffix_map[suffix])
    if direction and direction in dir_map:
        parts.append(dir_map[direction])
    return " ".join(parts)

def convert_properties(props):
    tags = {}

    # Safe extract values
    street      = safe_get(props, "STREET")
    suffix      = safe_get(props, "SUFFIX")
    direction   = safe_get(props, "DIRECTION")
    housenumber = safe_get(props, "ST_NUMBER")
    city        = safe_get(props, "CITY")
    province    = safe_get(props, "PROVINCE")
    country     = safe_get(props, "COUNTRY")
    postal      = safe_get(props, "POSTAL")

    # Build addr:street
    addr_street = normalize_street(street, suffix, direction)
    if addr_street:
        tags["addr:street"] = addr_street

    # House number
    if housenumber:
        tags["addr:housenumber"] = housenumber

    # City
    if city:
        tags["addr:city"] = city.title()

    # Province
    if province in province_map:
        tags["addr:province"] = province_map[province]

    # Country
    if country in country_map:
        tags["addr:country"] = country_map[country]

    # Postcode
    if postal:
        tags["addr:postcode"] = postal

    return tags

# Example usage with a GeoJSON file
if __name__ == "__main__":
    input_file = input('Input file:')
    output_file = input('Output file:')

    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    for feature in data["features"]:
        props = feature.get("properties", {})
        feature["properties"] = convert_properties(props)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Converted data saved to {output_file}")
