# =====================================
# modules/content_generator.py 수정 부분
# =====================================

"""
ChatGPT를 사용한 콘텐츠 생성 모듈
"""
import os
import json
from openai import OpenAI
from datetime import datetime
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

class ContentGenerator:
    def __init__(self, api_key=None):
        """OpenAI API 초기화"""
        # api_key 파라미터가 없으면 환경변수에서 읽기
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        
        if not self.api_key:
            raise ValueError(
                "OpenAI API 키가 없습니다!\n"
                ".env 파일에 OPENAI_API_KEY=sk-... 형식으로 추가하세요."
            )
        
        # API 키 유효성 간단 체크
        if not self.api_key.startswith('sk-'):
            raise ValueError("잘못된 OpenAI API 키 형식입니다.")
        
        try:
            self.client = OpenAI(api_key=self.api_key)
            self.model = "gpt-4o"  # 또는 "gpt-3.5-turbo" (저렴)
            print("✅ OpenAI API 연결 성공!")
        except Exception as e:
            raise Exception(f"OpenAI 클라이언트 초기화 실패: {e}")
    def generate_script(self, keyword, style="cinematic"):
        """
        지니티처 광고용 VEO3 프롬프트 생성
        
        Args:
            keyword: 광고 테마 키워드
            style: 영상 스타일 (cinematic/minimalist/futuristic)
        
        Returns:
            dict: VEO3용 상세 프롬프트 JSON
        """
        
        # 스타일별 무드 설정
        style_moods = {
            "cinematic": "premium educational transformation, elegant confidence",
            "minimalist": "clean, focused learning environment, pure simplicity",
            "futuristic": "next-generation education, innovative breakthrough"
        }
        
        system_prompt = """You are a cinematic advertising director specializing in luxury brand storytelling.
Create detailed VEO3 video generation prompts for GenITeacher (지니티처), a premium AI-powered educational service.
Follow the exact JSON structure provided in the examples, focusing on visual storytelling without text overlays.
The service transforms traditional education into personalized, intelligent learning experiences."""

        # 예시 프롬프트들을 참고용으로 포함
        example_prompts = """
REFERENCE STRUCTURE (Tesla/Moët/Rolex examples):
- Scene environment with detailed lighting and mood
- Subject focus with specific object descriptions
- Camera work with precise movements
- Sound design with ambient and focus effects
- Motion descriptions for all elements
- No text overlays (brand visibility through objects only)
"""

        user_prompt = f"""
Create a premium 8-second VEO3 video prompt for GenITeacher (지니티처) educational service.

Theme: {keyword}
Style: {style_moods.get(style, "premium educational transformation")}

Requirements:
1. NO TEXT OVERLAYS - visual storytelling only
2. Focus on transformation/reveal concept (like the examples)
3. Include specific camera movements, lighting, and sound design
4. Make it feel premium and cinematic
5. Educational elements should feel magical/futuristic

Create a JSON prompt following this EXACT structure:

{{
  "prompt_name": "GenITeacher – [Creative Title Related to {keyword}]",
  "version": 1.0,
  "target_ai_model": "VEO3",
  "core_concept": "[8-second transformation story showing educational evolution]",
  "details": {{
    "scene_environment": {{
      "setting": "[specific location description]",
      "lighting": "[detailed lighting setup]",
      "mood": "{style_moods.get(style, 'premium educational transformation')}",
      "features": "[environmental details]"
    }},
    "subject_focus": {{
      "object": "[main focus object - tablet/hologram/book transforming]",
      "description": "[detailed visual description]",
      "placement": "[exact positioning]",
      "action": "[transformation sequence]"
    }},
    "elements": [
      "[list of visual elements that appear]",
      "floating knowledge particles",
      "holographic displays",
      "AI visualization elements"
    ],
    "action_sequence": [
      {{
        "step": 1,
        "duration": "0-2s",
        "description": "[opening shot description]"
      }},
      {{
        "step": 2,
        "duration": "2-5s",
        "description": "[transformation moment]"
      }},
      {{
        "step": 3,
        "duration": "5-7s",
        "description": "[reveal of educational magic]"
      }},
      {{
        "step": 4,
        "duration": "7-8s",
        "description": "[final elegant frame]"
      }}
    ],
    "camera_work": {{
      "movement": "[specific camera movements]",
      "lens": "[lens type and focal length]",
      "frame": "[framing details]"
    }},
    "lighting": {{
      "style": "[lighting style]",
      "highlights": "[key light points]",
      "color_palette": "soft blues, warm whites, subtle gold accents"
    }},
    "motion": {{
      "[element_name]": "[specific motion description]"
    }},
    "sound_design": {{
      "ambient": [
        "[background sound 1]",
        "[background sound 2]"
      ],
      "focus_fx": [
        {{
          "sound": "[specific sound effect]",
          "timing": "[when it occurs]",
          "style": "[sound characteristic]"
        }}
      ],
      "music": "none"
    }},
    "final_frame": {{
      "composition": "[final shot description]",
      "visual_overlay": "none",
      "brand_element": "subtle GenITeacher logo glow on device/hologram"
    }},
    "aspect_ratio": "9:16",
    "style": "cinematic, premium educational, {style}",
    "color_grading": "cool blues with warm accent highlights"
  }}
}}

Make it as detailed as the Tesla/Moët/Rolex examples. Focus on:
- Traditional textbook transforming into holographic knowledge
- Student's desk evolving into futuristic learning space
- AI particles forming educational visualizations
- Knowledge flowing like liquid light
"""
        
        try:
            # ChatGPT API 호출
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.8,
                max_tokens=2500,
                response_format={"type": "json_object"}
            )
            
            # 응답 파싱
            script_json = json.loads(response.choices[0].message.content)
            
            # 메타데이터 추가
            script_json['service'] = 'GenITeacher'
            script_json['keyword'] = keyword
            script_json['generated_at'] = datetime.now().isoformat()
            script_json['style'] = style
            script_json['duration'] = "8 seconds"
            
            # 한국어 설명 추가 (GUI 표시용)
            script_json['korean_summary'] = self._generate_korean_summary(script_json)
            
            print(f"✅ VEO3 프롬프트 생성 완료: {script_json['prompt_name']}")
            
            return script_json
            
        except Exception as e:
            print(f"❌ 프롬프트 생성 실패: {e}")
            return None
    
    def _generate_korean_summary(self, script_json):
        """생성된 프롬프트의 한국어 요약 생성"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "인스타그램 릴스 캡션용: 영상 프롬프트를 간단한 한국어로 요약하세요."},
                    {"role": "user", "content": f"다음 영상의 핵심을 2-3문장으로 요약: {script_json['core_concept']}"}
                ],
                temperature=0.3,
                max_tokens=200
            )
            return response.choices[0].message.content
        except:
            return "지니티처의 혁신적인 교육 서비스를 보여주는 프리미엄 광고 영상"
    
    def generate_variations(self, base_keyword, count=3):
        """하나의 키워드로 여러 변형 생성"""
        variations = []
        styles = ["cinematic", "minimalist", "futuristic"]
        
        for i in range(min(count, len(styles))):
            script = self.generate_script(base_keyword, styles[i])
            if script:
                variations.append(script)
        
        return variations
    
    def save_script(self, script, filename=None):
        """스크립트를 파일로 저장"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            keyword_clean = script.get('keyword', 'script').replace(' ', '_')
            filename = f"veo3_prompt_{keyword_clean}_{timestamp}.json"
        
        filepath = os.path.join('data', 'scripts', filename)
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(script, f, ensure_ascii=False, indent=2)
        
        print(f"📁 VEO3 프롬프트 저장: {filepath}")
        return filepath
    
    def get_sample_themes(self):
        """지니티처에 적합한 샘플 테마 제공"""
        return [
            "AI-Powered Personalized Learning",
            "Knowledge Transformation",
            "Future of Education",
            "Smart Learning Revolution",
            "Intelligent Tutoring System",
            "Educational Innovation",
            "Digital Learning Evolution",
            "Adaptive Education Technology"
        ]
    
    def test_connection(self):
        """API 연결 테스트"""
        try:
            response = self.client.models.list()
            print("✅ OpenAI API 연결 정상")
            return True
        except Exception as e:
            print(f"❌ OpenAI API 연결 실패: {e}")
            return False

# 사용 예시
if __name__ == "__main__":
    generator = ContentGenerator()
    
    # 샘플 생성
    script = generator.generate_script(
        keyword="AI-Powered Learning Transformation",
        style="cinematic"
    )
    
    if script:
        print(json.dumps(script, ensure_ascii=False, indent=2))
        generator.save_script(script)