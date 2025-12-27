import pandas as pd
import json
import re
from datetime import datetime

LIBRARY_RULES = {
    "book_code": {
        "type": "string",
        "pattern": r"^[A-Z]{2}\d{4}$",
        "required": True
    },
    "title": {"type": "string", "required": True},
    "borrower": {"type": "string", "required": True},
    "borrow_date": {"type": "date", "format": "%Y-%m-%d", "required": True},
    "return_date": {"type": "date", "format": "%Y-%m-%d", "required": False},
    "late_fee": {"type": "int", "min": 0, "required": True}
}

def validate_library(csv_path):
    df = pd.read_csv(csv_path)
    errors = []
    
    for idx, row in df.iterrows():
        row_num = idx + 2
        borrow_date = None
        return_date = None
        
        for col, rules in LIBRARY_RULES.items():
            value = row.get(col)
            
            if pd.isna(value):
                if rules.get("required"):
                    errors.append({
                        "row": row_num,
                        "column": col,
                        "error": "필수 값이 누락되었습니다"
                    })
                continue
            
            if col == "book_code":
                value = str(value).strip()
                if not re.match(rules["pattern"], value):
                    errors.append({
                        "row": row_num,
                        "column": col,
                        "error": f"invalid form of book code(ex: AB1234): {value}"
                    })
            
            elif col in ["borrow_date", "return_date"]:
                try:
                    date_obj = datetime.strptime(str(value).strip(), rules["format"])
                    if col == "borrow_date":
                        borrow_date = date_obj
                    else:
                        return_date = date_obj
                except:
                    errors.append({
                        "row": row_num,
                        "column": col,
                        "error": f"invalid form of date (YYYY-MM-DD): {value}"
                    })
            
            elif col == "late_fee":
                try:
                    fee = int(value)
                    if fee < 0:
                        errors.append({
                            "row": row_num,
                            "column": col,
                            "error": f"late fees must be 0 or greater: {value}"
                        })
                except:
                    errors.append({
                        "row": row_num,
                        "column": col,
                        "error": f"late fees must be a whole number: {value}"
                    })
        
        if borrow_date and return_date:
            if return_date < borrow_date:
                errors.append({
                    "row": row_num,
                    "column": "return_date",
                    "error": "the return date is earlier than the loan date"
                })
    
    return errors

if __name__ == "__main__":
    INPUT_CSV = "sample_library.csv"
    OUTPUT_JSON = "library_errors.json"
    
    print("=" * 60)
    print("library loan record verifier")
    print("=" * 60)
    print(f"input file: {INPUT_CSV}")
    
    try:
        error_list = validate_library(INPUT_CSV)
        
        if error_list:
            with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
                json.dump(error_list, f, ensure_ascii=False, indent=4)
            print(f"{len(error_list)} errors found")
            print(f"error report: {OUTPUT_JSON}")
        else:
            print("no error!.")
    
    except FileNotFoundError:
        print(f"file not found: {INPUT_CSV}")
    except Exception as e:
        print(f"error occurred: {str(e)}")