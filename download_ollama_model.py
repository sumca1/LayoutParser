#!/usr/bin/env python3
"""
🤖 Ollama Model Downloader via GitHub Actions + git
מערכת להורדת מודלי Ollama דרך GitHub Actions עם git sparse-checkout
"""

import os
import sys
import subprocess
import time
from pathlib import Path
from typing import Optional
import requests
import json
from datetime import datetime

class OllamaModelDownloader:
    """מוריד מודלי Ollama דרך GitHub Actions + git"""
    
    def __init__(self, github_token: str, repo: str = "sumca1/ollama-models"):
        self.token = github_token
        self.repo = repo
        self.headers = {
            'Authorization': f'token {github_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        self.base_url = f"https://api.github.com/repos/{repo}"
        
    def trigger_download(self, model_name: str, chunk_size_mb: int = 1900) -> Optional[int]:
        """
        מפעיל GitHub Actions workflow להורדת מודל
        
        Args:
            model_name: שם המודל (למשל: llama3.1:8b)
            chunk_size_mb: גודל chunk במגה-בתים (ברירת מחדל: 1900)
            
        Returns:
            run_id של הworkflow או None אם נכשל
        """
        workflow_url = f"{self.base_url}/actions/workflows/download-ollama-model.yml/dispatches"
        
        payload = {
            'ref': 'main',
            'inputs': {
                'model_name': model_name,
                'chunk_size_mb': str(chunk_size_mb)
            }
        }
        
        print(f"🚀 מפעיל הורדת {model_name} ב-GitHub Actions...")
        response = requests.post(workflow_url, headers=self.headers, json=payload)
        
        if response.status_code == 204:
            print(f"✅ Workflow הופעל בהצלחה!")
            # נסה למצוא את ה-run_id
            time.sleep(5)  # המתן שהworkflow יתחיל
            return self._find_latest_run()
        else:
            print(f"❌ שגיאה בהפעלת workflow: {response.status_code}")
            print(response.text)
            return None
            
    def _find_latest_run(self) -> Optional[int]:
        """מוצא את ה-run האחרון"""
        runs_url = f"{self.base_url}/actions/runs"
        response = requests.get(runs_url, headers=self.headers)
        
        if response.status_code == 200:
            runs = response.json().get('workflow_runs', [])
            if runs:
                return runs[0]['id']
        return None
        
    def wait_for_completion(self, run_id: int, timeout: int = 3600) -> bool:
        """
        ממתין לסיום הworkflow
        
        Args:
            run_id: מזהה הריצה
            timeout: זמן המתנה מקסימלי בשניות
            
        Returns:
            True אם הצליח, False אם נכשל או timeout
        """
        run_url = f"{self.base_url}/actions/runs/{run_id}"
        start_time = time.time()
        
        print(f"⏳ ממתין לסיום הורדה (timeout: {timeout//60} דקות)...")
        
        while time.time() - start_time < timeout:
            response = requests.get(run_url, headers=self.headers)
            
            if response.status_code != 200:
                print(f"❌ שגיאה בבדיקת סטטוס: {response.status_code}")
                return False
                
            run = response.json()
            status = run['status']
            conclusion = run.get('conclusion')
            
            elapsed = int(time.time() - start_time)
            print(f"📊 סטטוס: {status} | זמן: {elapsed//60}:{elapsed%60:02d}", end='\r')
            
            if status == 'completed':
                print(f"\n{'✅' if conclusion == 'success' else '❌'} Workflow הסתיים: {conclusion}")
                return conclusion == 'success'
                
            time.sleep(30)  # בדיקה כל 30 שניות
            
        print(f"\n⏰ Timeout - הworkflow לא הסתיים תוך {timeout//60} דקות")
        return False
        
    def download_via_git(self, model_name: str, output_dir: str = ".") -> bool:
        """
        מוריד את המודל מ-GitHub דרך git sparse-checkout
        
        Args:
            model_name: שם המודל (בדיוק כמו שהועלה)
            output_dir: תיקיית יעד
            
        Returns:
            True אם הצליח
        """
        model_folder = model_name.replace(':', '_')  # llama3.1:8b -> llama3.1_8b
        output_path = Path(output_dir) / model_folder
        
        print(f"\n📥 מוריד {model_name} דרך git sparse-checkout...")
        
        try:
            # יצירת תיקייה זמנית
            temp_repo = Path(output_dir) / f"temp_ollama_repo_{int(time.time())}"
            temp_repo.mkdir(exist_ok=True, parents=True)
            
            # Clone עם sparse-checkout
            print(f"🔧 מתחיל git clone...")
            subprocess.run([
                'git', 'clone',
                '--depth', '1',
                '--filter=blob:none',
                '--sparse',
                f'https://{self.token}@github.com/{self.repo}.git',
                str(temp_repo)
            ], check=True, capture_output=True)
            
            # הגדרת sparse-checkout
            print(f"🎯 מגדיר sparse-checkout ל-{model_folder}...")
            subprocess.run([
                'git', '-C', str(temp_repo),
                'sparse-checkout', 'set', model_folder
            ], check=True, capture_output=True)
            
            # העברת הקבצים
            model_source = temp_repo / model_folder
            if model_source.exists():
                print(f"📦 מעתיק קבצים...")
                import shutil
                if output_path.exists():
                    shutil.rmtree(output_path)
                shutil.copytree(model_source, output_path)
                print(f"✅ הקבצים הועתקו ל-{output_path}")
                
                # ניקוי
                print(f"🧹 מנקה קבצים זמניים...")
                try:
                    shutil.rmtree(temp_repo)
                except:
                    print(f"⚠️  לא הצליח למחוק {temp_repo} - תוכל למחוק ידנית")
                
                return True
            else:
                print(f"❌ לא נמצאה תיקייה: {model_source}")
                return False
                
        except subprocess.CalledProcessError as e:
            print(f"❌ שגיאת git: {e}")
            if e.stderr:
                print(f"stderr: {e.stderr.decode()}")
            return False
        except Exception as e:
            print(f"❌ שגיאה: {e}")
            return False
            
    def install_to_ollama(self, model_dir: str, model_name: str) -> bool:
        """
        מתקין את המודל ב-Ollama
        
        Args:
            model_dir: תיקיית המודל שהורד
            model_name: שם המודל (llama3.1:8b)
            
        Returns:
            True אם הצליח
        """
        model_path = Path(model_dir)
        
        # בדיקה אם צריך reassemble
        parts = list(model_path.glob("part_*"))
        if parts:
            print(f"🔧 מזהה {len(parts)} מקטעים - מאחד...")
            output_file = model_path / "models.tar.gz"
            
            # איחוד
            with open(output_file, 'wb') as outfile:
                for part in sorted(parts):
                    print(f"  📎 {part.name}")
                    with open(part, 'rb') as infile:
                        outfile.write(infile.read())
            
            print(f"✅ אוחד ל-{output_file}")
        else:
            output_file = model_path / "models.tar.gz"
            if not output_file.exists():
                print(f"❌ לא נמצא קובץ models.tar.gz")
                return False
        
        # חילוץ ל-Ollama
        ollama_dir = Path.home() / ".ollama"
        print(f"📦 מחלץ ל-{ollama_dir}...")
        
        try:
            import tarfile
            with tarfile.open(output_file, 'r:gz') as tar:
                tar.extractall(ollama_dir)
            
            print(f"✅ המודל הותקן!")
            
            # בדיקה
            print(f"\n🧪 בודק את המודל...")
            result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
            if model_name in result.stdout:
                print(f"✅ {model_name} מותקן ומוכן לשימוש!")
                return True
            else:
                print(f"⚠️  המודל הותקן אבל לא מופיע ברשימה")
                print(f"נסה: ollama run {model_name}")
                return False
                
        except Exception as e:
            print(f"❌ שגיאה בהתקנה: {e}")
            return False
            
    def download_and_install(self, model_name: str, wait: bool = True) -> bool:
        """
        תהליך מלא: הפעלת הורדה + המתנה + הורדה + התקנה
        
        Args:
            model_name: שם המודל (llama3.1:8b)
            wait: האם לחכות לסיום או לחזור מיד
            
        Returns:
            True אם הכל הצליח
        """
        print(f"\n{'='*70}")
        print(f"🤖 מתחיל הורדת {model_name}")
        print(f"{'='*70}\n")
        
        # שלב 1: הפעלת workflow
        run_id = self.trigger_download(model_name)
        if not run_id:
            print("❌ נכשל בהפעלת workflow")
            return False
            
        if not wait:
            print(f"✅ Workflow הופעל (run_id: {run_id})")
            print(f"הרץ שוב עם wait=True כשהworkflow יסתיים")
            return True
            
        # שלב 2: המתנה לסיום
        if not self.wait_for_completion(run_id):
            print("❌ Workflow נכשל או timeout")
            return False
            
        # שלב 3: הורדה דרך git
        if not self.download_via_git(model_name):
            print("❌ נכשל בהורדה מGitHub")
            return False
            
        # שלב 4: התקנה
        model_folder = model_name.replace(':', '_')
        if not self.install_to_ollama(model_folder, model_name):
            print("❌ נכשל בהתקנה")
            return False
            
        print(f"\n{'='*70}")
        print(f"🎉 {model_name} הותקן בהצלחה!")
        print(f"{'='*70}\n")
        print(f"נסה: ollama run {model_name}")
        
        return True


def main():
    """פונקציה ראשית"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='🤖 הורדת מודלי Ollama דרך GitHub Actions + git'
    )
    parser.add_argument('model', help='שם המודל (למשל: llama3.1:8b)')
    parser.add_argument('--token', default=os.getenv('GITHUB_TOKEN'),
                       help='GitHub token (או משתנה GITHUB_TOKEN)')
    parser.add_argument('--repo', default='sumca1/ollama-models',
                       help='שם הrepository')
    parser.add_argument('--no-wait', action='store_true',
                       help='אל תחכה לסיום הworkflow')
    parser.add_argument('--chunk-size', type=int, default=1900,
                       help='גודל chunk במגה-בתים')
    
    args = parser.parse_args()
    
    if not args.token:
        print("❌ חסר GitHub token!")
        print("הגדר: $env:GITHUB_TOKEN='your_token'")
        print("או העבר: --token your_token")
        sys.exit(1)
        
    downloader = OllamaModelDownloader(args.token, args.repo)
    success = downloader.download_and_install(args.model, wait=not args.no_wait)
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
