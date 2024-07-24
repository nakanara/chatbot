import fitz  # PyMuPDF
import json

def extract_text_from_pdf(pdf_path):
    # PDF 파일 열기
    document = fitz.open(pdf_path)
    text = ""

    # 각 페이지마다 텍스트 추출
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text += page.get_text()

    return text


def save_text_to_file(data, output_path):
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(data)

def save_text_to_json(data, output_path):
    with open(output_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# 사용 예시
title = 'Entity'
pdf_path = './doc/EGENE DOCUMENT_SLM매니저.pdf'
output_path = './out/SLM매니저.txt'
output_json_path = './out/SLM매니저.json'

extracted_text = extract_text_from_pdf(pdf_path)


#save_text_to_file(extracted_text, output_path);

data = {"title": title, "content": extracted_text}
save_text_to_json(data, output_json_path)
