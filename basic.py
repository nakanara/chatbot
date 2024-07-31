# API KEY를 환경변수로 관리하기 위한 설정 파일
# 설치: pip install python-dotenv
from dotenv import load_dotenv 
import os

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.globals import set_llm_cache
from langchain.cache import InMemoryCache
from langchain_community.cache import SQLiteCache
from langchain_core.globals import set_llm_cache

from langchain_teddynote import logging
from langchain_teddynote.models import MultiModal
from langchain_teddynote.messages import stream_response
from langchain_teddynote.messages import stream_response  # 스트리밍 출력


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