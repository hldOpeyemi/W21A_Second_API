from flask import Flask, jsonify, make_response, request
from dbhelpers import run_statement, serialize_data
import json

app = Flask(__name__)

item_columns = ['id', 'name', 'description', 'in_stock_quantity', 'created_at']
employee_columns = ['id', 'name', 'position', 'hired_at', 'hourly_wage']
employee_update = ['id', 'name', 'hourly_wage']


@app.get('/api/items')
def get_all_item():
 try: 
   result = run_statement('CALL get_all_items()')
   print(result[0])
   formatted_items = serialize_data(item_columns, result)
   return make_response(formatted_items, 200)
 except Exception as error:
  return make_response(error, 500)


@app.post('/api/item')
def insert_an_item():
 try: 
  name = request.json.get('name')
  description = request.json.get('description')
  in_stock_quantity= request.json.get('in_stock_quantity')
  result = run_statement('CALL insert_and_get_item(?,?,?)', [name, description, in_stock_quantity])
#   formatted_items = serialize_data(result[0])
  return make_response(jsonify(result), 200)
   
 except Exception as error:
  return make_response("this is an error", 200)
 
@app.put('/api/edit/<int:item_id>')
def update_qty(item_id):
 try: 
  in_stock_quantity = request.json.get('in_stock_quantity')
  result = run_statement('CALL update_qty_by_id(?,?)', [item_id, in_stock_quantity])
  return make_response(jsonify(result), 200)
 
 except Exception as error:
  return make_response("error updating quantity", 200)
 
@app.delete('/api/delete/<int:item_id>')
def delete_item(item_id):
 try:
  run_statement('CALL delete_item(?)', [item_id])
  return make_response("Success", 204)
 except:
  return make_response("Error deleting item", 401)
 

# Employee API
 
@app.get('/api/employee/<int:employee_id>')
def get_employee(employee_id):
 try: 
   result = run_statement('CALL rtn_emp_by_id(?)', [employee_id])
   print(result[0])
   formatted_employee = serialize_data(employee_columns, result)[0]
   return make_response(formatted_employee, 200)
 except Exception as error:
  return make_response(error, 500)
 
@app.post('/api/employee')
def add_new_employee():
 try: 
  name = request.json.get('name')
  position = request.json.get('position')
  hourly_wage= request.json.get('hourly_wage')
  result = run_statement('CALL add_and_rtn_newEE(?,?,?)', [name, position, hourly_wage])
#   formatted_items = serialize_data(result[0])
  return make_response(jsonify(result), 200)
   
 except Exception as error:
  return make_response("this is an error", 200)
 
@app.put('/api/update/<int:employee_id>')
def update_wage(employee_id):
 try: 
  hourly_wage = request.json.get('hourly_wage')
  result = run_statement('CALL update_wage_by_id(?,?)', [employee_id, hourly_wage])
  formatted_employee = serialize_data(employee_update, result)[0]
  return make_response(formatted_employee, 200)
 except Exception as error:
  return make_response("error updating employee", 200)
 
@app.delete('/api/delete/employee/<int:employee_id>')
def delete_employee(employee_id):
 try:
  run_statement('CALL delete_employee(?)', [employee_id])
  return make_response("", 204)
 except:
  return make_response("Error deleting item", 401)
 
 
 
app.run(debug=True)