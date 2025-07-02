#!/usr/bin/env python3
"""
에크만 수송 시각화 시스템 실행 스크립트
Ekman Transport Visualization System Runner
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def check_python_version():
    """Python 버전 확인"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 이상이 필요합니다.")
        print(f"현재 버전: {sys.version}")
        return False
    print(f"✅ Python 버전 확인: {sys.version.split()[0]}")
    return True

def install_requirements():
    """필요한 패키지 설치"""
    print("📦 필요한 패키지를 설치합니다...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ 패키지 설치 완료")
        return True
    except subprocess.CalledProcessError:
        print("❌ 패키지 설치 실패")
        return False

def check_requirements():
    """requirements.txt 파일 존재 확인"""
    if not Path("requirements.txt").exists():
        print("❌ requirements.txt 파일을 찾을 수 없습니다.")
        return False
    return True

def run_application():
    """애플리케이션 실행"""
    print("🚀 에크만 수송 시각화 시스템을 시작합니다...")
    
    # Flask 앱 실행
    try:
        from app import app
        print("✅ Flask 애플리케이션이 성공적으로 로드되었습니다.")
        print("🌐 웹 브라우저에서 http://localhost:5000 으로 접속하세요.")
        print("⏹️  종료하려면 Ctrl+C를 누르세요.")
        
        # 3초 후 브라우저 자동 열기
        time.sleep(3)
        webbrowser.open('http://localhost:5000')
        
        # 개발 모드로 실행
        app.run(debug=True, host='0.0.0.0', port=5000)
        
    except ImportError as e:
        print(f"❌ 모듈 임포트 오류: {e}")
        print("requirements.txt의 패키지들이 제대로 설치되었는지 확인하세요.")
        return False
    except Exception as e:
        print(f"❌ 애플리케이션 실행 오류: {e}")
        return False

def main():
    """메인 함수"""
    print("=" * 60)
    print("🌊 에크만 수송 시각화 시스템")
    print("Ekman Transport Visualization System")
    print("=" * 60)
    
    # 1. Python 버전 확인
    if not check_python_version():
        return
    
    # 2. requirements.txt 확인
    if not check_requirements():
        return
    
    # 3. 패키지 설치 (필요시)
    install_choice = input("📦 필요한 패키지를 설치하시겠습니까? (y/n): ").lower().strip()
    if install_choice in ['y', 'yes', '예']:
        if not install_requirements():
            return
    
    # 4. 애플리케이션 실행
    run_application()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 애플리케이션이 종료되었습니다.")
    except Exception as e:
        print(f"\n❌ 예상치 못한 오류가 발생했습니다: {e}")
        print("문제가 지속되면 README.md를 참고하거나 이슈를 생성해주세요.") 