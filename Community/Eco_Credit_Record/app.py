# tests/test_rewards.py
import pytest
from fastapi.testclient import TestClient
from Eco_Credit_Record.app import app
from unittest.mock import MagicMock
from Eco_Credit_Record import db as real_db
import importlib

# Use TestClient
client = TestClient(app)

@pytest.fixture(autouse=True)
def patch_db(monkeypatch):
    # Create simple in-memory lists to simulate collections
    transactions_store = []
    redemptions_store = []

    class FakeCollection:
        def __init__(self, store):
            self.store = store

        def find_one(self, filter=None, sort=None):
            if not self.store:
                return None
            return self.store[-1]

        def insert_one(self, doc):
            # fake ObjectId with integer index
            doc_copy = doc.copy()
            doc_copy["_id"] = len(self.store) + 1
            self.store.append(doc_copy)
            class R: inserted_id = doc_copy["_id"]
            return R()

        def find(self, filter, sort=None):
            # return reversed iterator limited by None
            filtered = [d for d in self.store if d.get("user_id") == filter.get("user_id")]
            class Cursor:
                def __init__(self, arr):
                    self.arr = arr
                def sort(self, *_):
                    return self
                def limit(self, *_):
                    return iter(self.arr)
            return Cursor(list(reversed(filtered)))

    fake_tx = FakeCollection(transactions_store)
    fake_red = FakeCollection(redemptions_store)

    # patch db.transactions and db.redemptions
    monkeypatch.setattr(real_db, "transactions", fake_tx)
    monkeypatch.setattr(real_db, "redemptions", fake_red)

    yield

def test_add_transaction_and_balance_flow():
    payload = {"user_id": "testuser1", "action": "eco_hotel_stay"}
    r = client.post("/api/v1/transactions", json=payload)
    assert r.status_code == 201
    body = r.json()
    assert body["user_id"] == "testuser1"
    assert body["credits_balance"] == body["credits_earned"]
    # check balance endpoint
    b = client.get("/api/v1/balance/testuser1").json()
    assert b["balance"] == body["credits_balance"]

def test_redeem_flow():
    # first add some credits
    payload = {"user_id": "redeemuser", "action": "plant_tree"}
    r = client.post("/api/v1/transactions", json=payload)
    assert r.status_code == 201
    earned = r.json()["credits_earned"]

    # redeem some credits
    redeem_payload = {"user_id": "redeemuser", "credits_used": 10, "reward_item": "Voucher"}
    r2 = client.post("/api/v1/redeem", json=redeem_payload)
    assert r2.status_code == 200
    resp = r2.json()
    assert resp["remaining_balance"] >= 0
