# export.py
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from utils.db import aggregates_col
import pandas as pd
from io import StringIO

router = APIRouter()

@router.get("/export/csv")
def export_csv(start: str, end: str):
    cursor = aggregates_col.find({"date": {"$gte": start, "$lte": end}}).sort("date", 1)
    df = pd.DataFrame(list(cursor))
    if df.empty:
        raise HTTPException(status_code=404, detail="No data for given range")

    output = StringIO()
    df.to_csv(output, index=False)
    output.seek(0)
    return StreamingResponse(output, media_type="text/csv", headers={
        "Content-Disposition": f"attachment; filename=analytics_{start}_to_{end}.csv"
    })
