"""
YouTube 업로드 모듈 - 간결 버전
"""
import os
import pickle
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request

class YouTubeUploader:
    def __init__(self, token_file):
        """토큰 파일로 초기화"""
        self.youtube = None
        self.load_credentials(token_file)
    
    def load_credentials(self, token_file):
        """토큰 로드"""
        if not os.path.exists(token_file):
            raise FileNotFoundError(f"토큰 파일 없음: {token_file}")
        
        with open(token_file, 'rb') as f:
            creds = pickle.load(f)
        
        # 토큰 갱신
        if hasattr(creds, 'expired') and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            with open(token_file, 'wb') as f:
                pickle.dump(creds, f)
        
        self.youtube = build('youtube', 'v3', credentials=creds)
        print("✅ YouTube API 연결 성공")
    
    def upload_video(self, video_path, title, description="", tags=None, schedule_time=None):
        """비디오 업로드"""
        if not tags:
            tags = []
        tags.append("shorts")
        
        body = {
            'snippet': {
                'title': title[:100],
                'description': description[:5000],
                'tags': tags[:500],
                'categoryId': '22'
            },
            'status': {
                'privacyStatus': 'private',
                'selfDeclaredMadeForKids': False
            }
        }
        
        if schedule_time:
            body['status']['publishAt'] = schedule_time
        
        media = MediaFileUpload(video_path, mimetype='video/mp4', resumable=True)
        request = self.youtube.videos().insert(
            part=','.join(body.keys()),
            body=body,
            media_body=media
        )
        
        response = request.execute()
        
        return {
            'id': response['id'],
            'url': f"https://youtube.com/shorts/{response['id']}",
            'title': title
        }