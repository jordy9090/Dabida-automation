# modules/video_converter.py (새 파일)
import cv2
import numpy as np
from pathlib import Path

def convert_to_916(input_path, output_path=None):
    """비디오를 9:16 비율로 변환"""
    cap = cv2.VideoCapture(input_path)
    
    # 원본 정보
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # 9:16 비율 계산
    target_width = 1080
    target_height = 1920
    
    if output_path is None:
        output_path = str(Path(input_path).parent / f"converted_916_{Path(input_path).name}")
    
    # VideoWriter 설정
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (target_width, target_height))
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # 크기 조정 및 패딩
        h, w = frame.shape[:2]
        scale = min(target_width/w, target_height/h)
        
        new_w = int(w * scale)
        new_h = int(h * scale)
        
        # 리사이즈
        resized = cv2.resize(frame, (new_w, new_h))
        
        # 검은색 패딩 추가
        canvas = np.zeros((target_height, target_width, 3), dtype=np.uint8)
        y_offset = (target_height - new_h) // 2
        x_offset = (target_width - new_w) // 2
        canvas[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = resized
        
        out.write(canvas)
    
    cap.release()
    out.release()
    
    return output_path