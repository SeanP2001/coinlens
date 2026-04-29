import os
import json
import time

from fastapi import FastAPI
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from google import genai
from io import BytesIO
from PIL import Image

# creating app
app = FastAPI()

# Mount the "static" directory at the /static path
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Get the API key from the environment variables
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY is not set")

# Test API Endpoint
@app.get("/test/")
def first_example():
    return {"message": "Hello, FastAPI!"}

# Dummy Endpoint For Testing 
# (Faster and prevents wasting tokens)
@app.post("/dummy-analyse-coin/")
async def dummy_analyse_coin(image1: UploadFile, image2: UploadFile):
    
    time.sleep(2)
    
    return {
        "country": "Canada",
        "year": 2017,
        "denomination": "5 Dollars",
        "materials": [
            {
                "material": "Silver",
                "percentage": 99.99
            },
            {
                "material": "Cheese",
                "percentage": 0.001
            }
        ],
        "estimated_value": 24.50,
        "rarity": 3,
        "obverse_image_no": 1,
        "obverse_image_desc": "Effigy of Queen Elizabeth II facing right.",
        "obverse_text": "ELIZABETH II 5 DOLLARS 2017",
        "reverse_image_no": 2,
        "reverse_image_desc": "Stylized maple leaf.",
        "reverse_text": "CANADA 9999 FINE SILVER 1 OZ ARGENT PUR 9999",
        "confidence": 95,
        "context": "This is a 2017 Canadian Silver Maple Leaf coin. It is identified by the effigy of Queen Elizabeth II and the \"5 DOLLARS 2017\" inscription on the obverse, and the iconic maple leaf design with \"CANADA\" and \"FINE SILVER 1 OZ ARGENT PUR 9999\" on the reverse. These coins are known for their high purity (99.99% silver) and are primarily valued for their silver bullion content, which is 1 troy ounce. The estimated value is based on the current market spot price for 1 troy ounce of silver, plus a typical small premium for a bullion coin. No further steps are needed for identification as all markings are clear and standard for this type of coin."
    }


# Analyse Coin Endpoint
# Take two images of the coin, prompt gemini and return a json of the coin data
@app.post("/analyse-coin/")
async def analyse_coin(image1: UploadFile, image2: UploadFile):

    prompt = """
    The two images show the obverse and reverse sides of a coin. Please can you analyse the images and populate a JSON object with the following values:
    
    - country: The coins country of origin (string)
    - year: The year the coin was minted (integer)
    - denomination: The name given to a coin of this value (string)
    - materials: A list of up to 3 metals found within the coin, each represented as an object with a material (string) and a percentage (float)
    - estimated_value: The current estimated value of the coin in GBP (float)
    - rarity: On a scale from 1 (common) to 10 (extremely rare), how rare is this coin (integer)
    - obverse_image_no: Which image (1 or 2) shows the obverse side of the coin (integer)
    - obverse_image_desc: A very short description of the image on the obverse side of the coin (string) - nullable
    - obverse_text: A transcript of the text on the obverse side of the coin (string) - nullable
    - reverse_image_no: Which image (1 or 2) shows the reverse side of the coin (integer)
    - reverse_image_desc: A very short description of the image on the reverse side of the coin (string) - nullable
    - reverse_text: A transcript of the text on the reverse side of the coin (string) - nullable
    - confidence: On a scale from 0 (not confident) to 100 (certain) how confident are you in your analysis and valuation of this coin (integer)
    - context: A short paragraph explaining the reasoning behind why the coin has been identified and valued in this way. If applicable, mention further steps to prove or disprove the identification (string)
    
    If any of the nullable fields are not relevant, populate the value with null.
    
    Return ONLY valid JSON. Do not include markdown or formatting.
    """

    # Read files
    image_bytes_1 = await image1.read()
    image_bytes_2 = await image2.read()
    image1 = Image.open(BytesIO(image_bytes_1))
    image2 = Image.open(BytesIO(image_bytes_2))

    # Instantiate the Google Gemini AI client
    client = genai.Client(api_key=api_key)

    # Try multiple times, each time it fails (due to the api being unavailable), wait exponentially longer
    for attempt in range(5):
        try:
            return json.loads(client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[prompt, image1, image2],
                config={
                    "response_mime_type": "application/json",
                },
            ).text)
        except Exception as e:
            print("Type of Exception:", type(e))
            print("Message:", e)
            if "503" in str(e):
                time.sleep(2 ** attempt)
                print
            else:
                raise
    
    return { "error": "Service temporarily unavailable" }


# Main endpoint serves a HTML form
@app.get("/")
async def main():
    return FileResponse('app/templates/index.html')