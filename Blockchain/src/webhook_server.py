# webhook_server.py
from flask import Flask, request, abort
from save_payment import record_payment
import os, hmac, hashlib

app = Flask(__name__)
RAZORPAY_SECRET = os.getenv('RAZORPAY_WEBHOOK_SECRET')  
@app.route('/webhook/razorpay', methods=['POST'])
def razorpay_webhook():
    payload = request.data
    signature = request.headers.get('X-Razorpay-Signature')
    # Verify signature (Razorpay uses HMAC SHA256)
    if RAZORPAY_SECRET:
        generated = hmac.new(RAZORPAY_SECRET.encode(), payload, hashlib.sha256).hexdigest()
        if not hmac.compare_digest(generated, signature):
            abort(400)
    data = request.json

    # Build a canonical payment_payload from fields you want to store
    payment_entity = data.get('payload', {}).get('payment', {}).get('entity', {}) if data else {}
    payment_payload = {
        'tx_id': payment_entity.get('id', 'unknown'),
        'user_id': payment_entity.get('contact'),
        'amount': (payment_entity.get('amount', 0) / 100.0) if payment_entity else 0, 
        'currency': payment_entity.get('currency', 'INR'),
        'payment_method': payment_entity.get('method'),
        'status': payment_entity.get('status', 'unknown')
    }
    saved = record_payment(payment_payload)
    return {'ok': True, 'saved': str(saved.get('_id'))}

if __name__ == '__main__':
    app.run(port=5000)
