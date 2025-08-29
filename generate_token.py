"""
YouTube OAuth 토큰 생성 스크립트
로컬에서 실행 → token.pickle 생성...
"""

import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

def generate_youtube_token():
    """YouTube OAuth 토큰 생성"""
    
    SCOPES = ['https://www.googleapis.com/auth/youtube.upload',
              'https://www.googleapis.com/auth/youtube.readonly']
    
    creds = None
    token_file = 'token.pickle'
    
    # 기존 토큰이 있으면 삭제 (새로 생성)
    if os.path.exists(token_file):
        print("기존 토큰 파일 발견. 새로 생성합니다...")
        os.remove(token_file)
    
    # client_secret.json 파일 확인
    if not os.path.exists('client_secret.json'):
        print("❌ client_secret.json 파일이 없습니다!")
        print("Google Cloud Console에서 다운로드한 OAuth 2.0 클라이언트 파일을 ")
        print("이 스크립트와 같은 폴더에 'client_secret.json'으로 저장하세요.")
        return False
    
    # OAuth 인증 플로우 시작
    print("\n🔐 OAuth 인증을 시작합니다...")
    print("브라우저가 자동으로 열립니다.")
    print("Google 계정으로 로그인하고 권한을 허용해주세요.\n")
    
    try:
        flow = InstalledAppFlow.from_client_secrets_file(
            'client_secret.json', SCOPES)
        
        # 로컬 서버 실행 (브라우저 자동 열림)
        creds = flow.run_local_server(
            port=8080,  # 또는 0 (자동 할당)
            prompt='consent',  # 항상 동의 화면 표시
            success_message='인증 완료! 이 창을 닫고 터미널로 돌아가세요.'
        )
        
        # 토큰 저장
        with open(token_file, 'wb') as token:
            pickle.dump(creds, token)
        
        print("\n✅ 토큰 생성 완료!")
        print(f"📁 파일 위치: {os.path.abspath(token_file)}")
        
        # 연결 테스트
        youtube = build('youtube', 'v3', credentials=creds)
        
        # 채널 정보 확인
        request = youtube.channels().list(
            part='snippet',
            mine=True
        )
        response = request.execute()
        
        if response['items']:
            channel_name = response['items'][0]['snippet']['title']
            print(f"\n✅ YouTube 채널 연결 확인: {channel_name}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        return False

if __name__ == "__main__":
    print("="*50)
    print("YouTube OAuth 토큰 생성기")
    print("="*50)
    
    if generate_youtube_token():
        print("\n" + "="*50)
        print("🎉 성공! 이제 token.pickle을 Colab에 업로드하세요.")
        print("="*50)
    else:

        print("\n토큰 생성 실패. 오류를 확인하세요.")
