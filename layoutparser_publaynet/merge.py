#!/usr/bin/env python3
"""
סקריפט איחוד חלקים למודל שלם
"""
import os
import glob
import yaml
from pathlib import Path

def merge_model():
    # קריאת config
    with open('config.yml') as f:
        config = yaml.safe_load(f)
    
    model_name = config['model_name']
    file_ext = config['file_extension']
    output_file = f"model_final.{file_ext}"
    
    print(f"🔄 מאחד {config['parts_count']} חלקים...")
    
    # מציאת כל החלקים
    parts = sorted(glob.glob(f"model_final.{file_ext}.*.part"))
    
    if not parts:
        print("❌ לא נמצאו חלקים!")
        return False
    
    print(f"   נמצאו {len(parts)} חלקים")
    
    # איחוד
    with open(output_file, 'wb') as outfile:
        for i, part in enumerate(parts, 1):
            print(f"   מאחד חלק {i}/{len(parts)}: {part}")
            with open(part, 'rb') as infile:
                outfile.write(infile.read())
    
    # בדיקת גודל
    final_size = os.path.getsize(output_file)
    expected_size = config['total_size_bytes']
    
    if final_size == expected_size:
        print(f"✅ איחוד הושלם בהצלחה!")
        print(f"   קובץ: {output_file}")
        print(f"   גודל: {final_size / (1024*1024):.1f} MB")
        return True
    else:
        print(f"⚠️  אזהרה: גודל לא תואם!")
        print(f"   צפוי: {expected_size / (1024*1024):.1f} MB")
        print(f"   בפועל: {final_size / (1024*1024):.1f} MB")
        return False

if __name__ == '__main__':
    merge_model()
