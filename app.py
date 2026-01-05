from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from database import get_db_connection
from metrics import metrics
from metrics import calculate_and_cache_weekly_report, get_weekly_report_cache
from db_operations import database_operations
from apscheduler.schedulers.background import BackgroundScheduler
from algorithm import insert_reading
import sqlite3
import csv
import os

#Initialize flask
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


#Blueprint
app.register_blueprint(metrics)
app.register_blueprint(database_operations)



#scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(func=insert_reading, trigger="interval", minutes=5, id="insert_reading")
scheduler.add_job(calculate_and_cache_weekly_report, 'cron', day_of_week='fri', hour=2, minute=5, id='weekly_report_task')

try:
   scheduler.start()
   print("APScheduler is active and running.")  # Indicate the scheduler is running
except Exception as e:
   print(f"Error starting APScheduler: {e}")


@app.teardown_appcontext
def shutdown_scheduler(exception=None):
   if scheduler.running:  # Ensure the scheduler is running before shutting it down
       scheduler.shutdown()


if __name__ == '__main__':
   app.run(debug=True, port=5002)
