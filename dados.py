import requests
import pandas as pd
from config import TWELVE_DATA_KEY

def buscar_candles(par: str, timeframe: str, quantidade: int = 60) -> pd.DataFrame:
    url = "https://api.twelvedata.com/time_series"
    params = {
        "symbol": par,
        "interval": timeframe,
        "outputsize": quantidade,
        "apikey": TWELVE_DATA_KEY,
    }
    resp = requests.get(url, params=params, timeout=15)
    dados = resp.json()

    if "values" not in dados:
        raise ValueError(f"Erro ao buscar {par}: {dados}")

    df = pd.DataFrame(dados["values"])
    df = df.rename(columns={"datetime": "time"})
    df["close"] = df["close"].astype(float)
    df = df.iloc[::-1].reset_index(drop=True)
    return df
