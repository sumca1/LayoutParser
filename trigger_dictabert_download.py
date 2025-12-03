"""
מפעיל הורדת DictaBERT מ-HuggingFace דרך GitHub Actions
מודל: dicta-il/dictabert-large-char-menaked (~1.2GB)
"""

import requests
import os
from datetime import datetime

# הגדרות
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
REPO_OWNER = "sumca1"
REPO_NAME = "LayoutParser"
WORKFLOW_FILE = "download-dictabert.yml"

# פרטי המודל
MODEL_NAME = "dictabert-large-char-menaked"
HF_REPO = "dicta-il/dictabert-large-char-menaked"

def trigger_workflow():
    """מפעיל workflow להורדת DictaBERT"""
    
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/actions/workflows/{WORKFLOW_FILE}/dispatches"
    
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {GITHUB_TOKEN}",
        "Content-Type": "application/json"
    }
    
    data = {
        "ref": "main",
        "inputs": {
            "model_name": MODEL_NAME,
            "hf_repo": HF_REPO
        }
    }
    
    print(f"🚀 מפעיל הורדת DictaBERT...")
    print(f"📦 מודל: {HF_REPO}")
    print(f"🏷️  שם: {MODEL_NAME}")
    print(f"⏰ זמן: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 204:
        print("✅ הWorkflow הופעל בהצלחה!")
        print()
        print(f"🔗 עקוב אחרי ההתקדמות:")
        print(f"   https://github.com/{REPO_OWNER}/{REPO_NAME}/actions")
        print()
        print(f"📥 אחרי שההורדה תסתיים (2-3 דקות):")
        print(f"   https://github.com/{REPO_OWNER}/{REPO_NAME}/releases")
        print()
        print("⏳ המודל הוא 1.2GB - יקח כ-2-3 דקות להוריד ולארוז")
        print("📊 הrelease יופיע עם תיוג dictabert-large-char-menaked_TIMESTAMP")
        
    else:
        print(f"❌ שגיאה בהפעלת workflow!")
        print(f"📊 Status code: {response.status_code}")
        print(f"📄 תגובה: {response.text}")

if __name__ == "__main__":
    trigger_workflow()
