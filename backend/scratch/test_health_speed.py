import time
import socket
import httpx

print("Testing 127.0.0.1 socket connect:")
t0 = time.time()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(0.05)
try:
    s.connect(("127.0.0.1", 8001))
    print("Connected")
except Exception as e:
    print(f"Failed in {round(time.time()-t0, 4)}s: {e}")
finally:
    s.close()

print("\nTesting httpx get 127.0.0.1:")
t0 = time.time()
try:
    httpx.get("http://127.0.0.1:8001/health", timeout=0.05)
except Exception as e:
    print(f"httpx failed in {round(time.time()-t0, 4)}s: {e}")
