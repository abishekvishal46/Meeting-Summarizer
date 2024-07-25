from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from summarizer import summarize_meeting_transcript
import json
app = FastAPI()

templates = Jinja2Templates(directory="templates")


class TranscriptRequest(BaseModel):
    transcript: str


@app.get("/", response_class=HTMLResponse)
async def read_summary(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.post("/generate-summary")
async def generate_summary(request: Request, transcript: str = Form(...)):
    try:
        # Print the submitted transcript for debugging


        # Create a mock summary for demonstration
        summarized_str = summarize_meeting_transcript(transcript=transcript)
        print("API is been called!!!")
        summarized_dict = json.loads(summarized_str)
        print(summarized_dict)
        # Prepare summary data for the template
        summary_data = [
            {"key": list(item.keys())[0], "value": list(item.values())[0]}
            for item in summarized_dict['SUMMARY'][0]['SUBHEADINGS']
        ]

        return templates.TemplateResponse("index.html", {
            "request": request,
            "summary_data": summary_data
        })
    except Exception as e:
        # Log or handle the exception
        print(f"Error: {e}")
        return {"error": "An error occurred while generating the summary."}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5000)
