# 📱 Xiaomi HyperOS Bootloader Unlock Auto-Sniper

Automated precision sniper for Xiaomi HyperOS Bootloader Unlock authorization requests.

---

## 🔗 Quick Links
* **GitHub Repository:** [https://github.com/DeveshB-1/xiaomi-unlock-sniper](https://github.com/DeveshB-1/xiaomi-unlock-sniper)
* **GitHub Actions Live Runs:** [https://github.com/DeveshB-1/xiaomi-unlock-sniper/actions](https://github.com/DeveshB-1/xiaomi-unlock-sniper/actions)

---

## ⏰ Schedule & Automation
* **Trigger Time:** Automatically runs every evening at **21:20 IST** via GitHub Actions cron (`50 15 * * *`).
* **Burst Execution:** Synchronizes with NTP clock and fires 80 rapid requests starting at **21:29:59.850 IST** (00:00:00 Beijing Time reset).
* **Secrets:** `SERVICE_TOKEN` and `DEVICE_ID` are stored securely in GitHub Actions encrypted secrets.

---

## 🚀 What to do After Permission is Granted (`apply_result: 1`):
1. **On Phone:**
   * Turn **OFF Wi-Fi**, turn **ON Mobile Data**.
   * Go to **Settings > Additional Settings > Developer Options > Mi Unlock Status**.
   * Tap **"Add account and device"** to bind your account.
2. **On PC (Fastboot Unlock):**
   * Boot into Fastboot mode (`Power + Volume Down`).
   * Connect to PC via USB cable.
   * Open official **Mi Unlock Tool** (`miflash_unlock.exe`) and click **Unlock**.

---

## 💻 Local Testing Commands
```bash
# Test connection with Xiaomi servers
python3 unlock_sniper.py --test

# Run manual sniper countdown locally
python3 unlock_sniper.py --snipe
```
