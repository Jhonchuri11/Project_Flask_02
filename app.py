# Importamos flask
from flask import Flask, render_template, request, flash, redirect, url_for
#  importamos para conexion a base de datos
import mysql.connector

# crear una aplicacion para comprobar si estamos en el archivo principal

# nombre de la aplicacion
app = Flask(__name__)

# Configuracion usando Pymysql para conectar db 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'PASSWORD'
app.config['MYSQL_DB'] = 'DATABASE'
app.config['MYSQL_PORT'] = 3306

# Inicializar la conexión MySQL
mysql_conn = mysql.connector.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    database=app.config['MYSQL_DB'],
    port=app.config['MYSQL_PORT']
)

# Definiendo la sesion para la muestra de mensajes con flash
app.secret_key = 'mysecretkey'

# ruta principal
@app.route('/')
def index():
    cursor = mysql_conn.cursor()
    cursor.execute('SELECT * FROM empleado')
    data = cursor.fetchall()
    return render_template("empleado/index.html", empleados = data)


# Ruta para el insertar data 
@app.route('/insert_empleado', methods=['POST'])
def insert():
    if request.method == 'POST':
        detalle = request.form
        nombres = detalle['nombre']
        apellidos = detalle['apellido']
        telefono = detalle['telefono']
        carrera = detalle['carrera']
        pais = detalle['pais']
        cursor = mysql_conn.cursor()
        cursor.execute("INSERT INTO empleado (nombre, apellido, telefono, carrera, pais) VALUES (%s, %s, %s, %s, %s)", (nombres, apellidos,telefono, carrera, pais))
        mysql_conn.commit()
        # Estamos enviando un mensaje al user despues de la insercion de data
        flash('Empleado agregado correctamente!')
        cursor.close()
        # Al usar redirect + url_for en este caso tenemos que pasarle la funcion
        # para que nos pueda redireccionar a este
        return redirect(url_for('index'))
    
#Llamando a un solo dato
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_empleado(id):
    if request.method == "GET":
       cursor = mysql_conn.cursor()
       consulta = "SELECT * FROM empleado WHERE id = %s"
       cursor.execute(consulta, (id,))
       data = cursor.fetchone()
       return render_template('empleado/editar.html', empleados = data)
    elif request.method == "POST":
        nombres = request.form['nombre']
        apellidos = request.form['apellido']
        telefono = request.form['telefono']
        carrera = request.form['carrera']
        pais = request.form['pais']
        cursor = mysql_conn.cursor()
        cursor.execute(""" UPDATE empleado 
                       SET nombre = %s,
                       apellido = %s,
                       telefono = %s,
                       carrera = %s,
                       pais = %s 
                       WHERE id = %s""", 
                       (nombres, apellidos, telefono, carrera, pais, id))
        flash('Empleado actualizdo correctamente!')
        return redirect(url_for('index'))

# Ruta para eliminar empleado
@app.route('/delete/<string:id>')
def delete_client(id):
    cursor = mysql_conn.cursor()
    cursor.execute('DELETE FROM empleado where id = {0}'.format(id))
    mysql_conn.commit()
    flash('Empleado eliminado correctamente!')
    cursor.close()
    return redirect(url_for('index'))

if __name__=='__main__':
    app.run(debug=True, port=5000)



