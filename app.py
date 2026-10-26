import os
import re
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="WhatsApp Hello", page_icon="💬", layout="centered")
st.title("💬 WhatsApp Hello")
st.caption("Send a simple WhatsApp message through Meta's official WhatsApp Cloud API.")

access_token = os.getenv("WHATSAPP_ACCESS_TOKEN", "").strip()
phone_number_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "").strip()
api_version = os.getenv("WHATSAPP_API_VERSION", "").strip()

with st.form("send_message_form"):
    recipient = st.text_input(
        "Recipient's WhatsApp number",
        placeholder="+14155552671",
        help="Include the country code, e.g. +1 for the US or +91 for India."
    )
    submitted = st.form_submit_button("Send WhatsApp message: Hi", type="primary")

def normalize_phone(value: str) -> str:
    # The Cloud API expects the destination as digits only, including country code.
    return re.sub(r"\D", "", value or "")

if submitted:
    if not (access_token and phone_number_id and api_version):
        st.error(
            "Configuration is incomplete. Set WHATSAPP_ACCESS_TOKEN, "
            "WHATSAPP_PHONE_NUMBER_ID, and WHATSAPP_API_VERSION in your .env file."
        )
    else:
        to_number = normalize_phone(recipient)
        if not to_number or not (8 <= len(to_number) <= 15):
            st.error("Enter a valid international phone number with its country code.")
        else:
            endpoint = (
                f"https://graph.facebook.com/{api_version}/"
                f"{phone_number_id}/messages"
            )
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            }
            payload = {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": to_number,
                "type": "text",
                "text": {"preview_url": False, "body": "Hi"},
            }

            try:
                with st.spinner("Submitting message to WhatsApp..."):
                    response = requests.post(
                        endpoint, headers=headers, json=payload, timeout=30
                    )
                if response.ok:
                    result = response.json()
                    st.success("WhatsApp accepted the message request.")
                    message_ids = [
                        item.get("id")
                        for item in result.get("messages", [])
                        if item.get("id")
                    ]
                    if message_ids:
                        st.caption("Message ID: " + ", ".join(message_ids))
                    st.info(
                        "An accepted API request is not proof of delivery. "
                        "Check WhatsApp delivery status in your Meta setup if needed."
                    )
                else:
                    try:
                        error_data = response.json()
                    except ValueError:
                        error_data = {"response": response.text[:1000]}
                    st.error(f"WhatsApp API returned HTTP {response.status_code}.")
                    st.code(str(error_data), language="json")
                    st.caption(
                        "Common causes: invalid/expired token, wrong phone-number ID "
                        "or API version, recipient not eligible for testing, missing "
                        "permissions, or messaging-policy/window restrictions."
                    )
            except requests.RequestException as exc:
                st.error(f"Could not reach the WhatsApp API: {exc}")

st.divider()
st.caption(
    "Use only for recipients who have agreed to receive your message. "
    "WhatsApp Business Platform policies and Meta account setup apply."
)
