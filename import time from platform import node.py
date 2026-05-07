import time from platform import node
print(f"\n--- [ SYSTEM HEARTBEAT ] ---")
gateway = "Active"  # Define gateway variable
print(f"🌐 Network Shield: {gateway}")
if node:
    print(f"⛓️  Chain: {node.get('chain')} | Blocks: {node.get('blocks')}")
    print(f"📉 Difficulty: {node.get('difficulty')}")
else:
    print("❌ Bitcoin Node: OFFLINE or Connection Refused")
    
time.sleep(5)