from fastapi import FastAPI, Request
from fastapi.responses import Response
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

        # Return TwiML so Twilio doesn't return error 12300
        twiml = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say>Your call has been received. Thank you!</Say>
</Response>"""
        return Response(content=twiml, media_type="application/xml")

    except Exception as e:
        print("Error occurred:", str(e))
        error_twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say>Error: {str(e)}</Say>
</Response>"""
        return Response(content=error_twiml, media_type="application/xml")
