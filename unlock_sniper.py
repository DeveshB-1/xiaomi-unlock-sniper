#!/usr/bin/env python3
import time
import json
import argparse
import requests
from datetime import datetime, timezone, timedelta

# Target Xiaomi Global API Endpoint
API_URL = "https://sgp-api.buy.mi.com/bbs/api/global/apply/bl-auth"

# Captured Credentials & Device Tokens
SERVICE_TOKEN = "XxMKTR8913M%2FArytCfrxAHNeephO1csL5uNWjeXvSI2OKW1aQQAs5Ah3V86nX6AaikjkjjJ5blFV57uWAE%2B9ttkOZDj%2FP4p6t%2Bo8RIrrAqgEPDKKt5xjQUZz3V%2FlLRI1KuLy90wW5EMmIJTOyMFHjSTQxdFdiSbdB3XQdXnNjWg%3D"
DEVICE_ID = "927991B7CC07ECCAF75A14C7D836F6512CDC7051"
VERSION_CODE = "500428"
VERSION_NAME = "5.4.28"

HEADERS = {
    "User-Agent": "okhttp/4.12.0",
    "Content-Type": "application/json; charset=utf-8",
    "Accept": "application/json",
    "Cookie": (
        f"new_bbs_serviceToken={SERVICE_TOKEN};"
        f"versionCode={VERSION_CODE};"
        f"versionName={VERSION_NAME};"
        f"deviceId={DEVICE_ID};"
    ),
}

PAYLOAD = {"is_retry": True}


def send_request(session=None):
    s = session or requests.Session()
    try:
        resp = s.post(API_URL, headers=HEADERS, json=PAYLOAD, timeout=5)
        return resp.status_code, resp.json()
    except Exception as e:
        return 0, {"error": str(e)}


def test_connection():
    print("=" * 60)
    print("🔍 Testing Xiaomi Unlock API with captured credentials...")
    print("=" * 60)
    
    session = requests.Session()
    status_code, data = send_request(session)
    
    print(f"HTTP Status: {status_code}")
    print("Raw Response:", json.dumps(data, indent=2))
    print("-" * 60)
    
    code = data.get("code")
    res = data.get("data", {}).get("apply_result")
    
    if code == 0:
        if res == 1:
            print("🎉 SUCCESS! Unlock permission has been GRANTED!")
        elif res == 3:
            deadline = data.get("data", {}).get("deadline_format", "00:00")
            print(f"✅ Auth Valid! Quota full for now, resets at {deadline} Beijing Time (21:30 IST).")
            print("🚀 Tokens are 100% ready for sniper mode tonight.")
        else:
            print(f"ℹ️ Auth Valid. Result code: {res}")
    else:
        print(f"❌ Error: {data.get('msg', 'Unknown error')}")


def run_sniper():
    # Target: 21:30:00.000 IST (16:00:00.000 UTC / 00:00:00.000 Beijing Time)
    ist = timezone(timedelta(hours=5, minutes=30))
    now = datetime.now(ist)
    
    # Calculate target 21:30:00 IST
    target = now.replace(hour=21, minute=30, second=0, microsecond=0)
    if (target - now).total_seconds() < -10:
        target += timedelta(days=1)
        
    print(f"🎯 Target Time: {target.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print(f"🕒 Current Time: {datetime.now(ist).strftime('%Y-%m-%d %H:%M:%S.%f %Z')[:-3]}")
    
    # Burst start: 21:29:59.800 IST (200ms lead time for network latency to Singapore)
    burst_lead = 0.200
    
    session = requests.Session()
    # Warm up TCP / TLS handshake connection early
    try:
        session.get("https://sgp-api.buy.mi.com", timeout=3)
    except Exception:
        pass

    # Precision countdown loop
    while True:
        current = datetime.now(ist)
        diff = (target - current).total_seconds()
        
        if diff > 10:
            print(f"⏳ Waiting for 21:30 IST... Remaining: {int(diff)}s", end="\r")
            time.sleep(1)
        elif diff > burst_lead:
            print(f"⏳ Armed & Ready... Remaining: {diff:.3f}s", end="\r")
            time.sleep(0.01)
        else:
            print(f"\n🚀 [TRIGGERED AT {datetime.now(ist).strftime('%H:%M:%S.%f')[:-3]}] FIRING BURST REQUESTS! 🚀")
            break
            
    # Send rapid burst requests around the 21:30:00.000 mark
    for i in range(1, 80):
        t_req = datetime.now(ist).strftime("%H:%M:%S.%f")[:-3]
        status, res = send_request(session)
        print(f"[{t_req}] Request #{i:02d} -> HTTP {status} | Result: {res}")
        
        # Check for success
        if res.get("data", {}).get("apply_result") == 1:
            print("\n" + "=" * 60)
            print("🎉🎉🎉 SUCCESS! BOOTLOADER UNLOCK PERMISSION GRANTED! 🎉🎉🎉")
            print("=" * 60)
            return True
            
        time.sleep(0.12)
        
    print("\n⚠️ Burst finished. Check responses above.")
    return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Xiaomi Bootloader Unlock Auto-Sniper")
    parser.add_argument("--test", action="store_true", help="Test credentials immediately")
    parser.add_argument("--snipe", action="store_true", help="Wait and snipe at 21:30 IST")
    args = parser.parse_args()
    
    if args.snipe:
        run_sniper()
    else:
        test_connection()
