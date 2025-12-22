import pandas as pd
import json

COLUMN_RULES = {
    "age": {
        "type": "int",
        "min": 0,
        "max": 120,
        "required": True
    },
    "score": {
        "type": "float",
        "min": 0,
        "max": 100,
        "required": True
    },
    "email": {
        "type": "string",
        "required": True
    }
}

def validate_data(csv_path):
    df = pd.read_csv(csv_path)
    errors = []

    for index, row in df.iterrows():
        row_number = index + 2 

        for column, rules in COLUMN_RULES.items():
            value = row.get(column)

            if pd.isna(value):
                if rules.get("required", False):
                    errors.append({
                        "row": row_number,
                        "column": column,
                        "error": "Missing value"
                    })
                continue

            expected_type = rules.get("type")

            if expected_type == "int":
                try:
                    int_value = int(value)
                    if float(value) != int_value:
                        raise ValueError
                    value = int_value
                except:
                    errors.append({
                        "row": row_number,
                        "column": column,
                        "error": f"Expected int but got {value}"
                    })
                    continue

            elif expected_type == "float":
                try:
                    value = float(value)
                except:
                    errors.append({
                        "row": row_number,
                        "column": column,
                        "error": f"Expected float but got {value}"
                    })
                    continue

            elif expected_type == "string":
                if not isinstance(value, str):
                    errors.append({
                        "row": row_number,
                        "column": column,
                        "error": f"Expected string but got {value}"
                    })
                    continue

            if "min" in rules and value < rules["min"]:
                errors.append({
                    "row": row_number,
                    "column": column,
                    "error": f"Value {value} < minimum {rules['min']}"
                })

            if "max" in rules and value > rules["max"]:
                errors.append({
                    "row": row_number,
                    "column": column,
                    "error": f"Value {value} > maximum {rules['max']}"
                })

    return errors

if __name__ == "__main__":
    INPUT_CSV = "sample_data.csv"
    OUTPUT_JSON = "error_report.json"

    error_list = validate_data(INPUT_CSV)

    if error_list:
        with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
            json.dump(error_list, f, indent=4)

        print(f"Errors found: {len(error_list)}")
        print(f"Error report saved to {OUTPUT_JSON}")
    else:
        print("No errors found. Data is clean.")