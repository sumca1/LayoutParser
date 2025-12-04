"""
מפעיל הורדת DictaBERT-Morph מ-HuggingFace דרך GitHub Actions
מודל: dicta-il/dictabert-morph (~400MB)
"""

import requests
import os
from datetime import datetime

# הגדרות
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
REPO_OWNER = "sumca1"
REPO_NAME = "LayoutParser"
WORKFLOW_FILE = "download-dictabert-morph.yml"

# פרטי המודל
MODEL_NAME = "dictabert-morph"
HF_REPO = "dicta-il/dictabert-morph"

def trigger_workflow():
    """מפעיל workflow להורדת DictaBERT-Morph"""
    
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
    
    print("🚀 מפעיל הורדת DictaBERT-Morph...")
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
        print(f"📥 אחרי שההורדה תסתיים (1-2 דקות):")
        print(f"   https://github.com/{REPO_OWNER}/{REPO_NAME}/releases")
        print()
        print("⏳ המודל הוא 400MB - יקח כ-1-2 דקות להוריד ולארוז")
        print("📊 הrelease יופיע עם תיוג dictabert-morph_TIMESTAMP")
        print()
        print("💡 מה המודל יעשה:")
        print("   • ניתוח מורפולוגי: שורש, בניין, זמן, גוף")
        print("   • שיפור דיוק ניקוד מ-90% ל-95%+")
        print("   • הבחנה בין הומוגרפים")
        
    else:
        print(f"❌ שגיאה בהפעלת workflow!")
        print(f"📊 Status code: {response.status_code}")
        print(f"📄 תגובה: {response.text}")

if __name__ == "__main__":
    trigger_workflow()
