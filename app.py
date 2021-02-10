from flask import Flask, render_template, jsonify, request
from flask_mysqldb import MySQL,MySQLdb 

# Create a flask instance 
app = Flask(__name__)

# Set flask configuration variables for flask to use as MySQL Authentication 
app.config['MYSQL_HOST'] = '172.17.0.2'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'inventory'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Create a MySQL instance
mysql = MySQL(app)
   
# Define subroutine to run on loading the page root
@app.route('/')
def main():
    
    # We use the cursor to run commands like we are on the MySQL command line
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    result = cursor.execute("SELECT * FROM type ORDER BY id")
    
    # We return the value of the query to a variable (this populates the first dropdown menu)
    systems = cursor.fetchall()

    # The variable is passed to render_template, changing elements on the template html document to match.
    return render_template('index.html', systems=systems)
 

# Define subroutine to run on request to /system_type
@app.route("/system_type",methods=["POST","GET"])
def system_type():  
    cursor = mysql.connection.cursor()
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    # We expect POST requests to this endpoint from the JavaScript function running on the webpage.
    # The information returned will populate the second dropdown 
    if request.method == 'POST':
        category_id = request.form['category_id'] 
        result = cur.execute("SELECT * FROM devices WHERE id = %s ORDER BY device_name ASC", [category_id])
        device_list = cur.fetchall()  
        OutputArray = []
        for row in device_list:
            outputObj = {
                'id': row['id'],
                'name': row['device_name']}
            OutputArray.append(outputObj)
    
    # Return data formatted as JSON
    return jsonify(OutputArray)

# Define subroutine to run on POST request to /device_description
@app.route("/device_description",methods=["POST","GET"])
def device_description():  
    cursor = mysql.connection.cursor()
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        
        # Return query results based on device name
        category_id = request.form['device_name'] 
        result = cur.execute("SELECT description FROM devices WHERE device_name = %s", [category_id])
        db_description = cur.fetchall()
        for item in db_description:
            description = item.get('description')
        
        # Return data formatted as JSON
        return jsonify(description)
        
if __name__ == '__main__':
    app.run(debug=True)
