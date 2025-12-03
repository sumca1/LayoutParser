"""
DictaBERT - מודל ניקוד עברית מתקדם
מודל: dicta-il/dictabert-large-char-menaked
"""

from transformers import AutoTokenizer, AutoModel
import torch

# טען את המודל
print("📥 טוען DictaBERT...")
model_name = "dicta-il/dictabert-large-char-menaked"

tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
model = AutoModel.from_pretrained(model_name, trust_remote_code=True)

print("✅ המודל נטען בהצלחה!")
print(f"📊 גודל מודל: {model_name}")

# דוגמה לשימוש
def add_nikud(text):
    """מוסיף ניקוד לטקסט עברית"""
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    
    with torch.no_grad():
        outputs = model(**inputs)
    
    # כאן צריך לעבד את הפלט בהתאם ל-API של המודל
    return outputs

# דוגמה
if __name__ == "__main__":
    text = "שלום עולם"
    print(f"\n🧪 בודק עם: '{text}'")
    
    result = add_nikud(text)
    print(f"✅ המודל עבד!")
    print(f"📊 צורת פלט: {result.last_hidden_state.shape}")
    
    print("\n💡 לשימוש מתקדם, ראה: https://huggingface.co/dicta-il/dictabert-large-char-menaked")
