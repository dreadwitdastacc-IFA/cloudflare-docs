import json
import time
import random


def engine_pulse():
    print("--------------------------------------------------")
    print("[ORUNMILA] Sentinel Apex Core Engine Ignited.")
    print("--------------------------------------------------")

    # Simulated block height climbing to show it is "Live"
    current_block = 144
    
    while True:
        try:
            # 1. Fetch live data (Simulated for this test)
            current_block += random.randint(0, 1)
            btc_balance = 0.54020000 # Your simulated vault
            eth_price = round(random.uniform(3000.00, 3100.00), 2)
            ltc_price = round(random.uniform(80.00, 85.00), 2)

            # 2. Construct the state dictionary matching the React UI exactly
            state = {
                "btc_bal": btc_balance,
                "blocks": current_block,
                "eth_price": eth_price,
                "ltc_price": ltc_price,
                "error": False
            }

            # 3. Write to the Akashic Record
            with open('sentinel_state.json', 'w') as f:
                json.dump(state, f)
            
            print(f"[PULSE] State Updated | Blocks: {current_block} | BTC: {btc_balance}")
            
            # Rest for 2 seconds before the next pulse
            time.sleep(2)
            
        except Exception as e:
            print(f"[ERROR] Engine Misfire: {e}")
            time.sleep(5)

if __name__ == '__main__':
    engine_pulse()
