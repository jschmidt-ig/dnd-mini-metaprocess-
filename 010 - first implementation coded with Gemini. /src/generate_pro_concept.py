from google import genai
from PIL import Image, ImageDraw, ImageFont
import os

# Setup
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
output_dir = "capri_imageconcepts"

# Define the "Pro" Concept
concept = {
    "name": "Pro_Winged_Heroine",
    "description": "Balanced 'pretty' and 'heroic' 4-color AMS strategy.",
    "colors": ["#F5F5DC", "#D4AF37", "#F5C396", "#4169E1"], # Beige (Bone), Gold, Skin, Royal Blue
    "color_names": ["Bone/White", "Silk Gold", "Skin Tone", "Royal Blue"]
}

def create_swatch(concept):
    img = Image.new('RGB', (400, 500), color='white')
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.load_default()
    except:
        font = None

    draw.text((10, 10), f"Theme: {concept['name']}", fill='black', font=font)
    draw.text((10, 30), "Pro Strategy: Heroic & Pretty", fill='gray', font=font)
    
    y_start = 60
    height = 100
    
    for i, color_hex in enumerate(concept['colors']):
        shape = [(10, y_start + i*height), (390, y_start + (i+1)*height - 5)]
        draw.rectangle(shape, fill=color_hex, outline="black")
        label = f"{concept['color_names'][i]} ({color_hex})"
        
        # Determine text color based on background brightness
        # Simple heuristic: if R+G+B > 500, use black, else white
        r, g, b = Image.new('RGB', (1,1), color_hex).getpixel((0,0))
        text_fill = "black" if (r+g+b) > 400 else "white"
        
        draw.text((20, y_start + i*height + 10), label, fill=text_fill, stroke_fill="black", stroke_width=0)

    filename = os.path.join(output_dir, f"{concept['name']}_palette.png")
    img.save(filename)
    print(f"Generated palette: {filename}")

create_swatch(concept)

# Attempt Render with specific "safe" prompt
prompt = "A high quality studio photo of a generic 3D printed female figurine with wings. The figurine is painted in four specific colors: white wings, gold armor, beige skin, and a blue cape. White background. No weapons."

print("Attempting to generate Pro concept render...")
try:
    response = client.models.generate_content(
        model='gemini-2.0-flash-exp-image-generation',
        contents=prompt
    )
    if response.candidates and response.candidates[0].content.parts:
        found_image = False
        for i, part in enumerate(response.candidates[0].content.parts):
            if part.inline_data:
                with open(os.path.join(output_dir, "Pro_Winged_Heroine_Render.png"), "wb") as f:
                    f.write(part.inline_data.data)
                print("Success! Generated Pro concept render.")
                found_image = True
        if not found_image:
             print("Model returned text:", response.text)
except Exception as e:
    print(f"Render generation failed: {e}")
