# API KEY를 환경변수로 관리하기 위한 설정 파일
# 설치: pip install python-dotenv
from dotenv import load_dotenv
import os

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.prompts.chat import ChatMessage, ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.globals import set_llm_cache
from langchain_community.cache import SQLiteCache
from langchain_core.globals import set_llm_cache
from langchain.memory import ConversationBufferMemory
# from langchain.chains import ConversationChain
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.prompts import ChatPromptTemplate

from langchain_teddynote import logging
from langchain_teddynote.models import MultiModal
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

memory = ConversationBufferMemory()

# 프롬프트 템플릿 정의
# 초기 메시지 목록 생성 및 ChatMessage 객체로 변환
initial_messages = [
    ChatMessage(role="system", content="안녕하세요. ITSM의 로코입니다."),
    ChatMessage(role="user", content=""),
    ChatMessage(role="assistant", content="안녕하세요. ITSM의 로코입니다.")
]

# ChatPromptTemplate 생성
prompt_template = ChatPromptTemplate.from_messages(initial_messages)


memory.save_context(
    inputs={
        "user": "안녕하세요, 비대면으로 은행 계좌를 개설하고 싶습니다. 어떻게 시작해야 하나요?"
    },
    outputs={
        "assistant": "안녕하세요! 계좌 개설을 원하신다니 기쁩니다. 먼저, 본인 인증을 위해 신분증을 준비해 주시겠어요?"
    },
)

memory.save_context(
    inputs={"user": "사진을 업로드했습니다. 본인 인증은 어떻게 진행되나요?"},
    outputs={
        "assistant": "업로드해 주신 사진을 확인했습니다. 이제 휴대폰을 통한 본인 인증을 진행해 주세요. 문자로 발송된 인증번호를 입력해 주시면 됩니다."
    },
)
memory.save_context(
    inputs={"user": "인증번호를 입력했습니다. 계좌 개설은 이제 어떻게 하나요?"},
    outputs={
        "assistant": "본인 인증이 완료되었습니다. 이제 원하시는 계좌 종류를 선택하고 필요한 정보를 입력해 주세요. 예금 종류, 통화 종류 등을 선택할 수 있습니다."
    },
)
# 'history' 키에 저장된 대화 기록을 확인합니다.
memory.load_memory_variables({})

print(memory.load_memory_variables({})["history"])

# LLM 모델을 생성합니다.
llm = ChatOpenAI(temperature=0)

# 실행 가능한 객체 래퍼 정의
class LLMWrapper:
    def __init__(self, llm):
        self.llm = llm

    def __call__(self, messages):
        return self.llm.invoke(messages)

    def with_listeners(self, *args, **kwargs):
        # 필요한 경우 비동기 리스너 추가
        return self
    
    def with_alisteners(self, *args, **kwargs):
        # 필요한 경우 비동기 리스너 추가
        return self
    

# LLMWrapper 객체 생성
runnable = LLMWrapper(llm)

# 세션 히스토리를 가져오는 함수 정의
def get_session_history():
    return memory.load_memory_variables({}).get("history", "")

# RunnableWithMessageHistory 객체 생성
runnable_with_history = RunnableWithMessageHistory(
    runnable=runnable,
    get_session_history=get_session_history,
    prompt_template=prompt_template,
    memory=memory
)

# runnable = RunnableWithMessageHistory(llm=llm, prompt_template=prompt_template, memory=memory)


def run_conversation(runnable, user_input):
    messages = [ChatMessage(role="user", content=user_input)]
    response = runnable(messages)
    return response

response = run_conversation(runnable, "안녕하세요, 비대면으로 은행 계좌를 개설하고 싶습니다. 어떻게 시작해야 하나요?")
print(response)

response = run_conversation(runnable, "이전 답변을 불렛포인트 형식으로 정리하여 알려주세요.")
print(response)

response = run_conversation(runnable, "너의 이름은 뭐야?")
print(response)
