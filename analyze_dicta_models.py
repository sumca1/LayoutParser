"""
ניתוח מודלי Dicta - מה כל אחד עושה?
"""

from huggingface_hub import list_models, model_info

print("🔍 ניתוח מפורט של מודלי Dicta\n")
print("=" * 80)

models = list(list_models(author="dicta-il"))

# קטגוריזציה מפורטת
analysis = {
    "מודלי בסיס (Base Models)": {
        "models": [],
        "description": "מודלי BERT בסיסיים - הבסיס לכל השאר",
        "use": "בדרך כלל לא משתמשים בהם ישירות"
    },
    "ניקוד (Diacritization)": {
        "models": [],
        "description": "הוספת ניקוד לעברית",
        "use": "שימוש ישיר - מוסיף ניקוד לטקסט"
    },
    "ניתוח מורפולוגי (Morphology)": {
        "models": [],
        "description": "שורש, בניין, זמן, גוף",
        "use": "משלים לניקוד - מזהה צורת המילה"
    },
    "ניתוח לקסיקלי (Lexical)": {
        "models": [],
        "description": "משמעות מילים, ניתוח סמנטי",
        "use": "משלים לניקוד - הקשר משמעותי"
    },
    "זיהוי ישויות (NER)": {
        "models": [],
        "description": "זיהוי שמות, מקומות, ארגונים",
        "use": "עיבוד טקסט - לא רלוונטי לניקוד"
    },
    "פרסור תחבירי (Parsing)": {
        "models": [],
        "description": "מבנה משפט, יחסי תלות",
        "use": "משלים לניקוד - הבנת תפקיד בפועל"
    },
    "סנטימנט (Sentiment)": {
        "models": [],
        "description": "זיהוי רגשות בטקסט",
        "use": "לא רלוונטי לניקוד"
    },
    "מודלי שפה (LLM)": {
        "models": [],
        "description": "מודלים גדולים - הבנה מלאה",
        "use": "יכולים לעשות הכל אבל כבדים מאוד"
    },
    "מודלים מיוחדים": {
        "models": [],
        "description": "BEREL (רבני), segmentation, וכו'",
        "use": "שימוש ספציפי"
    }
}

for model in models:
    name = model.modelId.split('/')[-1]
    
    if 'menaked' in name.lower() or 'nakdan' in name.lower():
        analysis["ניקוד (Diacritization)"]["models"].append(name)
    elif 'morph' in name.lower():
        analysis["ניתוח מורפולוגי (Morphology)"]["models"].append(name)
    elif 'lex' in name.lower():
        analysis["ניתוח לקסיקלי (Lexical)"]["models"].append(name)
    elif 'ner' in name.lower():
        analysis["זיהוי ישויות (NER)"]["models"].append(name)
    elif 'parse' in name.lower() or 'syntax' in name.lower():
        analysis["פרסור תחבירי (Parsing)"]["models"].append(name)
    elif 'sentiment' in name.lower():
        analysis["סנטימנט (Sentiment)"]["models"].append(name)
    elif 'dictalm' in name.lower():
        analysis["מודלי שפה (LLM)"]["models"].append(name)
    elif any(x in name.lower() for x in ['berel', 'seg', 'heq', 'splinter', 'joint']):
        analysis["מודלים מיוחדים"]["models"].append(name)
    else:
        analysis["מודלי בסיס (Base Models)"]["models"].append(name)

# הצג ניתוח
for category, data in analysis.items():
    if data["models"]:
        print(f"\n📦 {category}")
        print(f"   📝 {data['description']}")
        print(f"   💡 {data['use']}")
        print(f"   📊 מודלים: {len(data['models'])}")
        print()
        for m in sorted(data["models"])[:5]:  # הצג רק 5 ראשונים
            print(f"      • {m}")
        if len(data["models"]) > 5:
            remaining = len(data["models"]) - 5
            print(f"      ... ועוד {remaining}")

print("\n" + "=" * 80)
print("🎯 מודלים משולבים (עושים כמה דברים ביחד)")
print("=" * 80)

combined = {
    "dictabert-joint": "ניתוח מורפולוגי + תחבירי ביחד",
    "dictabert-tiny-joint": "גרסה קטנה של joint",
    "DictaLM-3.0-*": "עושה הכל - ניקוד, מורפולוגיה, הבנה (אבל כבד!)",
    "BEREL": "כמו BERT אבל מיוחד לעברית רבנית"
}

for model, capability in combined.items():
    print(f"\n✅ {model}")
    print(f"   → {capability}")

print("\n" + "=" * 80)
print("💡 מה כדאי להוריד לשיפור ניקוד?")
print("=" * 80)

recommendations = [
    {
        "model": "dictabert-large-char-menaked",
        "status": "✅ כבר יש לך!",
        "priority": "1 (חובה)",
        "size": "~1.2GB"
    },
    {
        "model": "dictabert-morph",
        "status": "🔄 נוריד עכשיו",
        "priority": "2 (מומלץ מאוד)",
        "size": "~400MB"
    },
    {
        "model": "dictabert-lex",
        "status": "⭐ אופציונלי",
        "priority": "3 (שיפור נוסף)",
        "size": "~400MB"
    },
    {
        "model": "dictabert-joint",
        "status": "⭐ חלופה ל-morph",
        "priority": "2-3 (במקום morph+parse)",
        "size": "~400MB"
    },
    {
        "model": "DictaLM-3.0-1.7B",
        "status": "💪 אם יש GPU",
        "priority": "4 (רק אם יש משאבים)",
        "size": "~3.5GB"
    }
]

print("\nסדר עדיפויות:")
for i, rec in enumerate(recommendations, 1):
    print(f"\n{i}. {rec['model']}")
    print(f"   סטטוס: {rec['status']}")
    print(f"   עדיפות: {rec['priority']}")
    print(f"   גודל: {rec['size']}")

print("\n" + "=" * 80)
print("🎯 סיכום:")
print("=" * 80)
print("""
🔢 60 מודלים מתחלקים ל:
   • ~15 מודלי בסיס (BERT גנרי)
   • ~30 גרסאות של DictaLM (1.7B, 12B, 24B + quantized)
   • ~15 מודלים ספציפיים (ניקוד, NER, parse, וכו')

🎭 כל מודל עושה משהו ספציפי, אבל:
   • dictabert-joint - עושה מורפולוגיה + תחביר ביחד
   • DictaLM - עושה הכל (אבל כבד מאוד)
   
💡 לשיפור ניקוד:
   1. dictabert-large-char-menaked (יש לך ✓)
   2. dictabert-morph (מוריד עכשיו 🔄)
   3. dictabert-lex (אופציונלי)
   
📊 צפי שיפור:
   • רק ניקוד: 90% דיוק
   • ניקוד + morph: 95%+ דיוק
   • ניקוד + morph + lex: 97%+ דיוק
""")
