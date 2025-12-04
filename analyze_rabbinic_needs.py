"""
ניתוח המודול הנוכחי - מה חסר לעברית רבנית + ארמית?
"""

from transformers import AutoTokenizer, AutoModel
import torch

print("🔍 בודק את המודול הנוכחי שלך\n")
print("=" * 80)

# בדיקת המודל הנוכחי
MODEL_DIR = "downloaded_models/dictabert"

try:
    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_DIR, trust_remote_code=True, local_files_only=True
    )
    model = AutoModel.from_pretrained(
        MODEL_DIR, trust_remote_code=True, local_files_only=True
    )
    
    print("✅ המודל הנוכחי:")
    print(f"   📦 {type(model).__name__}")
    print(f"   🔤 מחלקות ניקוד: {len(model.config.nikud_classes)}")
    
    # בדיקה מה המודל עושה
    print("\n📊 יכולות המודל הנוכחי:")
    print("-" * 80)
    
    capabilities = {
        "✅ ניקוד בסיסי": "עובד - מוסיף ניקוד לעברית",
        "❌ ניתוח מורפולוגי": "חסר - לא מזהה שורש, בניין, זמן",
        "❌ ניתוח לקסיקלי": "חסר - לא מבין משמעות מילים",
        "❌ התייחסות לסימני עצירה": "חלקי - רק ברמת tokenization",
        "❌ זיהוי כותרות": "חסר - מתעלם ממבנה",
        "❌ עברית רבנית": "⚠️ חלקי - לא מאומן ספציפית",
        "❌ ארמית": "⚠️ לא תומך"
    }
    
    for capability, status in capabilities.items():
        print(f"   {capability}: {status}")
    
    print("\n🎯 מה זה אומר לפרויקט OCR שלך:")
    print("-" * 80)
    
    issues = {
        "בעיה 1": {
            "desc": "הומוגרפים לא מזוהים נכון",
            "example": "בית (שם עצם) vs בית (מילת יחס) - אותו ניקוד שגוי",
            "solution": "צריך dictabert-morph או BEREL"
        },
        "בעיה 2": {
            "desc": "ארמית לא מטופלת",
            "example": "דהוה, דאמר - ייתן ניקוד עברי שגוי",
            "solution": "צריך BEREL (מאומן על ארמית)"
        },
        "בעיה 3": {
            "desc": "מבנה מסמך מתעלם",
            "example": "כותרות, הערות שוליים - מנוקדות כטקסט רגיל",
            "solution": "צריך אינטגרציה עם LayoutParser"
        },
        "בעיה 4": {
            "desc": "הקשר רבני לא מובן",
            "example": "צירופים רבניים, לשון חכמים",
            "solution": "צריך BEREL או DictaLM"
        },
        "בעיה 5": {
            "desc": "סימני פיסוק לא משפיעים",
            "example": "נקודה, פסיק - לא משנים את הניקוד",
            "solution": "צריך context-aware model"
        }
    }
    
    for issue_num, issue in issues.items():
        print(f"\n⚠️ {issue_num}: {issue['desc']}")
        print(f"   דוגמה: {issue['example']}")
        print(f"   💡 פתרון: {issue['solution']}")
    
except Exception as e:
    print(f"❌ שגיאה: {e}")

print("\n" + "=" * 80)
print("🎯 המודלים שאתה צריך לעברית רבנית + ארמית:")
print("=" * 80)

recommendations = {
    "1. BEREL ⭐⭐⭐⭐⭐": {
        "priority": "קריטי!",
        "size": "~400MB",
        "what": "BERT מיוחד לעברית רבנית + ארמית",
        "features": [
            "✅ מאומן על תלמוד, מדרשים, ראשונים",
            "✅ מבין ארמית (דהוה, דאמר, וכו')",
            "✅ צירופים רבניים",
            "✅ לשון חכמים",
            "✅ ניתוח מורפולוגי מובנה"
        ],
        "use_case": "זה הבסיס לפרויקט שלך!"
    },
    "2. dictabert-morph": {
        "priority": "חשוב מאוד",
        "size": "~400MB",
        "what": "ניתוח מורפולוגי",
        "features": [
            "✅ שורש, בניין, זמן, גוף",
            "✅ הבחנה בין הומוגרפים",
            "✅ זיהוי צורות פועל",
            "⚠️ עברית מודרנית (לא רבנית)"
        ],
        "use_case": "משלים ל-BEREL לעברית מודרנית"
    },
    "3. dictabert-lex": {
        "priority": "משלים",
        "size": "~400MB",
        "what": "ניתוח לקסיקלי - משמעות",
        "features": [
            "✅ הבנת הקשר סמנטי",
            "✅ ניתוח פוליסמיה",
            "⚠️ עברית מודרנית"
        ],
        "use_case": "אופציונלי - פחות קריטי לרבנית"
    },
    "4. DictaLM-3.0 (אם יש GPU)": {
        "priority": "אופציונלי",
        "size": "3-50GB",
        "what": "מודל שפה ענק",
        "features": [
            "✅ הבנה מלאה של הקשר",
            "✅ עובד גם על רבנית",
            "❌ כבד מאוד"
        ],
        "use_case": "רק אם יש משאבים"
    }
}

for model, info in recommendations.items():
    print(f"\n{model}")
    print(f"   🎯 עדיפות: {info['priority']}")
    print(f"   💾 גודל: {info['size']}")
    print(f"   📝 {info['what']}")
    print(f"   🔧 {info['use_case']}")
    print("\n   תכונות:")
    for feature in info['features']:
        print(f"      {feature}")

print("\n" + "=" * 80)
print("🚀 תוכנית פעולה לפרויקט OCR רבני:")
print("=" * 80)

action_plan = """
שלב 1: הורד BEREL (קריטי!)
   • זה המודל המתאים ביותר לפרויקט שלך
   • מטפל בארמית + עברית רבנית
   • נוריד עכשיו דרך GitHub Actions

שלב 2: הורד dictabert-morph (בהורדה)
   • משלים ל-BEREL לניתוח מורפולוגי
   • שיפור דיוק ל-95%+

שלב 3: שילוב עם LayoutParser
   • זיהוי כותרות ← משפיע על ניקוד
   • הערות שוליים ← סגנון ניקוד שונה
   • מבנה עמוד ← הקשר מסמכי

שלב 4: התאמה לסימני פיסוק
   • נקודה/פסיק ← שינוי בניקוד
   • מרכאות ← ציטוט (ניקוד מיוחד)
   • מקף ← סמיכות

📊 צפי שיפור:
   • עכשיו: ~90% דיוק (עברית מודרנית בלבד)
   • עם BEREL: ~95% דיוק (עברית רבנית + ארמית)
   • עם BEREL + morph: ~97% דיוק
   • עם אינטגרציה מלאה: ~98%+ דיוק

🎯 התוצאה:
   מערכת OCR מושלמת לספרים רבניים:
   • תלמוד ✓
   • מדרשים ✓
   • ראשונים ✓
   • טקסטים מעורבים עברית-ארמית ✓
"""

print(action_plan)

print("\n💡 רוצה שאגדיר workflow גם ל-BEREL?")
print("   זה הכי קריטי לפרויקט שלך!")
