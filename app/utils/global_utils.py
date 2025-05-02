import re
import requests


def llama_call(prompt):
    model_name = "llama3.2:3b"
    
    OLLAMA_URL = "http://localhost:11434/api/generate"

    payload = {
        "model": "llama3.2:3b",
         "options":{
                "n_batch":256,
                "n_ctx":512,
                "f16_kv":True,
                "num_threads": 8,
                "use_gpu": True ,
                "gpu_layers": 30 
                        },
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)

    response.raise_for_status()  # Raise error for HTTP issues

    output_data=response.json()

    response_text = output_data["response"]
    
    return response_text
    

#Cleaning the unnecessary symbols from the generated text
def clean_and_strip_text(text):
    text = re.sub(r'^\s*```|```\s*$', '', text)
    text = re.sub(r'^\s*(?=\{)', '', text, 1)
    return text

# Removing numbers from the generated text
def remove_numbers(text):
    return re.sub(r'[^a-zA-Z\s]', '', text)