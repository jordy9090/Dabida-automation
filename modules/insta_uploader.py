# modules/insta_uploader.py 

"""
Instagram Reels 업로드 모듈
"""
import os
import requests
from pathlib import Path

class InstagramUploader:
    def init(self, access_token=None):
        """Instagram Graph API 초기화"""
        self.access_token = access_token or os.getenv('INSTAGRAM_ACCESS_TOKEN')
        self.instagram_account_id = os.getenv('INSTAGRAM_ACCOUNT_ID')

        if not self.access_token:
            raise ValueError("Instagram Access Token이 필요합니다")

        self.base_url = "https://graph.facebook.com/v18.0"
        print("✅ Instagram API 연결 준비")

    def upload_reels(self, video_path, caption="", tags=None):
        """
        Instagram Reels 업로드

        Args:
            video_path: 비디오 파일 경로
            caption: 설명
            tags: 해시태그 리스트

        Returns:
            dict: 업로드 정보
        """
        if tags is None:
            tags = []

        # 해시태그 추가
        hashtags = ' '.join([f'#{tag}' for tag in tags])
        full_caption = f"{caption}\n\n{hashtags}"

        try:
            # 1단계: 비디오 업로드 URL 받기
            container_params = {
                'media_type': 'REELS',
                'video_url': self._upload_video_to_hosting(video_path),
                'caption': full_caption,
                'share_to_feed': True,
                'access_token': self.access_token
            }

            # 미디어 컨테이너 생성
            create_url = f"{self.base_url}/{self.instagram_account_id}/media"
            response = requests.post(create_url, data=container_params)

            if response.status_code != 200:
                raise Exception(f"컨테이너 생성 실패: {response.text}")

            container_id = response.json()['id']

            # 2단계: 게시
            publish_url = f"{self.base_url}/{self.instagram_account_id}/media_publish"
            publish_params = {
                'creation_id': container_id,
                'access_token': self.access_token
            }

            response = requests.post(publish_url, data=publish_params)

            if response.status_code == 200:
                media_id = response.json()['id']
                print(f"✅ Instagram Reels 업로드 완료! ID: {media_id}")

                return {
                    'id': media_id,
                    'url': f"https://www.instagram.com/reel/{media_id}",
                    'caption': caption
                }
            else:
                raise Exception(f"게시 실패: {response.text}")

        except Exception as e:
            print(f"❌ Instagram 업로드 실패: {e}")
            return None

    def _upload_video_to_hosting(self, video_path):
        """
        비디오를 임시 호스팅 서버에 업로드
        Instagram은 URL로만 비디오를 받음
        """
        # 옵션 1: 자체 서버에 업로드
        # 옵션 2: 임시 파일 호스팅 서비스 사용
        # 여기서는 간단한 예시만 제공

        # 실제 구현시 AWS S3, Google Cloud Storage 등 사용
        video_url = f"https://your-server.com/videos/{Path(video_path).name}"

        # 또는 file.io 같은 임시 파일 서비스 사용
        with open(video_path, 'rb') as f:
            response = requests.post('https://file.io', files={'file': f})
            if response.status_code == 200:
                video_url = response.json()['link']

        return video_url

    def test_connection(self):
        """연결 테스트"""
        try:
            url = f"{self.base_url}/{self.instagram_account_id}"
            params = {'access_token': self.access_token}
            response = requests.get(url, params=params)

            if response.status_code == 200:
                account_info = response.json()
                print(f"✅ Instagram 계정: {account_info.get('username')}")
                return True
        except Exception as e:
            print(f"❌ 연결 실패: {e}")
        return False"""