#!/bin/bash

# Configuration
REPO_PATH="/data/.openclaw/workspace/swift_spark_studios"
REMOTE_URL="https://github.com/jimmycheng-sss/sss-finance.git"

cd "$REPO_PATH"

# Initialize git if not already
if [ ! -d ".git" ]; then
    git init
    git remote add origin "$REMOTE_URL"
    git branch -M main
fi

# Function to update and push
update_and_push() {
    # Run the JSON update script
    python3 update_json.py
    
    # Add files
    git add finance.html accounting_data.json SSS_ACCOUNTING_LOG.csv
    
    # Commit
    git commit -m "Update finance records: $(date +'%Y-%m-%d %H:%M:%S')"
    
    # Push (Note: This will fail if no credential helper/token is set)
    git push -u origin main
}

update_and_push
