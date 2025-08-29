
import os
import sys
from pathlib import Path

# 프로젝트 루트 설정
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.append(str(PROJECT_ROOT))

# GUI 앱 임포트 및 실행
from gui.app import create_interface

if __name__ == "__main__":
    demo = create_interface()
    demo.launch()
