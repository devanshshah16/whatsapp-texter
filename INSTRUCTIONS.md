# Setup and run instructions

## 1. Create the Meta / WhatsApp API setup

1. Sign in to Meta for Developers and create or select a Meta app.
2. Add/configure the WhatsApp product and follow Meta's Cloud API getting-started flow.
3. Use the test sender while developing, or configure an eligible business phone number for your intended use.
4. In the WhatsApp API setup, note:
   - **Access token** — use a suitable token for your environment. Temporary development tokens expire; for ongoing use, configure an appropriate longer-lived/system-user token following Meta's current guidance.
   - **Phone number ID** — this is the sender's Cloud API phone-number ID, not the recipient's number and not necessarily the visible telephone number.
   - **Graph API version** — use a currently supported version shown by Meta's documentation/dashboard.
5. Ensure the Meta app/token has the required WhatsApp permissions:
   - `whatsapp_business_messaging` — send messages.
   - `whatsapp_business_management` — manage/access WhatsApp Business account assets as needed for setup.
   Some business-portfolio operations may require additional permissions, but this minimal app normally needs the messaging permission and the appropriate access to the configured WhatsApp assets. Grant permissions in Meta; adding names to Python does not grant them.
6. Add the recipient as a permitted test recipient if Meta's test environment requires it. For real messaging, ensure the recipient has opted in and that your message complies with WhatsApp's current rules.

Official references:
- Meta's WhatsApp Cloud API overview: https://developers.facebook.com/docs/whatsapp/cloud-api/overview
- Cloud API messages reference: https://developers.facebook.com/docs/whatsapp/cloud-api/reference/messages
- Meta's WhatsApp Business Platform documentation collection: https://www.postman.com/meta/whatsapp-business-platform/documentation/wlk6lh4/whatsapp-cloud-api

## 2. Set up Python

Open a terminal in this folder. Python 3.10+ is recommended.

Create and activate a virtual environment:

**macOS/Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows PowerShell**
```powershell
py -m venv .venv
.venv\\Scripts\\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## 3. Configure credentials

Copy `.env.example` to a file named `.env` in the same folder, then fill in the three values from your Meta setup:

```dotenv
WHATSAPP_ACCESS_TOKEN=your_token_here
WHATSAPP_PHONE_NUMBER_ID=your_sender_phone_number_id
WHATSAPP_API_VERSION=your_supported_graph_api_version
```

Do not include quotes unless needed, do not paste credentials into `app.py`, and never share or commit `.env`. If a token is exposed, revoke/rotate it in Meta.

## 4. Run the app

```bash
streamlit run app.py
```

Streamlit will print a local URL, usually `http://localhost:8501`. Open it in your browser, enter the recipient's international number (for example, `+14155552671`), and click **Send WhatsApp message: Hi**.

The app removes spaces, plus signs, brackets, and dashes before sending; the country code must still be included. It sends only to one number per click.

## 5. Troubleshooting

- **Missing configuration:** Check that `.env` exists beside `app.py`, contains all three variables, and that you restarted Streamlit after editing it.
- **401/190 or token error:** Token may be invalid, expired, or missing required access.
- **Permission error:** Confirm `whatsapp_business_messaging` and access to the relevant WhatsApp Business account/phone number.
- **Invalid parameter / phone-number ID:** Confirm you used the sender's *Phone Number ID*, not the recipient's number.
- **Recipient/test-number error:** Add/verify the recipient in Meta's test setup where required, or confirm the production setup supports that recipient.
- **Message not delivered:** A successful API response only means the request was accepted. Check delivery status and ensure opt-in and messaging-window/template rules are met.
- **API version error:** Update `WHATSAPP_API_VERSION` to a currently supported version from Meta's documentation.

## Security and compliance

This is a starter/demo app, not a production messaging platform. Do not expose it publicly with an unrestricted send button. Add authentication, rate limiting, audit logging, and appropriate access controls before deployment. Never use it for unsolicited bulk messaging or to evade WhatsApp policies.
