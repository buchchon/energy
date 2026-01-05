from flask import Blueprint, jsonify
import requests
import time
import hashlib
import hmac
import base64
from database import get_db_connection
import sqlite3
from datetime import datetime, timedelta


# Tuya API credentials
ACCESS_ID = "XXXXXX"
ACCESS_KEY = "XXXXXX"
API_ENDPOINT = "https://openapi.tuyaus.com"  # Update endpoint based on your region

def add_reading_to_db(clamp_id, date_time, value):
   """
   Insert a new reading into the database for a given clamp ID.
   """
   conn = get_db_connection()
   c = conn.cursor()
   c.execute(
       "INSERT INTO readings (clamp_ID, date_time, value) VALUES (?, ?, ?)",
       (clamp_id, date_time, value),
   )
   conn.commit()
   conn.close()



def get_signature(access_id, access_key, t):
   """Generate Tuya API signature."""
   string_to_sign = access_id + t
   signature = hmac.new(
       access_key.encode('utf-8'),
       string_to_sign.encode('utf-8'),
       hashlib.sha256
   ).digest()
   return base64.b64encode(signature).decode('utf-8')

def get_headers():
   """Generate headers for the Tuya API request."""
   t = str(int(time.time() * 1000))  # Current timestamp in milliseconds
   signature = get_signature(ACCESS_ID, ACCESS_KEY, t)

   return {
       "client_id": ACCESS_ID,
       "sign": signature,
       "t": t,
       "sign_method": "HMAC-SHA256",
       "Content-Type": "application/json",
   }

def insert_reading(device_id):
   """Fetch the forward energy total for the PC311_W_TY clamp meter."""
   url = f"{API_ENDPOINT}/v1.0/devices/{device_id}/functions"

   headers = get_headers()
  
   response = requests.get(url, headers=headers)

   if response.status_code == 200:
       data = response.json()
       for function in data.get("result", {}).get("functions", []):
           if function["code"] == "forward_energy_total":
               return {
                   "success": True,
                   "unit": function.get("unit", ""),
                   "value": function.get("value", 0)
               }
       return {"success": False, "message": "forward_energy_total not found."}
   else:
       return {"success": False, "message": response.json()}



def query_data():
   conn = get_db_connection()
   c = conn.cursor()

   #get all clamps for database
   c.execute("SELECT DISTINCT clamp_ID FROM clamps")
   clamps = [row[0] for row in c.fetchall()]

   if not clamps:
       print("No clamps found, returning 0")
       return 0
  
  
   for clamp in clamps:
       value = insert_reading(clamp)
       current_time = datetime.now()
       current_timestamp = int(current_time.timestamp())
       add_reading_to_db(clamp, current_timestamp, value)

   conn.close()
