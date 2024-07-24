# API KEY를 환경변수로 관리하기 위한 설정 파일
# 설치: pip install python-dotenv
from dotenv import load_dotenv

from langchain_teddynote import logging
from langchain_openai import ChatOpenAI
from langchain_teddynote.models import MultiModal
from langchain_teddynote.messages import stream_response
import os

from langchain_teddynote.messages import stream_response  # 스트리밍 출력
from langchain_core.prompts import PromptTemplate


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

# template 정의
template = "{country}의 수도는 어디인가요?"

# from_template 메소드를 이용하여 PromptTemplate 객체 생성
prompt_template = PromptTemplate.from_template(template)

# prompt 생성
prompt = prompt_template.format(country="대한민국")

from langchain_openai import ChatOpenAI

model = ChatOpenAI(
    model="gpt-4o-mini",
    max_tokens=2048,
    temperature=0.1,
)

from langchain_core.output_parsers import StrOutputParser

output_parser = StrOutputParser()


chain = prompt | model | output_parser

input = {"topic": "인공지능 모델의 학습 원리"}

# 스트리밍 출력을 위한 요청
answer = chain.stream(input)
# 스트리밍 출력
stream_response(answer)
