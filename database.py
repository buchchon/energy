import sqlite3
import os

def get_db_connection():
   try:
       conn = sqlite3.connect('power_readings.db')
       return conn
   except sqlite3.Error as e:
       print(f"Database connection failed: {e}")
       return None

def create_table():
   conn = sqlite3.connect('power_readings.db')
   c = conn.cursor()
   #Create Floor Table
   c.execute("""
             CREATE TABLE IF NOT EXISTS floors (
             floor_ID text PRIMARY KEY,
             building_ID text
             )""")
   conn.commit()
  
   #Create Clamp Table
   c.execute("""CREATE TABLE IF NOT EXISTS clamps (
             clamp_ID text PRIMARY KEY,
             floor_ID text,
             FOREIGN KEY (floor_ID) REFERENCES floors(floor_ID)
             )""")
   conn.commit()
  
   #Create Readins Table
   c.execute("""CREATE TABLE IF NOT EXISTS readings (
             clamp_ID text,
             date_time integer,
             value integer,
             FOREIGN KEY (clamp_ID) REFERENCES clamps(clamp_ID)
             PRIMARY KEY (clamp_ID, date_time)
             )""")
   conn.commit()
   conn.close()

create_table()
