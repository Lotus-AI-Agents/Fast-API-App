from fastapi import FastAPI, Request
import httpx

app = FastAPI()

# Replace this with your actual Zapier webhook URL
ZAPIER_WEBHOOK_URL = "https://hooks.zapier.com/hooks/catch/21667749/27ivbeb/"

@app.get("/")
async def root():
    return {"message": "Server is running. Waiting for POST data."}

@app.post("/")
async def relay_data(request: Request):
    try:
        # Get the form data from Twilio
        form = await request.form()
        data = dict(form)

        # Debug print: see what Twilio sent
        print("Received data:", data)

        # Forward the data to Zapier
        async with httpx.AsyncClient() as client:
            response = await client.post(ZAPIER_WEBHOOK_URL, json=data)

        return {"status": "success", "zapier_status": response.status_code}

    except Exception as e:
        # If something goes wrong, log the error
        print("Error occurred:", str(e))
        return {"status": "error", "details": str(e)}
