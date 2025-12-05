"""
פייפליין ניקוד מלא עם הכרעה אוטומטית
מערכת המשלבת Nakdimon + DictaBERT + מורפולוגיה
"""

import sys
from pathlib import Path

# הוסף encoding UTF-8
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


class HebrewNikudPipeline:
    """
    פייפליין מלא לניקוד עברי עם הכרעה חכמה
    """
    
    def __init__(self):
        self.dictabert_nikud = None
        self.nakdimon = None
        self.morph_model = None
        self.abbreviations_dict = {}
        
    def load_models(self):
        """טוען את כל המודלים הנדרשים"""
        print("=" * 70)
        print("טוען מודלים...")
        print("=" * 70)
        
        # 1. טען DictaBERT-nikud
        try:
            from transformers import AutoTokenizer, AutoModel
            
            nikud_path = "./downloaded_models/dictabert-nikud"
            if not Path(nikud_path).exists():
                nikud_path = "dicta-il/dictabert-nikud"
            
            print(f"\n1. טוען DictaBERT-nikud...")
            self.dictabert_nikud = {
                'tokenizer': AutoTokenizer.from_pretrained(nikud_path),
                'model': AutoModel.from_pretrained(nikud_path, trust_remote_code=True)
            }
            self.dictabert_nikud['model'].eval()
            print("   ✓ DictaBERT-nikud נטען")
            
        except Exception as e:
            print(f"   ✗ שגיאה בטעינת DictaBERT-nikud: {e}")
        
        # 2. טען Nakdimon (אופציונלי)
        try:
            print("\n2. טוען Nakdimon...")
            from nakdimon import Nakdimon
            self.nakdimon = Nakdimon()
            print("   ✓ Nakdimon נטען")
        except Exception as e:
            print(f"   ✗ Nakdimon לא זמין: {e}")
        
        # 3. טען DictaBERT-morph למורפולוגיה
        try:
            morph_path = "./downloaded_models/dictabert-morph"
            if not Path(morph_path).exists():
                morph_path = "dicta-il/dictabert-morph"
            
            print(f"\n3. טוען DictaBERT-morph...")
            self.morph_model = {
                'tokenizer': AutoTokenizer.from_pretrained(morph_path),
                'model': AutoModel.from_pretrained(morph_path, trust_remote_code=True)
            }
            self.morph_model['model'].eval()
            print("   ✓ DictaBERT-morph נטען")
            
        except Exception as e:
            print(f"   ✗ שגיאה בטעינת Morph: {e}")
        
        # 4. טען מילון קיצורים
        try:
            print("\n4. טוען מילון קיצורים...")
            abbrev_file = Path("simple_abbreviations_dict.py")
            if abbrev_file.exists():
                import importlib.util
                spec = importlib.util.spec_from_file_location("abbrev_dict", abbrev_file)
                abbrev_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(abbrev_module)
                self.abbreviations_dict = abbrev_module.ABBREVIATIONS
                print(f"   ✓ מילון עם {len(self.abbreviations_dict)} קיצורים")
            else:
                print("   ✗ קובץ מילון לא נמצא")
        except Exception as e:
            print(f"   ✗ שגיאה בטעינת מילון: {e}")
        
        print("\n" + "=" * 70)
        print("סיום טעינה")
        print("=" * 70)
    
    def get_morphology(self, sentence):
        """מנתח מורפולוגיה של משפט"""
        if not self.morph_model:
            return None
        
        try:
            result = self.morph_model['model'].predict(
                [sentence], 
                self.morph_model['tokenizer']
            )
            return result[0] if result else None
        except Exception as e:
            print(f"שגיאה בניתוח מורפולוגי: {e}")
            return None
    
    def nikud_with_dictabert(self, text):
        """מנקד עם DictaBERT"""
        if not self.dictabert_nikud:
            return None
        
        try:
            result = self.dictabert_nikud['model'].predict(
                [text],
                self.dictabert_nikud['tokenizer']
            )
            return result[0] if result else None
        except Exception as e:
            print(f"שגיאה בניקוד DictaBERT: {e}")
            return None
    
    def nikud_with_nakdimon(self, text):
        """מנקד עם Nakdimon"""
        if not self.nakdimon:
            return None
        
        try:
            return self.nakdimon.nakdan(text)
        except Exception as e:
            print(f"שגיאה בניקוד Nakdimon: {e}")
            return None
    
    def decide_nikud(self, text, dictabert_result, nakdimon_result):
        """
        מכריע בין DictaBERT ל-Nakdimon
        
        לוגיקה:
        1. אם אין הבדל -> החזר DictaBERT
        2. אם יש הבדל:
           a. בדוק מורפולוגיה
           b. אם המורפולוגיה ברורה -> סמוך על DictaBERT
           c. אם יש ספק -> הצג למשתמש
        """
        # אם אין Nakdimon, החזר DictaBERT
        if not nakdimon_result:
            return {
                'text': dictabert_result,
                'source': 'DictaBERT',
                'confidence': 'high',
                'notes': 'Nakdimon לא זמין'
            }
        
        # אם אין הבדל
        if dictabert_result == nakdimon_result:
            return {
                'text': dictabert_result,
                'source': 'Both (identical)',
                'confidence': 'very_high',
                'notes': 'שני המודלים מסכימים'
            }
        
        # יש הבדל - נבדוק מורפולוגיה
        morph = self.get_morphology(text)
        
        if morph:
            # אם המורפולוגיה ברורה (למשל, יש POS ברור לכל מילה)
            tokens = morph.get('tokens', [])
            unclear_tokens = [t for t in tokens if not t.get('pos')]
            
            if len(unclear_tokens) == 0:
                # המורפולוגיה ברורה -> סמוך על DictaBERT
                return {
                    'text': dictabert_result,
                    'source': 'DictaBERT (with morph)',
                    'confidence': 'high',
                    'notes': 'מורפולוגיה ברורה, DictaBERT אמין יותר',
                    'alternative': nakdimon_result
                }
            else:
                # יש ספק -> הצג שתי אפשרויות
                return {
                    'text': dictabert_result,
                    'source': 'DictaBERT (uncertain)',
                    'confidence': 'medium',
                    'notes': f'יש {len(unclear_tokens)} מילים לא ברורות',
                    'alternative': nakdimon_result,
                    'requires_review': True
                }
        else:
            # אין מורפולוגיה - העדף DictaBERT אבל סמן לבדיקה
            return {
                'text': dictabert_result,
                'source': 'DictaBERT (no morph)',
                'confidence': 'medium',
                'notes': 'לא ניתן לנתח מורפולוגיה',
                'alternative': nakdimon_result,
                'requires_review': True
            }
    
    def process(self, text):
        """
        מעבד טקסט מלא:
        1. מנקד עם DictaBERT
        2. מנקד עם Nakdimon
        3. מכריע
        4. מחזיר תוצאה עם ציון ביטחון
        """
        print("\n" + "=" * 70)
        print("מעבד טקסט:")
        print("=" * 70)
        print(f"קלט: {text}")
        print()
        
        # שלב 1: DictaBERT
        print("שלב 1: ניקוד עם DictaBERT...")
        dictabert_result = self.nikud_with_dictabert(text)
        if dictabert_result:
            print(f"   תוצאה: {dictabert_result}")
        
        # שלב 2: Nakdimon
        print("\nשלב 2: ניקוד עם Nakdimon...")
        nakdimon_result = self.nikud_with_nakdimon(text)
        if nakdimon_result:
            print(f"   תוצאה: {nakdimon_result}")
        
        # שלב 3: הכרעה
        print("\nשלב 3: הכרעה...")
        decision = self.decide_nikud(text, dictabert_result, nakdimon_result)
        
        print(f"\n{'=' * 70}")
        print("תוצאה סופית:")
        print(f"{'=' * 70}")
        print(f"טקסט: {decision['text']}")
        print(f"מקור: {decision['source']}")
        print(f"ביטחון: {decision['confidence']}")
        print(f"הערות: {decision['notes']}")
        
        if 'alternative' in decision:
            print(f"\nאלטרנטיבה: {decision['alternative']}")
        
        if decision.get('requires_review'):
            print("\n⚠️  דורש בדיקה ידנית!")
        
        return decision


def main():
    """בדיקה של הפייפליין"""
    
    # צור פייפליין
    pipeline = HebrewNikudPipeline()
    pipeline.load_models()
    
    # משפטי בדיקה
    test_sentences = [
        "לפי שהיה אברהם בטל ביחוד אור אין סוף ב\"ה",
        "על ידי עסק התורה והמצות בכלל",
        "שלום עליכם",
        "ברוך הוא וברוך שמו"
    ]
    
    print("\n\n" + "=" * 70)
    print("בדיקות:")
    print("=" * 70)
    
    for sentence in test_sentences:
        result = pipeline.process(sentence)
        print("\n" + "-" * 70 + "\n")


if __name__ == "__main__":
    main()
