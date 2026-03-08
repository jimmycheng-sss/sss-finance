import csv
import json
import os
import subprocess
from datetime import datetime

def csv_to_json():
    csv_path = 'swift_spark_studios/SSS_ACCOUNTING_LOG.csv'
    json_path = 'swift_spark_studios/accounting_data.json'
    
    if not os.path.exists(csv_path):
        return

    transactions = []
    total_balance = 0.0
    jimmy_loans = 0.0

    try:
        with open(csv_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    amount = float(row['Amount'])
                except:
                    amount = 0.0
                
                row['Amount'] = amount
                transactions.append(row)
                total_balance += amount
                
                if 'jimmy personal loan' in row['Description'].lower():
                    jimmy_loans += amount

        data = {
            "last_updated": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "total_balance": round(total_balance, 2),
            "jimmy_loans": round(jimmy_loans, 2),
            "transactions": transactions
        }
        
        with open(json_path, 'w') as f:
            json.dump(data, f, indent=4)
            
    except Exception as e:
        pass

def auto_deploy():
    # Attempt to git push if in a git repo
    try:
        if os.path.exists('swift_spark_studios/.git'):
            subprocess.run(["git", "-C", "swift_spark_studios", "add", "."], check=True)
            subprocess.run(["git", "-C", "swift_spark_studios", "commit", "-m", f"Auto-update: {datetime.now()}"], check=True)
            subprocess.run(["git", "-C", "swift_spark_studios", "push"], check=True)
    except:
        pass

if __name__ == "__main__":
    csv_to_json()
    auto_deploy()
