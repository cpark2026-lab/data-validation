import pandas as pd
import json
import re
from datetime import datetime

CLUB_RULES = {
    "name": {"type": "string", "required": True},
    "grade": {"type": "int", "min": 1, "max": 3, "required": True},
    "phone": {
        "type": "string",
        "pattern": r"^010-\d{4}-\d{4}$",
        "required": True
    },
    "email": {
        "type": "string",
        "pattern": r"^[\w\.-]+@[\w\.-]+\.\w+$",
        "required": True
    },
    "join_date": {
        "type": "date",
        "format": "%Y-%m-%d",
        "required": True
    }
}

def validate_club(csv_path):
    df = pd.read_csv(csv_path)
    errors = []
    
    for idx, row in df.iterrows():
        row_num = idx + 2 
        
        for col, rules in CLUB_RULES.items():
            value = row.get(col)
            
            if pd.isna(value):
                if rules.get("required"):
                    errors.append({
                        "row": row_num,
                        "column": col,
                        "error": "필수 값이 누락되었습니다"
                    })
                continue
            
            value = str(value).strip()
            
            if col == "phone":
                if not re.match(rules["pattern"], value):
                    errors.append({
                        "row": row_num,
                        "column": col,
                        "error": f"invalid form of phone-number (010-XXXX-XXXX): {value}"
                    })
            
            elif col == "email":
                if not re.match(rules["pattern"], value):
                    errors.append({
                        "row": row_num,
                        "column": col,
                        "error": f"invalid form of email: {value}"
                    })
            
            elif col == "join_date":
                try:
                    date_obj = datetime.strptime(value, rules["format"])
                    if date_obj > datetime.now():
                        errors.append({
                            "row": row_num,
                            "column": col,
                            "error": f"Sign-up date is in the future: {value}"
                        })
                except:
                    errors.append({
                        "row": row_num,
                        "column": col,
                        "error": f"invalid form of date (YYYY-MM-DD): {value}"
                    })
            
            elif col == "grade":
                try:
                    grade_val = int(value)
                    if grade_val < rules["min"] or grade_val > rules["max"]:
                        errors.append({
                            "row": row_num,
                            "column": col,
                            "error": f"grade needs to be between 1~3: {value}"
                        })
                except:
                    errors.append({
                        "row": row_num,
                        "column": col,
                        "error": f"grade needs to be form of number: {value}"
                    })
    
    return errors

if __name__ == "__main__":
    INPUT_CSV = "sample_club.csv"
    OUTPUT_JSON = "club_errors.json"
    
    print("=" * 60)
    print("club member list verifier")
    print("=" * 60)
    print(f"input file: {INPUT_CSV}")
    
    try:
        error_list = validate_club(INPUT_CSV)
        
        if error_list:
            with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
                json.dump(error_list, f, ensure_ascii=False, indent=4)
            print(f"error found: {len(error_list)}개")
            print(f"error reporting: {OUTPUT_JSON}")
        else:
            print("no error! Your data is clean.")
    
    except FileNotFoundError:
        print(f"file not found: {INPUT_CSV}")
    except Exception as e:
        print(f"Error occurred: {str(e)}")