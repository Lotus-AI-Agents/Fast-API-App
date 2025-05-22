from fastapi import FastAPI, Request
from fastapi.responses import Response
import httpx

app = FastAPI()

# Replace with your actual Zapier webhook URL
ZAPIER_WEBHOOK_URL = "https://hooks.zapier.com/hooks/catch/21667749/27ivbeb/"

@app.post("/")
async def relay_data(request: Request):
    try:
        # Parse form data from Twilio into a flat dictionary
        form = await request.form()
        data = dict(form)
        print("Received data:", data)

        # Send the data to Zapier as top-level JSON
        async with httpx.AsyncClient() as client:
            await client.post(ZAPIER_WEBHOOK_URL, json=data)

        # Return valid TwiML XML to Twilio to avoid 12300
        return Response(
            content="""<?xml version="1.0" encoding="UTF-8"?><Response></Response>""",
            media_type="application/xml"
        )

    except Exception as e:
        print("Error occurred:", str(e))
        return Response(
            content=f"""<?xml version="1.0" encoding="UTF-8"?><Response><Say>Error: {str(e)}</Say></Response>""",
            media_type="application/xml"
        )
