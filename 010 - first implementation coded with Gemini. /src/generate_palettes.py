from google import genai
from PIL import Image, ImageDraw, ImageFont
import os
import json

# Setup
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
output_dir = "capri_imageconcepts"

# 1. Define the 4 Concepts (Text)
concepts = [
    {
        "name": "Classic_Hero",
        "description": "Traditional hero palette with noble colors.",
        "colors": ["#0047AB", "#FFD700", "#F5F5F5", "#333333"], # Cobalt Blue, Gold, White, Dark Grey
        "color_names": ["Cobalt Blue", "Gold", "White", "Dark Grey"]
    },
    {
        "name": "Forest_Ranger",
        "description": "Natural camouflage suitable for woodland settings.",
        "colors": ["#228B22", "#8B4513", "#F0E68C", "#1A1A1A"], # Forest Green, Saddle Brown, Khaki, Soft Black
        "color_names": ["Forest Green", "Saddle Brown", "Khaki", "Soft Black"]
    },
    {
        "name": "Arcane_Mystic",
        "description": "Magical aesthetic with high contrast.",
        "colors": ["#4B0082", "#00FFFF", "#C0C0C0", "#191970"], # Indigo, Cyan, Silver, Midnight Blue
        "color_names": ["Indigo", "Cyan", "Silver", "Midnight Blue"]
    },
    {
        "name": "Molten_Warrior",
        "description": "Fiery theme for an aggressive look.",
        "colors": ["#8B0000", "#FF4500", "#FFD700", "#2F4F4F"], # Dark Red, Orange Red, Gold, Dark Slate Gray
        "color_names": ["Dark Red", "Orange Red", "Gold", "Charcoal"]
    }
]

# 2. Generate Swatch Images
def create_swatch(concept):
    # Create a 400x400 image
    img = Image.new('RGB', (400, 500), color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw title
    try:
        # Default font
        font = ImageFont.load_default()
    except:
        font = None

    draw.text((10, 10), f"Theme: {concept['name']}", fill='black', font=font)
    draw.text((10, 30), concept['description'], fill='gray', font=font)
    
    # Draw 4 color bars
    y_start = 60
    height = 100
    
    for i, color_hex in enumerate(concept['colors']):
        # Draw rectangle
        shape = [(10, y_start + i*height), (390, y_start + (i+1)*height - 5)]
        draw.rectangle(shape, fill=color_hex, outline="black")
        # Draw label
        label = f"{concept['color_names'][i]} ({color_hex})"
        # Draw text inside (or next to) the box - contrasting color?
        # Simple hack: draw text in white with black stroke or just top left
        draw.text((20, y_start + i*height + 10), label, fill="white", stroke_fill="black", stroke_width=1)

    filename = os.path.join(output_dir, f"{concept['name']}_palette.png")
    img.save(filename)
    print(f"Generated palette: {filename}")

for c in concepts:
    create_swatch(c)

# 3. Try to generate a 3D Concept Render (with safety-safe prompt)
prompt_safe = "A small toy figurine of a fantasy knight, painted in blue and gold, standing on a white background. Studio lighting. High quality product photo."

print("Attempting to generate render with sanitized prompt...")
try:
    response = client.models.generate_content(
        model='gemini-2.0-flash-exp-image-generation',
        contents=prompt_safe
    )
    if response.candidates and response.candidates[0].content.parts:
        for part in response.candidates[0].content.parts:
            if part.inline_data:
                with open(os.path.join(output_dir, "Classic_Hero_Render_Attempt.png"), "wb") as f:
                    f.write(part.inline_data.data)
                print("Success! Generated concept render.")
            else:
                print("Model returned text instead of image:", response.text)
except Exception as e:
    print(f"Render generation failed: {e}")

