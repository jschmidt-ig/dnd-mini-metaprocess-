from google import genai
import os

api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
output_dir = "Capri_concepts2"

prompt = "Digital concept painting of a majestic winged angel woman standing with a white wolf. She wears gold armor and a royal blue cape. Her skin is beige. High fantasy art style, detailed, cinematic lighting, white background."

print(f"Attempting to generate AI concept with prompt: {prompt}")

try:
    # Try the flash-exp-image-generation model again with this specific fantasy prompt
    response = client.models.generate_content(
        model='gemini-2.0-flash-exp-image-generation',
        contents=prompt
    )
    
    if response.candidates and response.candidates[0].content.parts:
        for i, part in enumerate(response.candidates[0].content.parts):
            if part.inline_data:
                filename = os.path.join(output_dir, "AI_Winged_Heroine_Concept.png")
                with open(filename, "wb") as f:
                    f.write(part.inline_data.data)
                print(f"Success! Generated {filename}")
            else:
                print("Model returned text:", response.text)
except Exception as e:
    print(f"Generation failed: {e}")
