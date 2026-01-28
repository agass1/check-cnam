# Telegram Bot for Health Insurance Expiry Notifications

This bot automatically checks **the status of the health insurance policy (for citizens of the Republic of Moldova)** and notifies in Telegram if the policy has expired.

The check is performed every **24 hours**, the timer is implemented directly in the script for cross-platform operation **without using cron or Task Scheduler**.

For stable operation, it is recommended to add the script to your system **autostart**.

---------------------------------------------------------------

## Checking Platform

https://aoam.cnam.gov.md:10201/check-status

---------------------------------------------------------------

## Installing Dependencies

Contents of `requirements.txt`:

selenium>=4.15.0  
requests>=2.31.0  

Installation:

pip install -r requirements.txt  
or  
pip3 install -r requirements.txt  

Chrome or Firefox and the corresponding WebDriver in PATH are also required.

---------------------------------------------------------------

## Telegram Bot Setup

1. Create a bot via @BotFather  
   - /newbot  
   - set a name  
   - set a username (must end with bot)  
   - save the provided token  

2. Getting chat_id  
   Edit `getchatid.py`:

TOKEN = "ТОКЕН_ИЗ_BOTFATHER"

Run:

python3 getchatid.py

You will receive:

Your personal chat_id: xxxxxxxxx

---------------------------------------------------------------

## Main Script Setup

Edit `med.py`:

TOKEN = "ВСТАВЬТЕ_ТОКЕН_ИЗ_BOTFATHER"

CHAT_ID = "ВСТАВЬТЕ_АЙДИ_ЧАТА"

DATA_IN ="ВСТАВЬТЕ_ПРОВЕРЯЕМЫЙ_НОМЕР_ПАСПОРТА" 

HEADLESS = True  
TESTMODE = False  

Run:

python3 med.py

---------------------------------------------------------------

## Parameters

HEADLESS  
True — browser runs in the background  
False — browser is visible  

TESTMODE  
True — sends any status every 24 hours  
False — sends notification only if status != ASIGURAT  

---------------------------------------------------------------

## Notification Logic

if TESTMODE:
    send_telegram_message(f"[TEST] Status: {result}")
    
else:
    if result.strip().upper() != "ASIGURAT":
        send_telegram_message("Seems your health insurance expired")

---------------------------------------------------------------

## Autostart

Linux: autostart / screen / tmux  
Windows: Startup folder or Task Scheduler
