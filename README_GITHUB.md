# LayoutParser Models Collection 🤖

מאגר המכיל את כל מודלי LayoutParser להורדה ישירה (ללא NetFree blocking)

## 🚀 איך זה עובד?

1. **GitHub Actions מוריד אוטומטית** את כל המודלים מהאינטרנט
2. **מפצל קבצים גדולים** ל-95MB (GitHub limit)
3. **מעלה למאגר** - אתה פשוט מוריד!

## 📥 התקנה מהירה

```powershell
# הורד את כל המודלים
git clone https://github.com/sumca1/LayoutParser.git C:\layoutparser_models_all

cd C:\layoutparser_models_all\models

# מזג קבצים מפוצלים (אם יש)
python merge_model_final.py
```

## 📦 מודלים זמינים

| מודל | מחלקות | תיאור | גודל |
|------|---------|-------|------|
| **PubLayNet** | 5 | מאמרים מדעיים (350k+ מסמכים) | ~300MB |
| **PrimaLayout** | 6 | מסמכים היסטוריים מעורבים | ~250MB |
| **NewspaperNavigator** | 7 | עיתונים אמריקאיים (16M עמודים) | ~300MB |
| **TableBank** | 1 | טבלאות (417k+ דוגמאות) | ~400MB |

## 🔧 שימוש בקוד

```python
import layoutparser as lp

# PubLayNet - מאמרים מדעיים
model = lp.Detectron2LayoutModel(
    config_path='C:/layoutparser_models_all/models/publaynet_config.yaml',
    model_path='C:/layoutparser_models_all/models/publaynet_model.pth',
    label_map={0: "Text", 1: "Title", 2: "List", 3: "Table", 4: "Figure"}
)

# PrimaLayout - מסמכים היסטוריים
model = lp.Detectron2LayoutModel(
    config_path='C:/layoutparser_models_all/models/primalayout_config.yaml',
    model_path='C:/layoutparser_models_all/models/primalayout_model.pth',
    label_map={
        1: "TextRegion",
        2: "ImageRegion", 
        3: "TableRegion",
        4: "MathsRegion",
        5: "SeparatorRegion",
        6: "OtherRegion"
    }
)
```

## 🎯 הפעלת GitHub Actions

1. לך ל-**Actions** בדף GitHub
2. בחר **"Download LayoutParser Models"**
3. לחץ **"Run workflow"**
4. המתן ~10-15 דקות
5. המודלים יועלו אוטומטית!

## 📊 סטטיסטיקות

- ✅ **4 מודלים מלאים**
- ✅ **~1.2GB סה"ך**
- ✅ **מוכן לשימוש ישיר**
- ✅ **ללא צורך ב-VPN**

## 🔄 עדכון המודלים

```bash
cd C:\layoutparser_models_all
git pull
```

## 📝 רישיון

מודלים אלו שייכים לפרויקט [LayoutParser](https://github.com/Layout-Parser/layout-parser) תחת רישיון Apache 2.0.

---

**נוצר אוטומטית ע"י GitHub Actions** 🤖
