import os
from dotenv import load_dotenv
import time

from fastapi import FastAPI
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse

from google import genai
from io import BytesIO
from PIL import Image

# creating app
app = FastAPI()

# Load any local environment variables
load_dotenv(".env")

# Get the API key from the environment variables
api_key = os.getenv("GEMINI_API_KEY")


# Test API Endpoint
@app.get("/test/")
def first_example():
    return {"message": "Hello, FastAPI!"}

# Analyse Coin Endpoint
# Take two images of the coin, prompt gemini and return a json of the coin data
@app.post("/analyse-coin/")
async def analyse_coin(images: list[UploadFile]):

    prompt = """
    The two images show the obverse and reverse sides of a coin. Please can you analyse the images and populate a JSON object with the following values:
    
    - country: The coins country of origin (string)
    - year: The year the coin was minted (integer)
    - denomination: The name given to a coin of this value (string)
    - materials: A list of up to 3 metals found within the coin, each represented as an object with a material (string) and a percentage (float)
    - estimated_value: The estimated value of the coin in GBP (float)
    - rarity: On a scale from 1 (common) to 10 (extremely rare), how rare is this coin (integer)
    - obverse_image: A very short description of the image on the obverse side of the coin (string) - nullable
    - obverse_text: A transcript of the text on the obverse side of the coin (string) - nullable
    - reverse_image: A very short description of the image on the reverse side of the coin (string) - nullable
    - reverse_text: A transcript of the text on the reverse side of the coin (string) - nullable
    - confidence: On a scale from 0 (not confident) to 100 (certain) how confident are you in your analysis and valuation of this coin (integer)
    - context: A short paragraph explaining the reasoning behind why the coin has been identified and valued in this way. If applicable, mention further steps to prove or disprove the identification (string)
    
    If any of the nullable fields are not relevant, populate the value with null.
    """

    # Read files
    image_bytes_1 = await images[0].read()
    image_bytes_2 = await images[1].read()
    image1 = Image.open(BytesIO(image_bytes_1))
    image2 = Image.open(BytesIO(image_bytes_2))

    # Instantiate the Google Gemini AI client
    client = genai.Client(api_key=api_key)

    # Try multiple times, each time it fails (due to the api being unavailable), wait exponentially longer
    for attempt in range(25):
        try:
            return client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[prompt, image1, image2]
            )
        except Exception as e:
            if "503" in str(e):
                time.sleep(2 ** attempt)
            else:
                raise
    
    return None


# Main endpoint serves a HTML form
@app.get("/")
async def main():
    content = """
<body style="font-family: system-ui, sans-serif;">
<div style="text-align: center">
    <h1>Upload Coin Images</h1>
    <form action="/analyse-coin/" enctype="multipart/form-data" method="post">
        <input name="images" type="file" multiple>
        <input type="submit">
    </form>
</div>
</body>
    """
    return HTMLResponse(content=content)