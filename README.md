# WhatsApp Hello — Streamlit

A minimal Streamlit app with a phone-number field and a button that submits the message **“Hi”** using Meta's official WhatsApp Business Platform Cloud API.

## What this app does

- Accepts one international recipient number at a time.
- Sends the literal text `Hi` using the configured WhatsApp Business phone number.
- Keeps the access token in an environment file rather than in source code.
- Shows the API response or an error to help troubleshoot setup.

## Important limitations

This app does **not** grant itself WhatsApp permissions. You must configure a Meta app and WhatsApp Business Platform/Cloud API access, and supply valid credentials. A phone number being typed into the app does not guarantee WhatsApp will allow delivery.

- Use this only for people who have opted in to receive messages from you.
- During development, Meta's test setup may restrict which recipient numbers you can message.
- Free-form text is generally allowed during the 24-hour customer-service window after a user messages the business. Outside that window, a business-initiated message generally needs an approved message template.
- API acceptance is not the same as delivery. Delivery status is separate.

## Files

- `app.py` — Streamlit UI and Cloud API request.
- `requirements.txt` — Python dependencies.
- `.env.example` — environment-variable template.
- `INSTRUCTIONS.md` — setup and run instructions.
- `.gitignore` — helps prevent committing credentials.
