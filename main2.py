# API KEY를 환경변수로 관리하기 위한 설정 파일
# 설치: pip install python-dotenv
from dotenv import load_dotenv

from langchain_teddynote import logging
from langchain_openai import ChatOpenAI
from langchain_teddynote.models import MultiModal
from langchain_teddynote.messages import stream_response
import os


# API KEY 정보로드
load_dotenv()


print(f"[API OPENAI_API_KEY] {os.environ['OPENAI_API_KEY']}")

print(f"[API LANGCHAIN_TRACING_V2] {os.environ['LANGCHAIN_TRACING_V2']}")
print(f"[API LANGCHAIN_ENDPOINT] {os.environ['LANGCHAIN_ENDPOINT']}")
print(f"[API LANGCHAIN_PROJECT] {os.environ['LANGCHAIN_PROJECT']}")
print(f"[API LANGCHAIN_API_KEY] {os.environ['LANGCHAIN_API_KEY']}")

# 프로젝트 이름을 입력합니다.
logging.langsmith("SETG Service Desk")

# set_enable=False 로 지정하면 추적을 하지 않습니다.
logging.langsmith("SETG Service Desk", set_enable=False)

# 객체 생성
llm = ChatOpenAI(
    temperature=0.1,  # 창의성 (0.0 ~ 2.0)
    max_tokens=2048,  # 최대 토큰수
    model_name="gpt-4o-mini",  # 모델명
).bind(logprobs=True)


system_prompt = """당신은 표(재무제표) 를 해석하는 금융 AI 어시스턴트 입니다. 
당신의 임무는 주어진 테이블 형식의 재무제표를 바탕으로 흥미로운 사실을 정리하여 친절하게 답변하는 것입니다."""

user_prompt = """당신에게 주어진 표는 회사의 재무제표 입니다. 흥미로운 사실을 정리하여 답변하세요."""

# 멀티모달 객체 생성
multimodal_llm_with_prompt = MultiModal(
    llm, system_prompt=system_prompt, user_prompt=user_prompt
)

# 로컬 PC 에 저장되어 있는 이미지의 경로 입력
IMAGE_PATH_FROM_FILE = "https://storage.googleapis.com/static.fastcampus.co.kr/prod/uploads/202212/080345-661/kwon-01.png"

# 이미지 파일로 부터 질의(스트림 방식)
answer = multimodal_llm_with_prompt.stream(IMAGE_PATH_FROM_FILE)

# 스트리밍 방식으로 각 토큰을 출력합니다. (실시간 출력)
stream_response(answer)
