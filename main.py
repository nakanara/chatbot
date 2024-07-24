# API KEY를 환경변수로 관리하기 위한 설정 파일
# 설치: pip install python-dotenv
from dotenv import load_dotenv

# API KEY 정보로드
load_dotenv()

import os

print(f"[API OPENAI_API_KEY] {os.environ['OPENAI_API_KEY']}")

print(f"[API LANGCHAIN_TRACING_V2] {os.environ['LANGCHAIN_TRACING_V2']}")
print(f"[API LANGCHAIN_ENDPOINT] {os.environ['LANGCHAIN_ENDPOINT']}")
print(f"[API LANGCHAIN_PROJECT] {os.environ['LANGCHAIN_PROJECT']}")
print(f"[API LANGCHAIN_API_KEY] {os.environ['LANGCHAIN_API_KEY']}")


from langchain_teddynote import logging

# 프로젝트 이름을 입력합니다.
logging.langsmith("SETG Service Desk")

# set_enable=False 로 지정하면 추적을 하지 않습니다.
logging.langsmith("SETG Service Desk", set_enable=False)

from langchain_openai import ChatOpenAI

# 객체 생성
llm = ChatOpenAI(
    temperature=0.1,  # 창의성 (0.0 ~ 2.0)
    max_tokens=2048,  # 최대 토큰수
    model_name="gpt-4o-mini",  # 모델명
).bind(logprobs=True)

# 질의내용
question = "대한민국의 수도는 어디인가요?"

# 질의
## print(f"[답변]: {llm.invoke(question)}")

# 스트림 방식으로 질의
# answer 에 스트리밍 답변의 결과를 받습니다.
## answer = llm.stream("대한민국의 아름다운 관광지 10곳과 주소를 알려주세요!")
# 스트리밍 방식으로 각 토큰을 출력합니다. (실시간 출력)
## for token in answer:
##    print(token.content, end="", flush=True)


# 스트림 방식
"""
from langchain_teddynote.messages import stream_response

# 스트림 방식으로 질의
# answer 에 스트리밍 답변의 결과를 받습니다.
answer = llm.stream("대한민국의 아름다운 관광지 10곳과 주소를 알려주세요!")
stream_response(answer)
"""

## 이미지 인식
from langchain_teddynote.models import MultiModal
from langchain_teddynote.messages import stream_response

# 객체 생성
llm = ChatOpenAI(
    temperature=0.1,  # 창의성 (0.0 ~ 2.0)
    max_tokens=2048,  # 최대 토큰수
    model_name="gpt-4o",  # 모델명
)

# 멀티모달 객체 생성
multimodal_llm = MultiModal(llm)


# 샘플 이미지 주소(웹사이트로 부터 바로 인식)
IMAGE_URL = "https://t3.ftcdn.net/jpg/03/77/33/96/360_F_377339633_Rtv9I77sSmSNcev8bEcnVxTHrXB4nRJ5.jpg"

# 이미지 파일로 부터 질의
answer = multimodal_llm.stream(IMAGE_URL)
# 스트리밍 방식으로 각 토큰을 출력합니다. (실시간 출력)
stream_response(answer)

"""
로컬 이미지를 로드하여 분석
"""

# 로컬 PC 에 저장되어 있는 이미지의 경로 입력
#IMAGE_PATH_FROM_FILE = "./images/sample-image.png"

# 이미지 파일로 부터 질의(스트림 방식)
#answer = multimodal_llm.stream(IMAGE_PATH_FROM_FILE)
# 스트리밍 방식으로 각 토큰을 출력합니다. (실시간 출력)
#stream_response(answer)
