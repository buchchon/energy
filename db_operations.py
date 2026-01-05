from flask import Blueprint, jsonify, request, send_file
import csv
from database import get_db_connection

database_operations = Blueprint('database_operations', __name__)

# Adding a new building
@database_operations.route('/add-building', methods=['POST'])
def add_building():
   data = request.json
   building_id = data.get('building_id')

   if not building_id:
       return jsonify({'error': 'Building ID is required in field'}), 400

   conn = get_db_connection()
   c = conn.cursor()

   c.execute("SELECT * FROM floors WHERE building_ID = ?", (building_id,))
   existing_building = c.fetchone()

   if existing_building:
       return jsonify({'message': 'Building already exists'}), 409

   # Create floor ID as "building_ID_1"
   floor_id = f"{building_id}_1"
  
   # Insert new building with floor "1"
   c.execute("INSERT INTO floors (floor_ID, building_ID) VALUES (?, ?)", (floor_id, building_id))
   conn.commit()
   conn.close()

   return jsonify({'message': 'Building and associated floor added successfully'}), 201

# Adding a new floor
@database_operations.route('/add-floor', methods=['POST'])
def add_floor():
   data = request.json
   floor_id = data.get('floor_id')
   building_id = data.get('building_id')

   if not floor_id:
       return jsonify({'error': 'Floor ID is required in the field'}), 400
   if not building_id:
       return jsonify({'error': 'Building ID is required in the field'}), 400

   conn = get_db_connection()
   c = conn.cursor()

   c.execute("SELECT * FROM floors WHERE floor_ID = ? AND building_ID = ?", (floor_id, building_id))
   existing_floor = c.fetchone()

   if existing_floor:
       conn.close()
       return jsonify({'message': 'Floor already exists in the building'}), 409

   actual_floor_id = f"{building_id}_{floor_id}"

   c.execute("INSERT INTO floors (floor_ID, building_ID) VALUES (?, ?)", (actual_floor_id, building_id))
   conn.commit()
   conn.close()

   return jsonify({'message': f'Floor {actual_floor_id} added successfully to Building {building_id}'}), 201

# Adding a new clamp
@database_operations.route('/add-clamp', methods=['POST'])
def add_clamp():
   data = request.json
   clamp_id = data.get('clamp_id')
   floor_id = data.get('floor_id')

   if not clamp_id:
       return jsonify({'error': 'Clamp ID is required in the field'}), 400
   if not floor_id:
       return jsonify({'error': 'Floor ID is required in the field'}), 400

   conn = get_db_connection()
   c = conn.cursor()

   c.execute("SELECT * FROM clamps WHERE clamp_ID = ? AND floor_ID = ?", (clamp_id, floor_id))
   existing_clamp = c.fetchone()

   if existing_clamp:
       conn.close()
       return jsonify({'message': 'Clamp already exists'}), 409

   c.execute("INSERT INTO clamps (clamp_ID, floor_ID) VALUES (?, ?)", (clamp_id, floor_id))
   conn.commit()
   conn.close()

   return jsonify({'message': f'Clamp {clamp_id} added successfully to Floor {floor_id}'}), 201

# Deleting a clamp
@database_operations.route('/delete-clamp', methods=['POST'])
def delete_clamp():
   data = request.json
   clamp_id = data.get('clamp_id')

   if not clamp_id:
       return jsonify({'error': 'Clamp ID is required in the field'}), 400

   conn = get_db_connection()
   c = conn.cursor()

   c.execute("DELETE FROM clamps WHERE clamp_ID = ?", (clamp_id,))
   c.execute("DELETE FROM readings WHERE clamp_ID = ?", (clamp_id,))
   conn.commit()
   conn.close()

   return jsonify({'message': f'Clamp {clamp_id} deleted successfully'}), 200

# Getting buildings
@database_operations.route('/get-buildings', methods=['GET'])
def get_buildings():
   conn = get_db_connection()
   if conn is None:
       return jsonify({'error': 'Database connection failed'}), 500

   c = conn.cursor()
   c.execute("SELECT DISTINCT building_ID, floor_ID FROM floors")
   buildings = c.fetchall()
   conn.close()

   return jsonify({'buildings': buildings}), 200

# Getting floors
@database_operations.route('/get-floors', methods=['GET'])
def get_floors():
   conn = get_db_connection()
   if conn is None:
       return jsonify({'error': 'Database connection failed'}), 500

   c = conn.cursor()
   c.execute("SELECT floor_ID FROM floors")
   floors = c.fetchall()
   conn.close()

   floors_list = [{'floor_ID': floor[0]} for floor in floors]

   return jsonify({'floors': floors_list}), 200

# Getting clamps
@database_operations.route('/get-clamps', methods=['GET'])
def get_clamps():
   conn = get_db_connection()
   if conn is None:
       return jsonify({'error': 'Database connection failed'}), 500

   c = conn.cursor()
   c.execute("SELECT clamp_ID FROM clamps")
   clamps = c.fetchall()
   conn.close()

   clamps_list = [{'clamp_ID': clamp[0]} for clamp in clamps]

   return jsonify({'clamps': clamps_list}), 200

# Downloading the database
@database_operations.route('/download-database', methods=['GET'])
def download_database():
   conn = get_db_connection()
   if conn is None:
       return jsonify({'error': 'Database connection failed'}), 500

   tables = ['floors', 'clamps', 'readings']
   output_filename = 'database_export.csv'

   with open(output_filename, 'w', newline='') as csvfile:
       csv_writer = csv.writer(csvfile)

       for table in tables:
           csv_writer.writerow([f"Table: {table}"])
           c = conn.cursor()
           c.execute(f"SELECT * FROM {table}")
           rows = c.fetchall()
           columns = [description[0] for description in c.description]
           csv_writer.writerow(columns)
           for row in rows:
               csv_writer.writerow(row)
           csv_writer.writerow([])

   conn.close()

   return send_file(output_filename, as_attachment=True)
