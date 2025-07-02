#!/usr/bin/env python3
"""
Ekman Transport Visualizer - Web Demo Launcher
3가지 웹 버전을 쉽게 실행할 수 있는 통합 런처
"""

import os
import sys
import subprocess
import webbrowser
import time
import threading

def main():
    print("🌊 Ekman Transport Visualizer - Web Demo Launcher")
    print("=" * 50)
    
    print("\n어떤 웹 버전을 실행하시겠습니까?")
    print("1. PyScript - 브라우저에서 직접 Python 실행")
    print("2. Streamlit - 빠르고 아름다운 웹 앱")
    print("3. Flask - 전통적인 웹 애플리케이션")
    print("4. 종료")
    
    choice = input("\n선택하세요 (1-4): ")
    
    if choice == '1':
        print("\n🚀 PyScript 버전 시작 중...")
        if os.path.exists('index_pyscript.html'):
            subprocess.run([sys.executable, '-m', 'http.server', '8000'])
        else:
            print("❌ index_pyscript.html 파일을 찾을 수 없습니다")
            
    elif choice == '2':
        print("\n🚀 Streamlit 버전 시작 중...")
        if os.path.exists('streamlit_app.py'):
            subprocess.run([sys.executable, '-m', 'streamlit', 'run', 'streamlit_app.py'])
        else:
            print("❌ streamlit_app.py 파일을 찾을 수 없습니다")
            
    elif choice == '3':
        print("\n🚀 Flask 버전 시작 중...")
        if os.path.exists('app.py'):
            subprocess.run([sys.executable, 'app.py'])
        else:
            print("❌ app.py 파일을 찾을 수 없습니다")
            
    elif choice == '4':
        print("👋 프로그램을 종료합니다.")
        
    else:
        print("❌ 잘못된 선택입니다.")

if __name__ == "__main__":
    main() 