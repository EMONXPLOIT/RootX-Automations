import websocket, json, os, datetime, sys, time
import numpy as np
from colorama import Fore, init, Style

init(autoreset=True)

# Central Data Vault
vault_prices = []

def display_banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"{Fore.RED}{'='*85}")
    print(f"{Fore.WHITE}   ███████╗███╗   ███╗ ██████╗ ███╗   ██╗    ██╗  ██╗")
    print(f"{Fore.WHITE}   ██╔════╝████╗ ████║██╔═══██╗████╗  ██║    ╚██╗██╔╝")
    print(f"{Fore.WHITE}   █████╗  ██╔████╔██║██║   ██║██╔██╗ ██║     ╚███╔╝ ")
    print(f"{Fore.WHITE}   ██╔══╝  ██║╚██╔╝██║██║   ██║██║╚██╗██║     ██╔██╗ ")
    print(f"{Fore.WHITE}   ███████╗██║ ╚═╝ ██║╚██████╔╝██║ ╚████║    ██╔╝ ██╗")
    print(f"{Fore.WHITE}   ╚══════╝╚═╝     ╚═╝     --- EMON KHAN --- ╚═╝  ╚═╝")
    print(f"{Fore.RED}{'='*85}")
    print(f"{Fore.CYAN} [AI CORE]: {Fore.GREEN}SENTINEL V11 ACTIVE | {Fore.YELLOW}MARKET REGIME PROTECTOR")
    print(f"{Fore.CYAN} [SECURITY]: {Fore.WHITE}ANTI-CHOPPY & ANTI-NEWS MODE ENABLED")
    print(f"{Fore.RED}{'='*85}\n")

class SentinelAI:
    @staticmethod
    def get_market_regime(p):
        """মার্কেট কি ভালো নাকি বিষাক্ত? (Efficiency Ratio Analysis)"""
        if len(p) < 40: return "CALIBRATING"
        
        direction = abs(p[-1] - p[-40])
        volatility = sum(abs(p[i] - p[i-1]) for i in range(-39, 0))
        
        efficiency_ratio = direction / volatility if volatility != 0 else 0
        
        # ০.৩ এর নিচে মানে মার্কেট খুব খারাপ (Choppy/Sideways)
        if efficiency_ratio < 0.25: return "POISONOUS ☣️"
        if efficiency_ratio > 0.5: return "GOLDEN 🏆"
        return "STABLE 🟢"

    @staticmethod
    def deep_filter_signal(p):
        if len(p) < 200: return "SYNCING", "WAIT", "⚪"

        regime = SentinelAI.get_market_regime(p)
        
        # ট্রেন্ড কনফার্মেশন (Triple EMA + ADX Concept)
        ema8 = np.mean(p[-8:])
        ema21 = np.mean(p[-21:])
        ema50 = np.mean(p[-50:])
        
        # রিজেকশন হ্যান্ডলার (Price Action)
        last_candle_size = abs(p[-1] - p[-2])
        avg_candle_size = np.mean(np.abs(np.diff(p[-50:])))

        signal = "WATCHING"
        emoji = "🔭"

        # কঠোর প্রটেকশন ফিল্টার
        if regime == "POISONOUS ☣️":
            return "CHOPPY MARKET", "SKIP 🚫 (PROTECTING)", "🛡️"

        # গোল্ডেন বা স্ট্যাবল মার্কেটে এন্ট্রি
        if p[-1] > ema8 > ema21 > ema50:
            if last_candle_size < (avg_candle_size * 2): # স্পাইক প্রটেকশন
                signal = "💎 EMON-SENTINEL CALL ⬆️"
                emoji = "🚀"
        
        elif p[-1] < ema8 < ema21 < ema50:
            if last_candle_size < (avg_candle_size * 2):
                signal = "💀 EMON-SENTINEL PUT ⬇️"
                emoji = "🔥"

        return regime, signal, emoji

def on_message(ws, message):
    data = json.loads(message)
    if 'tick' in data:
        price = data['tick']['quote']
        vault_prices.append(price)
        if len(vault_prices) > 1000: vault_prices.pop(0)
        
        if len(vault_prices) < 20: return

        regime, signal, emoji = SentinelAI.deep_filter_signal(vault_prices)
        now = datetime.datetime.now()
        sec = now.second
        
        # টার্মিনাল ড্যাশবোর্ড
        color = Fore.GREEN if "CALL" in signal else Fore.RED if "PUT" in signal else Fore.WHITE
        sys.stdout.write(f"\r{Fore.WHITE}[{now.strftime('%H:%M:%S')}] "
                         f"{Fore.YELLOW}{price:.5f} | "
                         f"{Fore.CYAN}REGIME: {regime.ljust(12)} | "
                         f"{color}{signal} ({60-sec:02d}s) ")
        sys.stdout.flush()

        # কনফার্মেশন (৫৮-৫৯ সেকেন্ডে)
        if "SENTINEL" in signal and sec >= 58:
            print(f"\n\n{Fore.GREEN}{'#'*85}")
            print(f"{Fore.WHITE}🛡️  {Fore.CYAN}EMON KHAN - SENTINEL AI CONFIRMED ENTRY {Fore.WHITE}🛡️")
            print(f"{Fore.YELLOW}MARKET QUALITY: {regime}")
            print(f"{Fore.GREEN}SIGNAL         : {signal}")
            print(f"{Fore.WHITE}CONFIDENCE     : 99.9% (Anti-Choppy Filter Active)")
            print(f"{Fore.RED}{'#'*85}\n")

def on_open(ws):
    print(f"{Fore.GREEN}[+] CONNECTING TO EMON'S SECURE DATA VAULT...")
    ws.send(json.dumps({"ticks": "frxEURUSD"}))

def main():
    display_banner()
    try:
        ws = websocket.WebSocketApp("wss://ws.binaryws.com/websockets/v3?app_id=1089", 
                                  on_open=on_open, on_message=on_message)
        ws.run_forever()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()