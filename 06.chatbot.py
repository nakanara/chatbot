from dotenv import load_dotenv 
import os
import openai
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

# API KEY 정보로드
load_dotenv()


print(f"[API OPENAI_API_KEY] {os.environ['OPENAI_API_KEY']}")

print(f"[API LANGCHAIN_TRACING_V2] {os.environ['LANGCHAIN_TRACING_V2']}")
print(f"[API LANGCHAIN_ENDPOINT] {os.environ['LANGCHAIN_ENDPOINT']}")
print(f"[API LANGCHAIN_PROJECT] {os.environ['LANGCHAIN_PROJECT']}")
print(f"[API LANGCHAIN_API_KEY] {os.environ['LANGCHAIN_API_KEY']}")


# OpenAI API 키 설정
openai.api_key = f"{os.environ['OPENAI_API_KEY']}"

# 사전 답변 매뉴얼 설정
predefined_answers = {
    "인사": "안녕하세요! 무엇을 도와드릴까요?",
    "업무 시간": "저희의 업무 시간은 월요일부터 금요일까지 오전 9시부터 오후 6시까지입니다.",
    "연락처": "저희의 연락처는 123-456-7890입니다. 이메일은 info@example.com입니다."
}

# 질문 유형 판단 함수
def classify_question(question):
    keywords = {
        "API 요청": ["API", "연동", "데이터", "요청"],
        "일반 질문": ["인사", "업무 시간", "연락처"]
    }
    
    for key, words in keywords.items():
        if any(word in question for word in words):
            return key
    
    return "기타"

# ChatGPT를 이용한 답변 생성 함수
def generate_response(question):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": question}
        ],
        max_tokens=150
    )
    return response.choices[0].message["content"].strip()

# 메인 챗봇 함수
def chatbot(question):
    # 질문 유형 판단
    question_type = classify_question(question)
    
    # 사전 답변이 있는 경우 해당 답변 반환
    if question_type == "일반 질문":
        for key, answer in predefined_answers.items():
            if key in question:
                return answer
    
    # API 요청 유형일 경우 ChatGPT를 이용하여 답변 생성
    if question_type == "API 요청":
        return generate_response(question)
    
    # 기타 질문에 대해서는 기본 답변 반환
    return "죄송합니다. 질문을 이해하지 못했습니다. 다시 시도해 주세요."

# 예제 실행
if __name__ == "__main__":
    questions = [
        "API를 통해 데이터를 요청하고 싶습니다.",
        "안녕하세요",
        "업무 시간이 어떻게 되나요?",
        "연락처를 알고 싶어요",
        "이해할 수 없는 질문"
    ]
    
    for question in questions:
        print(f"질문: {question}")
        print(f"답변: {chatbot(question)}\n")
