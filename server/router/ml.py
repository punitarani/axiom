"""server/router/ml.py"""

from datetime import datetime, timedelta

import pandas as pd
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from mdata.equity import get_daily_price_history
from sklearn.preprocessing import StandardScaler

from ..load import get_weekly_resistance_model

router = APIRouter(prefix="/ml")


@router.get("/weekly-resistance")
async def get_weekly_resistance(symbol: str = "SPY") -> JSONResponse:
    # Temporarily only allow SPY
    if symbol != "SPY":
        raise HTTPException(status_code=404, detail="Symbol not supported")

    # Get the lats week's highs and lows
    data = await get_daily_price_history(symbol)
    df = pd.DataFrame.from_records([candle.model_dump() for candle in data.candles])
    df["datetime"] = pd.to_datetime(df["datetime"], unit="ms")

    # Calculate last Friday's date
    today = datetime.now()
    last_friday_date = today - timedelta(days=(today.weekday() + 1) % 7 + 3)

    # Filter the data to only last week's data
    df_filtered = df[df["datetime"] <= last_friday_date].iloc[-5:]
    highs = df_filtered["high"].values.reshape(1, -1)
    lows = df_filtered["low"].values.reshape(1, -1)

    # Get the models
    model = await get_weekly_resistance_model()
    if model is None:
        raise HTTPException(status_code=500, detail="Error loading models")

    # Run the model
    next_week_high, next_week_low = model.predict(highs, lows)

    return JSONResponse(
        content={
            "symbol": symbol,
            "next_week_high": float(next_week_high),
            "next_week_low": float(next_week_low),
        }
    )
