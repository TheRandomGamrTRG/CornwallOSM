import json
from titlecase import titlecase  # pip install titlecase
from pathlib import Path

# --- MAPPINGS ---

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
    "TER": "Terrace",
    "CRES": "Crescent",
    "WAY": "Way",
    "PKWY": "Parkway",
}

dir_map = {
    "N": "North", "S": "South", "E": "East", "W": "West",
    "NE": "Northeast", "NW": "Northwest",
    "SE": "Southeast", "SW": "Southwest",
}

province_map = {"ON": "Ontario"}
country_map = {"CA": "Canada"}

# --- HELPERS ---

def safe_get(props, key):
    """Safely get a value from a dict and strip whitespace."""
    val = props.get(key)
    if val is None:
        return ""
    return str(val).strip()

def normalize_street(street, suffix, direction):
    """Combine and format street parts according to OSM naming."""
    parts = []
    if street:
        parts.append(titlecase(street.lower()))
    if suffix:
        sfx = suffix.upper()
        parts.append(suffix_map.get(sfx, titlecase(suffix)))
    if direction:
        d = direction.upper()
        parts.append(dir_map.get(d, titlecase(direction)))
    return " ".join(parts).strip()

def convert_properties(props):
    """Convert city data tags into OSM-compliant addr:* tags."""
    tags = {}

    street      = safe_get(props, "STREET")
    suffix      = safe_get(props, "SUFFIX")
    direction   = safe_get(props, "DIRECTION")
    housenumber = safe_get(props, "ST_NUMBER")
    unit        = safe_get(props, "UNIT")
    city        = safe_get(props, "CITY")
    province    = safe_get(props, "PROVINCE")
    country     = safe_get(props, "COUNTRY")
    postal      = safe_get(props, "POSTAL")

    # Build the street name
    addr_street = normalize_street(street, suffix, direction)
    if addr_street:
        tags["addr:street"] = addr_street

    if housenumber:
        tags["addr:housenumber"] = housenumber
    if unit:
        tags["addr:unit"] = unit
    if city:
        tags["addr:city"] = titlecase(city.lower())
    if province:
        tags["addr:province"] = province_map.get(province.upper(), titlecase(province))
    if country:
        tags["addr:country"] = country_map.get(country.upper(), titlecase(country))
    if postal:
        tags["addr:postcode"] = postal

    return tags


# --- MAIN ---

def process_geojson(input_path, output_path):
    """Read a GeoJSON, convert address tags, and write output."""
    with open(input_path, encoding="utf-8") as f:
        data = json.load(f)

    for feature in data.get("features", []):
        props = feature.get("properties", {})
        feature["properties"] = convert_properties(props)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ Converted {len(data.get('features', []))} features")
    print(f"💾 Output saved to {output_path}")


if __name__ == "__main__":
    # Example usage: edit these file paths as needed
    input_file = input('Input file name: ')
    output_file = input('Output file name: ')

    process_geojson(input_file, output_file)
