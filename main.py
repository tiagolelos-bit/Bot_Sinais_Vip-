import time
import schedule
from config import PARES, INTERVALO_ANALISE_MIN, TIMEFRAME
from dados import buscar_candles
from indicadores import calcular_indicadores, gerar_sinal
from telegram_bot import enviar_mensagem

def analisar_mercado():
    melhor_sinal = None
    melhor_par = None

    for par in PARES:
        try:
            df = buscar_candles(par, TIMEFRAME)
            df = calcular_indicadores(df)
            resultado = gerar_sinal(df)

            if resultado["sinal"] and resultado["forca"] == "moderado":
                melhor_sinal = resultado
                melhor_par = par
                break

        except Exception as e:
            print(f"Erro em {par}: {e}")

    if melhor_sinal:
        texto = (
            f"📊 *Sinal detectado*\n"
            f"Par: *{melhor_par}*\n"
            f"Direção: *{melhor_sinal['sinal']}*\n"
            f"RSI: {melhor_sinal['rsi']}\n"
            f"Preço: {melhor_sinal['preco']}\n\n"
            f"⚠️ Sinal baseado em cruzamento de médias + RSI. "
            f"Sem garantia de acerto — use gestão de risco."
        )
        enviar_mensagem(texto)
    else:
        print("Nenhum sinal com força suficiente neste ciclo.")

schedule.every(INTERVALO_ANALISE_MIN).minutes.do(analisar_mercado)

if __name__ == "__main__":
    analisar_mercado()
    while True:
        schedule.run_pending()
        time.sleep(30)
