"""
DABIDA 자동화 시스템 웹 GUI 모듈 - 수정 버전
"""
import json
import os
import sys
from pathlib import Path
from datetime import datetime, timedelta
from dotenv import load_dotenv
import gradio as gr

# 프로젝트 루트 설정
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

# .env 파일 로드 (중요!)
env_path = PROJECT_ROOT / '.env'
load_dotenv(env_path)

from modules.content_generator import ContentGenerator
from modules.youtube_uploader import YouTubeUploader

class DabidaGUI:
    def __init__(self):
        # 환경변수에서 API 키 읽기
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            print("⚠️ OPENAI_API_KEY가 .env 파일에 없습니다!")
            self.content_gen = None
        else:
            try:
                self.content_gen = ContentGenerator(api_key=api_key)
                print("✅ OpenAI API 연결 성공")
            except Exception as e:
                print(f"❌ OpenAI 연결 실패: {e}")
                self.content_gen = None
        
        # YouTube 토큰 경로 설정
        token_path = PROJECT_ROOT / 'token.pickle'
        try:
            if token_path.exists():
                self.youtube_uploader = YouTubeUploader(str(token_path))
                print("✅ YouTube 연결 성공")
            else:
                print(f"⚠️ token.pickle 파일이 없습니다: {token_path}")
                self.youtube_uploader = None
        except Exception as e:
            print(f"❌ YouTube 연결 실패: {e}")
            self.youtube_uploader = None
        
        self.current_script = None
        self.current_video = None
    
    def generate_script(self, keyword, style):
        if not self.content_gen:
            return None, "❌ OpenAI API가 초기화되지 않았습니다. .env 파일을 확인하세요."
        
        try:
            self.current_script = self.content_gen.generate_script(keyword, style)
            return json.dumps(self.current_script, ensure_ascii=False, indent=2), "✅ 스크립트 생성 완료!"
        except Exception as e:
            return None, f"❌ 스크립트 생성 실패: {str(e)}"
    
    def handle_video_upload(self, file):
        if not file:
            return None, "❌ 파일이 선택되지 않았습니다"
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"uploaded_{timestamp}.mp4"
            filepath = str(PROJECT_ROOT / 'data' / 'videos' / filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            import shutil
            shutil.copy(file, filepath)
            self.current_video = filepath
            
            return filepath, f"✅ 비디오 업로드 완료: {filename}"
        except Exception as e:
            return None, f"❌ 업로드 실패: {str(e)}"
    
    def convert_video_to_916(self):
        """비디오를 9:16 비율로 변환"""
        if not self.current_video:
            return None, "❌ 먼저 비디오를 업로드하세요"
        
        try:
            from modules.video_converter import convert_to_916
            
            output_path = str(PROJECT_ROOT / 'data' / 'videos' / f"converted_916_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4")
            
            # 변환 실행
            converted_path = convert_to_916(self.current_video, output_path)
            self.converted_video = converted_path
            self.current_video = converted_path  # 변환된 걸로 교체
            
            return converted_path, f"✅ 9:16 변환 완료!\n📁 {Path(converted_path).name}"
            
        except ImportError:
            return None, "❌ OpenCV가 설치되지 않았습니다. !pip install opencv-python"
        except Exception as e:
            return None, f"❌ 변환 실패: {str(e)}"  # 따옴표 추가!


def create_interface():
    app = DabidaGUI()
    
    with gr.Blocks(title="DABIDA 숏폼 자동화", theme=gr.themes.Soft()) as demo:
        gr.Markdown("# 🎬 DABIDA 숏폼 자동화 시스템")
        
        with gr.Tab("📝 스크립트 생성"):
            with gr.Row():
                keyword_input = gr.Textbox(label="키워드", placeholder="예: AI 기반 교육 혁신")
                style_select = gr.Dropdown(
                    label="스타일",
                    choices=["cinematic", "minimalist", "futuristic"],
                    value="cinematic"
                )
            
            generate_btn = gr.Button("스크립트 생성", variant="primary")
            chatgpt_btn = gr.Button("🤖 ChatGPT 바로가기 (JSON 수정용)", variant="secondary")
            
            script_display = gr.Code(label="생성된 스크립트", language="json", interactive=True)
            script_status = gr.Textbox(label="상태", interactive=False)
            
            generate_btn.click(app.generate_script, [keyword_input, style_select], [script_display, script_status])
            chatgpt_btn.click(None, js="() => { window.open('https://chat.openai.com', '_blank'); }")
        
        with gr.Tab("🎥 비디오 생성"):
            gr.Markdown("### 옵션 1: Flow에서 AI 비디오 생성")
            
            flow_prompt = gr.Textbox(label="Flow 프롬프트", lines=8, interactive=True)
            with gr.Row():
                generate_prompt_btn = gr.Button("📝 프롬프트 생성")
                copy_btn = gr.Button("📋 복사")
                open_flow_btn = gr.Button("🌐 Flow 열기", variant="primary")
            
            def generate_flow_prompt():
                return json.dumps(app.current_script, ensure_ascii=False, indent=2) if app.current_script else "먼저 스크립트를 생성하세요"
            
            generate_prompt_btn.click(generate_flow_prompt, outputs=flow_prompt)
            copy_btn.click(None, flow_prompt, js="(p) => { navigator.clipboard.writeText(p); alert('복사됨!'); }")
            open_flow_btn.click(None, js="() => { window.open('https://labs.google/fx/ko/tools/flow', '_blank'); }")
            
            gr.Markdown("---")
            gr.Markdown("### 옵션 2: 비디오 파일 업로드")
            
            video_upload = gr.File(label="비디오 파일 선택", file_types=["video"])
            upload_status = gr.Textbox(label="업로드 상태", interactive=False)
            video_preview = gr.Video(label="현재 비디오")
            
            video_upload.upload(app.handle_video_upload, video_upload, [video_preview, upload_status])
            
            gr.Markdown("---")
            gr.Markdown("### 옵션 3: 9:16 크기 변환 (Shorts/Reels용)")
            
            with gr.Row():
                convert_btn = gr.Button("📐 9:16으로 변환", variant="secondary")
                convert_status = gr.Textbox(label="변환 상태", interactive=False)
            
            converted_preview = gr.Video(label="변환된 비디오 (9:16)")
            
            convert_btn.click(
                app.convert_video_to_916,
                outputs=[converted_preview, convert_status]
            )

        with gr.Tab("📤 YouTube 업로드"):
            schedule_checkbox = gr.Checkbox(label="예약 게시", value=False)
            schedule_datetime = gr.Textbox(
                label="게시 시간 (한국 시간)",
                placeholder="2025-01-01 12:00",
                visible=False
            )
            
            upload_btn = gr.Button("YouTube 업로드", variant="primary")
            upload_result = gr.Textbox(label="업로드 결과", lines=3, interactive=False)
            
            schedule_checkbox.change(lambda x: gr.update(visible=x), schedule_checkbox, schedule_datetime)
            
            def upload_to_youtube(use_schedule, schedule_time):
                if not app.current_video:
                    return "❌ 업로드할 비디오가 없습니다"
                if not app.youtube_uploader:
                    return "❌ YouTube API가 초기화되지 않았습니다"
                
                title = app.current_script.get('prompt_name', 'GenITeacher 비디오') if app.current_script else "테스트 비디오"
                description = app.current_script.get('korean_summary', '') if app.current_script else ""
                tags = ['GenITeacher', '지니티처', 'AI교육']
                
                publish_time = None
                if use_schedule and schedule_time:
                    try:
                        dt_kst = datetime.strptime(schedule_time, "%Y-%m-%d %H:%M")
                        dt_utc = dt_kst - timedelta(hours=9)
                        publish_time = dt_utc.strftime('%Y-%m-%dT%H:%M:%S.000Z')
                    except ValueError:
                        return "❌ 날짜 형식 오류 (YYYY-MM-DD HH:MM)"
                
                try:
                    result = app.youtube_uploader.upload_video(
                        app.current_video, title, description, tags, publish_time
                    )
                    status = f"예약됨 ({schedule_time})" if publish_time else "게시됨"
                    return f"✅ {status}!\n🔗 {result['url']}"
                except Exception as e:
                    return f"❌ 업로드 실패: {str(e)}"
            
            upload_btn.click(upload_to_youtube, [schedule_checkbox, schedule_datetime], upload_result)
        
        with gr.Tab("📸 Instagram 업로드"):
            gr.Markdown("### Instagram Reels 업로드")
            
            with gr.Row():
                with gr.Column():
                    insta_caption = gr.Textbox(
                        label="캡션 (자동 생성)",
                        lines=5,
                        interactive=True
                    )
                    with gr.Row():
                        generate_caption_btn = gr.Button("📝 캡션 생성")
                        copy_caption_btn = gr.Button("📋 복사")
                        open_insta_btn = gr.Button("📸 Instagram 열기", variant="primary")
                
                with gr.Column():
                    gr.Markdown("""
                    사용 방법:
                    1. '캡션 생성' 클릭
                    2. '복사' 클릭
                    3. 'Instagram 열기' → 브라우저에서 업로드
                    4. 생성된 비디오 업로드 & 캡션 붙여넣기
                    """)
            
            def generate_instagram_caption():
                if app.current_script:
                    title = app.current_script.get('prompt_name', '지니티처')
                    summary = app.current_script.get('korean_summary', '')
                    caption = f"""
{title}

{summary}

#지니티처 #GenITeacher #AI교육 #교육혁신 #에듀테크
#AITutor #개인화학습 #미래교육 #shorts #reels
"""
                    return caption.strip()
                return "먼저 스크립트를 생성하세요"
            
            generate_caption_btn.click(
                generate_instagram_caption,
                outputs=insta_caption
            )
            
            copy_caption_btn.click(
                None,
                inputs=insta_caption,
                js="""
                (text) => {
                    navigator.clipboard.writeText(text);
                    alert('캡션이 복사되었습니다!');
                }
                """
            )
            
            open_insta_btn.click(
                None,
                js="() => { window.open('https://business.facebook.com/', '_blank'); }"
            )
    
    return demo

if __name__ == "__main__":  # 언더스코어 추가!
    demo = create_interface()
    demo.launch(share=True, debug=True)