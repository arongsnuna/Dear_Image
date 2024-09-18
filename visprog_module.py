import os
import sys
import base64
import requests
from io import BytesIO
from PIL import Image
from prompts.imgeEdit import PROMPT
from engine.utils import ProgramGenerator, ProgramInterpreter

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

# Function to handle OpenAI text generation
def generate_text_response(imageURL, user_msg):
    api_key = os.getenv("OPENAI_API_KEY")
        
    # Getting the base64 string
    base64_image = encode_image(imageURL)
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    # Adjust the payload structure for better compatibility with the API
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": "You are a photo editor. You can do color pop, replace, blur operation for each object in the image."
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

    # Parse the JSON response and handle errors
    try:
        response_json = response.json()
        return response_json['choices'][0]['message']['content']
    except KeyError as e:
        # Log the actual error message and return it
        return f"An error occurred: {str(e)}"
    except Exception as e:
        # Catch any other potential errors
        return f"An unexpected error occurred: {str(e)}"

# Create a prompt based on the user's instruction
def create_prompt(instruction):
    return PROMPT.format(instruction=instruction)

# Image editing logic with ProgramInterpreter and ProgramGenerator
def exe_imageEdit(imageURL, chat):
    interpreter = ProgramInterpreter(dataset='imageEdit')
    generator = ProgramGenerator(prompter=create_prompt)
    
    # URL에서 이미지 다운로드
    response = requests.get(imageURL)
    image_data = response.content

    # 이미지 데이터를 PIL Image로 열기
    image = Image.open(BytesIO(image_data))

    # Process the image to 640x640 size
    image.thumbnail((640, 640), Image.Resampling.LANCZOS)
    
    init_state = dict(
        IMAGE=image.convert('RGB')
    )

    instruction = chat
    prog, _ = generator.generate(instruction)
    result, prog_state, html_str = interpreter.execute(prog, init_state, inspect=True)
    
    return result

# Main handler function to either process image or generate text response
def imageHandler(imageURL, chat):
    # List of specific commands that trigger image processing
    photo_editing_commands = ["colorpop", "replace", "blur"]

    # Check if the input contains an image editing command
    if any(command in chat.lower() for command in photo_editing_commands):
        return exe_imageEdit(imageURL, chat)
    else:
        return generate_text_response(imageURL, chat)
