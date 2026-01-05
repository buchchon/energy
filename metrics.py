from flask import Blueprint, jsonify
import sqlite3
from datetime import datetime, timedelta
from database import get_db_connection

metrics = Blueprint('metrics', __name__)

# Overall function to get power consumed
def get_power_consumed(start_time):
   conn = get_db_connection()
   c = conn.cursor()

   #Get current time in UNIX stamp
   current_time = int(datetime.now().timestamp())

   #get all clamps for database
   c.execute("SELECT DISTINCT clamp_ID FROM clamps")
   clamps = [row[0] for row in c.fetchall()]

   if not clamps:
       print("No clamps found, returning 0")
       return 0
  
   total_power_consumed = 0

   #iteraring through each clamp id
   for clamp_id in clamps:
      
       #find value at start_time (or closest)
       c.execute(""" SELECT value FROM readings WHERE clamp_id = ? AND date_time <= ? ORDER BY date_time DESC LIMIT 1 """, (clamp_id, start_time))
       start_reading = c.fetchone()

       #find value at current_time (or closest as well)
       c.execute(""" SELECT value FROM readings WHERE clamp_id = ? AND date_time <= ? ORDER BY date_time DESC LIMIT 1 """, (clamp_id, current_time))
       end_reading = c.fetchone()

       if start_reading is None or end_reading is None:
           print(f"No valid readings for clamp {clamp_id}, skipping")
           continue
      
       power_consumed = end_reading[0] - start_reading[0] #fetch returns in tuple, only choose first value
       total_power_consumed = total_power_consumed + power_consumed
  
   conn.close()
   return round(total_power_consumed)


@metrics.route('/power-last-5-min', methods=['GET'])
def power_last_5_min():
   current_time = int(datetime.now().timestamp())
   start_time = current_time - (300)
   power_consumed = get_power_consumed(start_time)
   return jsonify({'power_last_5_min': power_consumed})

@metrics.route('/power-last-hour', methods=['GET'])
def power_last_hour():
   current_time = int(datetime.now().timestamp())
   start_time = current_time - (3600)
   power_consumed = get_power_consumed(start_time)
   return jsonify({'power_last_hour': power_consumed})

@metrics.route('/power-today', methods=['GET'])
def power_today():
   current_time = datetime.now()
   start_time = datetime(current_time.year, current_time.month, current_time.day)
   start_timestamp = int(start_time.timestamp())
   power_consumed = get_power_consumed(start_timestamp)
   return jsonify({'power_today': power_consumed})

@metrics.route('/power-this-week', methods=['GET'])
def power_this_week():
   current_time = datetime.now()
   start_of_week = current_time - timedelta(days=current_time.weekday())
   start_timestamp = int(start_of_week.replace(hour=0, minute=0, second=0, microsecond=0).timestamp())
   power_consumed = get_power_consumed(start_timestamp)
   return jsonify({'power_this_week': power_consumed})

@metrics.route('/total-cost-this-week', methods=['GET'])
def total_cost_this_week():
   cost_per_kwh = 4.42 
   current_time = datetime.now()
   start_of_week = current_time - timedelta(days=current_time.weekday())
   start_timestamp = int(start_of_week.replace(hour=0, minute=0, second=0, microsecond=0).timestamp())
   power_consumed = get_power_consumed(start_timestamp)
   total_cost = round(power_consumed * cost_per_kwh, 2)
   return jsonify({'total_cost': total_cost})


#function for weekly report
weekly_report_cache = {}

#weekly report function and store in cache
def calculate_and_cache_weekly_report():
   global weekly_report_cache  # Only needed inside this function for updating

   conn = get_db_connection()
   c = conn.cursor()

   # Calculate the start and end of the current week
   current_time = datetime.now()
   start_of_week = current_time - timedelta(days=current_time.weekday())
   start_timestamp = int(start_of_week.replace(hour=0, minute=0, second=0, microsecond=0).timestamp())

   # Calculate total power consumed
   total_power_consumed = get_power_consumed(start_timestamp)

   # Calculate total cost
   cost_per_kwh = 4.42
   total_cost = round(total_power_consumed * cost_per_kwh, 2)

   # Calculate averages
   days_elapsed = 7
   average_power_per_day = round(total_power_consumed / days_elapsed, 2)
   average_cost_per_day = round(total_cost / days_elapsed, 2)

   # Update the cache
   weekly_report_cache = {
       'week_start': start_of_week.strftime('%Y-%m-%d'),
       'week_end': (start_of_week + timedelta(days=6)).strftime('%Y-%m-%d'),
       'total_power_consumed': total_power_consumed,
       'total_cost': total_cost,
       'average_power_per_day': average_power_per_day,
       'average_cost_per_day': average_cost_per_day
   }

   conn.close()
   print("Weekly report updated:", weekly_report_cache)

# Function to access the cached data
def get_weekly_report_cache():
   return weekly_report_cache


# Weekly report endpoint
@metrics.route('/weekly-report', methods=['GET'])
def get_weekly_report():
   report_cache = get_weekly_report_cache()
   if not report_cache:
       return jsonify({'message': 'Weekly report not yet generated'}), 404

   return jsonify(report_cache)
