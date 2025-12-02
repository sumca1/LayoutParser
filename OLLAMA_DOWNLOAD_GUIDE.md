# 🤖 הורדת מודלי Ollama דרך GitHub Actions + git

## 🎯 הבעיה שפתרנו

המערכת של Ollama **לא תעבוד** אצלך כי:
- GitHub Actions Artifacts נחסמים ע"י NetFree
- צריך להוריד דרך UI של GitHub
- זה לא דרך git!

**הפתרון שלנו:**
- GitHub Actions מוריד מ-Ollama Registry
- שומר את המודל ב-**repository עצמו** (commit + push)
- אנחנו מורידים דרך **git sparse-checkout** (עובד!)

---

## 📋 דרישות מקדימות

1. **Repository ב-GitHub** (כבר קיים: `sumca1/LayoutParser`)
2. **GitHub Token** עם הרשאות:
   - `repo` - גישה לrepository
   - `workflow` - הרצת Actions
3. **Ollama מותקן** במחשב:
   ```powershell
   winget install Ollama.Ollama
   ```

---

## 🚀 שימוש מהיר

### שיטה 1: דרך Python (אוטומטי מלא)

```powershell
# הגדר את הtoken
$env:GITHUB_TOKEN = "ghp_YOUR_TOKEN_HERE"

# הורד והתקן מודל
python download_ollama_model.py llama3.1:8b
```

**זה יעשה הכל אוטומטית:**
1. יפעיל GitHub Actions workflow
2. יחכה שהworkflow יסיים (10-15 דקות)
3. יוריד את המודל דרך git sparse-checkout
4. יאחד את המקטעים (אם צריך)
5. יתקין ב-Ollama

### שיטה 2: ידני (צעד צעד)

#### שלב 1: הפעל הורדה ב-GitHub

1. גש ל: https://github.com/sumca1/LayoutParser/actions
2. בחר **"Download Ollama Model"**
3. לחץ **"Run workflow"**
4. בחר מודל: `llama3.1:8b`
5. לחץ **"Run workflow"** (הכפתור הירוק)

#### שלב 2: המתן לסיום (10-15 דקות)

עקוב אחרי הלוג:
```
✅ Install Ollama
✅ Start Ollama service  
📥 Downloading llama3.1:8b...
✅ Download complete!
📦 Exporting...
✅ Uploaded to repository!
```

#### שלב 3: הורד דרך git

```powershell
cd I:\OCR_Arabic_Testing\BiblIA_dataset-project\BiblIA_dataset\NEW_SPLIT_VIEW_FEATURE

# הורד רק את תיקיית המודל
git clone --depth 1 --filter=blob:none --sparse https://github.com/sumca1/LayoutParser.git temp_ollama
cd temp_ollama
git sparse-checkout set llama3.1_8b
```

#### שלב 4: התקן את המודל

אם יש מקטעים:
```powershell
cd llama3.1_8b
.\reassemble.ps1
tar -xzf models.tar.gz -C $env:USERPROFILE\.ollama\
```

אם קובץ אחד:
```powershell
cd llama3.1_8b
tar -xzf models.tar.gz -C $env:USERPROFILE\.ollama\
```

#### שלב 5: בדיקה

```powershell
ollama list
ollama run llama3.1:8b "שלום עולם!"
```

---

## 📦 מודלים זמינים

| מודל | גודל | זמן הורדה | תיאור |
|------|------|-----------|--------|
| **llama3.1:8b** | ~4.9GB | 10-15 דקות | מומלץ להתחלה |
| llama3.1:70b | ~40GB | 1-2 שעות | מודל גדול |
| mistral:7b | ~4.1GB | 8-12 דקות | מהיר וטוב |
| codellama:7b | ~3.8GB | 8-10 דקות | לקוד |
| qwen2.5:3b | ~2.0GB | 5-8 דקות | קטן ומהיר |

---

## 🔧 אפשרויות מתקדמות

### שינוי גודל chunks

```powershell
# chunks של 500MB (לחיבור איטי)
python download_ollama_model.py llama3.1:8b --chunk-size 500

# chunks של 3000MB (לא יפצל מודלים קטנים)
python download_ollama_model.py llama3.1:8b --chunk-size 3000
```

### הפעלה ללא המתנה

```powershell
# רק תפעיל את הworkflow ותחזור
python download_ollama_model.py llama3.1:8b --no-wait

# אחר כך, כשהworkflow יסיים:
python download_ollama_model.py llama3.1:8b
```

### repository אחר

```powershell
python download_ollama_model.py llama3.1:8b --repo YOUR_USERNAME/your-repo
```

---

## 🛠️ פתרון בעיות

### שגיאה: "חסר GitHub token"

```powershell
$env:GITHUB_TOKEN = "ghp_YOUR_TOKEN_HERE"
```

או:
```powershell
python download_ollama_model.py llama3.1:8b --token ghp_YOUR_TOKEN_HERE
```

### שגיאה: "git command not found"

התקן Git:
```powershell
winget install Git.Git
```

### שגיאה: "Ollama not found"

התקן Ollama:
```powershell
winget install Ollama.Ollama
```

### המודל לא מופיע ב-`ollama list`

נסה להריץ:
```powershell
ollama run llama3.1:8b
```

Ollama יזהה את המודל ויוסיף אותו לרשימה.

---

## 📊 השוואה למערכות אחרות

| מערכת | Artifacts? | git? | עובד ב-NetFree? |
|-------|-----------|------|----------------|
| **Ollama original** | ✅ | ❌ | ❌ (Artifacts חסומים) |
| **LayoutParser (קודם)** | ❌ | ✅ | ✅ |
| **המערכת שלנו** | ❌ | ✅ | ✅ |

**היתרון:** משתמשים ב-**commit + push** במקום Artifacts!

---

## 🎯 דוגמאות שימוש

### דוגמה 1: שאלה בעברית

```powershell
ollama run llama3.1:8b "מה הבירה של ישראל?"
```

### דוגמה 2: יצירת קוד

```powershell
ollama run llama3.1:8b "כתוב פונקציה Python שמחשבת פיבונאצי"
```

### דוגמה 3: תרגום

```powershell
ollama run llama3.1:8b "תרגם לעברית: Hello world, how are you?"
```

---

## 🔄 הורדת מודלים נוספים

פשוט הרץ שוב עם מודל אחר:

```powershell
python download_ollama_model.py mistral:7b
python download_ollama_model.py codellama:7b
python download_ollama_model.py qwen2.5:3b
```

כל מודל יישמר בתיקייה נפרדת ב-repository.

---

## 💡 טיפים

1. **התחל ממודל קטן** - `qwen2.5:3b` (2GB) או `llama3.1:8b` (4.9GB)
2. **אל תסגור את הטרמינל** במהלך ההורדה
3. **בדוק שיש מקום פנוי** - לפחות פי 2 מגודל המודל
4. **השתמש ב-`--no-wait`** אם אתה רוצה להמשיך לעבוד בינתיים

---

## 🎉 סיכום

המערכת מאפשרת:
- ✅ הורדת מודלי Ollama **דרך GitHub Actions**
- ✅ עקיפת חסימות NetFree דרך **git sparse-checkout**
- ✅ פיצול אוטומטי לchunks (עד 1.9GB כל אחד)
- ✅ התקנה אוטומטית ב-Ollama
- ✅ תמיכה במודלים ענקיים (עד 100GB+)

**זמן כולל:** ~15-20 דקות למודל של 5GB 🚀
