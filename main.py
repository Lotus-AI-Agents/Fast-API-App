from fastapi import FastAPI, Request
from fastapi.responses import Response
import httpx

app = FastAPI()

# Your Zapier Webhook URL
ZAPIER_WEBHOOK_URL = "https://hooks.zapier.com/hooks/catch/21667749/27ivbeb/"

@app.post("/")
async def relay_data(request: Request):
    try:
        form = await request.form()
        data = dict(form)
        print("Received data:", data)

        # Send the data to Zapier
        async with httpx.AsyncClient() as client:
            await client.post(ZAPIER_WEBHOOK_URL, json=data)

        # Return a blank but valid TwiML XML response to keep Twilio happy
        return Response(
            content="""<?xml version="1.0" encoding="UTF-8"?><Response></Response>""",
            media_type="application/xml"
        )

    except Exception as e:
        print("Error occurred:", str(e))
        # Still return valid XML on error so Twilio doesn’t throw another error
        return Response(
            content=f"""<?xml version="1.0" encoding="UTF-8"?><Response><Say>Error: {str(e)}</Say></Response>""",
            media_type="application/xml"
        )
