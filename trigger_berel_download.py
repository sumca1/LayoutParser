"""
סקריפט להפעלת הורדת BEREL דרך GitHub Actions
"""

import requests
import os

# הגדרות
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
REPO_OWNER = "sumca1"
REPO_NAME = "LayoutParser"
WORKFLOW_FILE = "download-berel.yml"

if not GITHUB_TOKEN:
    print("❌ שגיאה: GITHUB_TOKEN לא מוגדר")
    print("📝 הגדר אותו ב-PowerShell:")
    print('   $env:GITHUB_TOKEN="ghp_..."')
    exit(1)

# URL להפעלת workflow
url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/actions/workflows/{WORKFLOW_FILE}/dispatches"

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

data = {
    "ref": "main",
    "inputs": {
        "model_name": "dicta-il/BEREL"
    }
}

print(f"🚀 מפעיל הורדת BEREL...")
print(f"📦 מודל: dicta-il/BEREL")
print(f"💾 גודל משוער: ~400-800MB")
print(f"⏱️ זמן משוער: 2-3 דקות")
print()

response = requests.post(url, headers=headers, json=data)

if response.status_code == 204:
    print("✅ הWorkflow הופעל בהצלחה!")
    print()
    print("📊 מה קורה עכשיו:")
    print("   1. GitHub Actions מוריד את BEREL מ-Hugging Face")
    print("   2. יוצר קובץ ZIP: berel.zip")
    print("   3. מעלה ל-GitHub Releases")
    print()
    print("🔗 בדוק התקדמות:")
    print(f"   https://github.com/{REPO_OWNER}/{REPO_NAME}/actions")
    print()
    print("📥 אחרי שיסתיים:")
    print(f"   https://github.com/{REPO_OWNER}/{REPO_NAME}/releases")
    print()
    print("⏳ זמן המתנה: 2-3 דקות")
    print()
    print("🎯 BEREL זה המודל הנכון לעברית רבנית + ארמית!")
else:
    print(f"❌ שגיאה: {response.status_code}")
    print(f"📝 תגובה: {response.text}")
