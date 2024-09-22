import os
import sys
import base64
import requests
from io import BytesIO
from PIL import Image
from googletrans import Translator

module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)

# Function to encode the image
def encode_image(imageURL):
    # URL에서 이미지 다운로드
    response = requests.get(imageURL)
    image_data = response.content

    # 이미지 데이터를 PIL Image로 열기
    image = Image.open(BytesIO(image_data))

    # Buffer to hold the image data in bytes
    buffered = BytesIO()
    image.save(buffered, format="JPEG")  # Assuming the image format is JPEG
    encoded_image = base64.b64encode(buffered.getvalue()).decode('utf-8')

    return encoded_image

# 챗피지티 사용
def generate_text_response(imageURL, user_msg):
    api_key = os.getenv("OPENAI_API_KEY")

    base64_image = encode_image(imageURL)
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": "You are a photo editor. You can only do color pop, replace, blur operation for each object in the image, and remove background of the selected object."
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": user_msg
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    try:
        response_json = response.json()
        english_response = response_json['choices'][0]['message']['content']
        
        korean_response = translate_to_korean(english_response)
        return korean_response

    except KeyError as e:
        return f"An error occurred: {str(e)}"
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"

# 한글 번역
def translate_to_korean(text):
    translator = Translator()
    try:
        translated = translator.translate(text, dest='ko')
        return translated.text
    except Exception as e:
        return f"Translation error: {str(e)}"

# 이미지 수정
def exe_imageEdit(imageURL, chat, interpreter, generator):

    response = requests.get(imageURL)
    image_data = response.content

    image = Image.open(BytesIO(image_data))

    image.thumbnail((640, 640), Image.Resampling.LANCZOS)
    
    init_state = dict(
        IMAGE=image.convert('RGB')
    )

    instruction = chat
    prog, _ = generator.generate(instruction)
    result, prog_state, html_str = interpreter.execute(prog, init_state, inspect=True)
    
    return result

def imageHandler(imageURL, chat, interpreter=None, generator=None):
    
    photo_editing_commands = ["colorpop", "replace", "blur", "remove", "pop", "select", "change"]

    if any(command in chat.lower() for command in photo_editing_commands):
        return exe_imageEdit(imageURL, chat, interpreter, generator)
    else:
        return generate_text_response(imageURL, chat)
