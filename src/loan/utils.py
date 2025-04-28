import os
import json
import hmac
import hashlib
import base64
import httpx
from datetime import datetime, timezone

ABA_PAYWAY_QR_API = "https://checkout-sandbox.payway.com.kh/api/payment-gateway/v1/payments/generate-qr"
ABA_PAYWAY_KEY = os.environ.get("ABA_PAYWAY_KEY")
ABA_CALLBACK_URL = os.environ.get("ABA_CALLBACK_URL")
ABA_PAYWAY_MERCHANT_ID = os.environ.get("ABA_PAYWAY_MERCHANT_ID")

async def generate_qr_code(self) -> str:
    """
    Generate QR code for payment
    :return: QR code string
    """

    #Encode callback url into bytes
    byte_callback = ABA_CALLBACK_URL.encode("utf-8")
    #Encode callback url into base64
    b64_callback = base64.b64encode(byte_callback)
    #Encode b64-byte callback url into string
    str_callback = b64_callback.decode()


    body = {
        "req_time": datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S"),
        "merchant_id": ABA_PAYWAY_MERCHANT_ID,
        "tran_id": str(self.id),
        "amount": "11",
        "payment_option": "abapay_khqr",
        "callback_url": str_callback,
        "currency": "USD",
        "lifetime": "5000",
        "qr_image_template": "template1",
    }
    #Concatenate the values of the body together
    body_string = "".join(body.values())


    #Convert string to bytes
    byte_body_string = body_string.encode("utf-8")
    byte_key_string = ABA_PAYWAY_KEY.encode("utf-8")
    #Create HMAC-SHA512 hash
    hmac_digest = hmac.new(byte_key_string, byte_body_string, hashlib.sha512).digest()
    #Encode the hash in base64
    base64_encoded = base64.b64encode(hmac_digest).decode()

    body["amount"] = 11
    body["lifetime"] = 5000
    body["hash"] = base64_encoded

    # Convert the Python dict to JSON
    payload = json.dumps(body)

    headers = {
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(ABA_PAYWAY_QR_API, headers=headers, data=payload)
            return response.json().get("qrString")
        except httpx.RequestError as e:
            raise Exception(f"An error occurred while requesting {e.request.url!r}.")
        except httpx.HTTPStatusError as e:
            raise Exception(f"Error response {e.response.status_code} while requesting {e.request.url!r}.")

        
   