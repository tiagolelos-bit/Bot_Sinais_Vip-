import pandas as pd
import pandas_ta as ta

def calcular_indicadores(df: pd.DataFrame) -> pd.DataFrame:
    df["sma20"] = ta.sma(df["close"], length=20)
    df["ema5"] = ta.ema(df["close"], length=5)
    df["rsi14"] = ta.rsi(df["close"], length=14)
    return df

def gerar_sinal(df: pd.DataFrame) -> dict:
    ultima = df.iloc[-1]
    anterior = df.iloc[-2]

    cruzou_cima = anterior["ema5"] <= anterior["sma20"] and ultima["ema5"] > ultima["sma20"]
    cruzou_baixo = anterior["ema5"] >= anterior["sma20"] and ultima["ema5"] < ultima["sma20"]

    sinal = None
    forca = "fraco"

    if cruzou_cima and ultima["rsi14"] < 65:
        sinal = "CALL (compra)"
        forca = "moderado" if ultima["rsi14"] < 50 else "fraco"
    elif cruzou_baixo and ultima["rsi14"] > 35:
        sinal = "PUT (venda)"
        forca = "moderado" if ultima["rsi14"] > 50 else "fraco"

    return {
        "sinal": sinal,
        "forca": forca,
        "rsi": round(ultima["rsi14"], 1),
        "preco": ultima["close"],
    }
