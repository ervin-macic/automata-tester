import os
import re

from dotenv import load_dotenv

from google import genai
from google.genai import types

from constants import DFA_example_json, NFA_example_json

def clean_json_fences(text: str) -> str:
    """
    Remove markdown-style JSON fences (```json ... ``` or ``` ... ```)
    and trim whitespace.
    """
    # Regex removes code fences, optional 'json' label, and trailing backticks
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip(), flags=re.DOTALL)
    return cleaned.strip()

def automata_img_to_json(file_name, automata_type):
    load_dotenv()
    key = os.getenv("automata")

    with open(f'{automata_type}_examples/{file_name}', 'rb') as f:
        image_bytes = f.read()

    example = DFA_example_json if automata_type == "dfa" else NFA_example_json

    # Prompt Gemini to make a JSON abstraction of the automata from the image
    client = genai.Client()
    response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[
        types.Part.from_bytes(
        data=image_bytes,
        mime_type='image/png',
        ),
        f'''Here is an example {example} turned into json:
        For the given image, create similar json and your whole response should just be the json like above. 
        Do not add any text or respond to my prompt. Please do not add ```json fences or comments of any kind. 
        Make sure there are no ```json fences. The alphabet is always just 0 and 1.''']
    )

    with open("temporary_automata_config.json", "w") as f:
        cleaned_text = clean_json_fences(response.text)
        f.write(cleaned_text)