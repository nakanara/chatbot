from dotenv import load_dotenv 
import os
import re
from langchain.llms import OpenAI, ChatOpenAI  # 수정된 import 경로
from langchain.llms import LLMChain
from langchain.prompts import PromptTemplate
from sklearn.feature_extraction.text import TfidfVectorizer  # TF-IDF를 이용한 키워드 추출

# API KEY 정보로드
load_dotenv()

print(f"[API OPENAI_API_KEY] {os.environ['OPENAI_API_KEY']}")
print(f"[API LANGCHAIN_TRACING_V2] {os.environ['LANGCHAIN_TRACING_V2']}")
print(f"[API LANGCHAIN_ENDPOINT] {os.environ['LANGCHAIN_ENDPOINT']}")
print(f"[API LANGCHAIN_PROJECT] {os.environ['LANGCHAIN_PROJECT']}")
print(f"[API LANGCHAIN_API_KEY] {os.environ['LANGCHAIN_API_KEY']}")

OPENAI_API_KEY = os.environ['OPENAI_API_KEY']

# LLM 모델 및 프롬프트 설정
llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=OPENAI_API_KEY)

prompt_template = PromptTemplate(
    input_variables=["user_input", "history"],
    template="다음은 사용자와의 대화 기록입니다.\n{history}\n사용자: {user_input}\n챗봇:"
)
llm_chain = LLMChain(llm=llm, prompt=prompt_template)

def get_user_command(user_input):
    # 특정 커맨드를 추출하는 정규 표현식
    command_pattern = r"^(나의|해야할)일"
    match = re.search(command_pattern, user_input)
    if match:
        return match.group()
    return None

def generate_response(user_input, history):
    try:
        response = llm_chain.run(user_input=user_input, history=history)
    except Exception as e:
        print(f"오류 발생: {e}")
        return "죄송합니다, 현재 요청을 처리할 수 없습니다. 다시 시도해주세요."

    # 키워드 추출 및 커맨드 매칭
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([response])
    keywords = vectorizer.get_feature_names_out()[tfidf_matrix.argsort(1)[:, -5:][0]]

    # 커맨드별 처리
    if "나의할일" in keywords:
        return "나의 할 일을 알려드릴게요. (구체적인 기능 구현 필요)"
    elif "해야할일" in keywords:
        return "해야 할 일을 알려드릴게요. (구체적인 기능 구현 필요)"
    else:
        return response

# 예제 실행
if __name__ == "__main__":
    questions = [
        "API를 통해 데이터를 요청하고 싶습니다.",
        "안녕하세요",
        "업무 시간이 어떻게 되나요?",
        "연락처를 알고 싶어요",
        "이해할 수 없는 질문"
    ]

    history = ""
    for question in questions:
        history += f"사용자: {question}\n챗봇: "
        response = generate_response(question, history)
        print(f"챗봇: {response}")
        history += f"{response}\n"
