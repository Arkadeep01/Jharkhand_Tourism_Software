from fastapi import FastAPI
from Profile_Section.main_routes import router as main_router

app = FastAPI(title="Jharkhand Tourism - Eco Credit Rewards")

app.include_router(main_router, prefix="/api/v1")

# Root health check
@app.get("/")
def root():
    return {"ok": True, "service": "eco-credit-rewards", "version": "1.0"}
