
from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail,Message
from itsdangerous import URLSafeTimedSerializer
from itsdangerous.exc import BadSignature
import matplotlib.pyplot as plt
import os

directorio_guardado = os.path.join(os.path.dirname(__file__), 'app', 'static', 'img')

app = Flask(__name__, static_url_path='/static')

#configurar conexion de la bd
app.config['SECRET_KEY'] = '315859351'

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="gestionar"
)
cursor = db.cursor()

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'garciacacher@gmail.com'
app.config['MAIL_PASSWORD'] = 'vmci dxui pznv goxy'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEFAULT_SENDER'] = 'garciacacher@gmail.com'

mail = Mail(app)
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

cursor = db.cursor()

#crear ruta
@app.route('/registrouser',methods=['GET', 'POST'])
def Resgistro_usuario():
    if request.method == 'POST':
        nombreusuario = request.form.get('nombre_user')
        apellidousuario = request.form.get('apellido_user')
        emailusuario = request.form.get('email_user')
        usuario  = request.form.get('usuario_user')
        contrasena = request.form.get('contraseña_user')
        rol = request.form.get('rol_user')
        cecriptar = generate_password_hash(contrasena)

        #verficar si el usuario y email existen
        cursor = db.cursor()
        cursor.execute("SELECT * FROM usuario WHERE usuario_user = %s OR email_user = %s",(usuario,emailusuario))
        resultado = cursor.fetchone()
        if resultado:
            print("Usuario o email ya esta registrado")
            return render_template('registrouser.html')
            #insertar los usuario en la bd
        else:
            cursor.execute("INSERT INTO usuario(nombre_user,apellido_user,email_user,usuario_user,contraseña_user,rol_user)VALUES(%s,%s,%s,%s,%s,%s)",(nombreusuario,apellidousuario,emailusuario,usuario,cecriptar,rol))
            db.commit()
            print("Usuario registrado")
            return redirect(url_for('Resgistro_usuario'))

    return render_template('registrouser.html')
#ruta2 verificacion de usuario de acuerdo al rol
@app.route('/',methods=['GET', 'POST'])
def login():
    
    usuario = request.form.get('usuario_user')
    contrasena = request.form.get('contraseña_user')

    cursor = db.cursor(dictionary=True)
    consulta = "SELECT usuario_user, contraseña_user, rol_user FROM usuario WHERE usuario_user = %s"
    cursor.execute(consulta, (usuario,))
    usuarios = cursor.fetchone()
    print(usuarios)
    print(contrasena)

    if usuarios and check_password_hash(usuarios['contraseña_user'], contrasena):
        # crear la sesión
        session['usuario'] = usuarios['usuario_user']
        session['rol'] = usuarios['rol_user']

        if usuarios['rol_user'] == 'administrador':
            print("inicio correcto")
            return render_template('registrot.html')
        else:
            return render_template('principaluser.html')
    else:
        print("Credenciales inválidas")
        return render_template('index.html')

    return render_template('index.html')

#olvido contraseña
def enviar_correo(email):
    token = serializer.dumps(email, salt='restablecimiento de contraseña')
    enlace = url_for('restablecer_contraseña', token=token, _external=True)
    mensaje = Message(subject='Restablecimiento de contraseña', recipients=[email], body=f'Para restablecer contraseña, click en el siguiente enlace: {enlace}')
    mail.send(mensaje)

@app.route("/recuperar_contraseña", methods=['GET', 'POST'])
def recuperar_contraseña():
    if request.method == 'POST':
        email = request.form['email_user']
        enviar_correo(email)
        return redirect(url_for('login'))
    return render_template('recuperar_contraseña.html')

@app.route("/restablecer_contraseña/<token>", methods=['GET', 'POST'])
def restablecer_contraseña(token):
    if request.method == 'POST':
        nueva_c = request.form['nueva_c']
        confirmar_c = request.form['confirmar_c']

        if nueva_c != confirmar_c:
            return 'Las contraseñas no son iguales'

        nueva_pass = generate_password_hash(nueva_c)

        cursor = db.cursor()
        email = serializer.loads(token, salt='restablecimiento de contraseña', max_age=3600)
        consulta = "UPDATE usuario SET contraseña_user = %s WHERE email_user = %s"
        cursor.execute(consulta, (nueva_pass, email))
        db.commit()
        return redirect(url_for('login'))

    return render_template('restablecer_contraseña.html')



#ruta 3
@app.route("/salir")
def salir():
    session.pop('usuario',None)
    return redirect(url_for('login'))
#no almacena el cache
@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-cache,no-store,must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = 0
    
    return response
#listar usuarios
@app.route('/lista', methods=['GET', 'POST'])
def lista():
    cursor=db.cursor()
    cursor.execute('SELECT * FROM usuario')
    usuarios = cursor.fetchall()
    return render_template('registrot.html', usuarios = usuarios)

@app.route("/listaT", methods=['GET','POST'])
def listaT():
    cursor=db.cursor()
    cursor.execute('SELECT * FROM tareas')
    tareas = cursor.fetchall()
    return render_template('registrot.html', tareas = tareas)

@app.route("/listaTU", methods=['GET','POST'])
def listaTU():
    username = session.get('usuario')
    cursor=db.cursor()
    cursor.execute('SELECT * FROM tareas WHERE id_user = (SELECT id_user FROM usuario WHERE usuario_user = %s)', (username,))
    tareas = cursor.fetchall()
    print(tareas)
    return render_template('principaluser.html', tareas=tareas)

#eliminar usuario
@app.route("/eliminarusu/<int:id>", methods=['GET'])
def eliminarusuario(id):
    cursor = db.cursor()
    cursor.execute('DELETE FROM usuario WHERE id_user = %s',(id,))
    db.commit()
    print("Usuario eliminado")
    return redirect(url_for('lista'))
#eliminar tarea
@app.route("/eliminart/<int:id>", methods=['GET'])
def eliminart(id):
    cursor = db.cursor()
    if 'rol_user' == 'administrador':
        cursor.execute('DELETE FROM tareas WHERE id_tarea = %s',(id,))
        db.commit()
        print("Tarea eliminada")
        return redirect(url_for('listaT'))
    else:
        cursor.execute('DELETE FROM tareas WHERE id_tarea = %s',(id,))
        db.commit()
        print("Tarea eliminada")
        return redirect(url_for('listaTU'))
#eliminar tarea usuario
@app.route("/eliminartusu/<int:id>", methods=['GET'])
def eliminartusu(id):
    cursor = db.cursor()
    cursor.execute('DELETE FROM tareas WHERE id_tarea = %s',(id,))
    db.commit()
    print("Tarea eliminada")
    return redirect(url_for('listaTU'))
#buscar tarea
@app.route("/buscar_tarea", methods =['POST'])
def buscar_tareas():
    busqueda = request.form.get('busqueda')

    cursor = db.cursor(dictionary=True)
    consulta = 'SELECT * FROM tareas WHERE id_tarea = %s OR nombre LIKE %s'
    cursor.execute(consulta,(busqueda,"%" + busqueda + "%"))
    tareas = cursor.fetchall()
    return render_template('Resultadob.html', tareas=tareas, busqueda=busqueda)
#buscar tarea en usuario
@app.route("/buscar_tareatu", methods=['POST'])
def buscar_tareastu():
    busquedatu = request.form.get('busquedatu')
    nombre_usuario = session.get('usuario')


 # Asegúrate de que busquedatu y id_user no sean None
    cursor = db.cursor(dictionary=True)
    consulta_user = 'SELECT id_user FROM usuario WHERE usuario_user = %s'
    cursor.execute(consulta_user, (nombre_usuario,))
    result = cursor.fetchone()
    if result:
        id_user = result['id_user']
        consulta = 'SELECT * FROM tareas WHERE (id_tarea = %s OR nombre LIKE %s) AND id_user = %s'
        cursor.execute(consulta, (busquedatu, "%" + busquedatu + "%", id_user))
        tareas = cursor.fetchall()
        
        # Verificar el resultado de la consulta
        if tareas:
            print(f"Tareas encontradas: {tareas}")
        else:
            print("No se encontraron tareas.")
        
        return render_template('Resultadob.html', tareas=tareas, busquedatu=busquedatu)
    else:
        return "Usuario no encontrado", 404


#buscar usuario
@app.route("/buscar_usuario", methods=['POST'])
def buscar_usuario():
    busquedau = request.form.get('busquedau')

    cursor = db.cursor(dictionary=True)
    consulta = 'SELECT * FROM usuario WHERE id_user = %s OR usuario_user LIKE %s'
    cursor.execute(consulta,(busquedau, "%" + busquedau + "%"))
    usuarios = cursor.fetchall()

    return render_template('Resultadou.html', usuarios= usuarios, busquedau= busquedau)
#editar usuario
@app.route("/editarusuario/<int:id>", methods=('GET', 'POST'))
def editarusuario(id):
       

        if request.method == 'POST':
            nombreusu = request.form['nombre_user']
            apellidousu = request.form['apellido_user']
            email = request.form['email_user']
            usuario = request.form['usuario_user']
            contrasena = request.form['contraseña_user']
            rol = request.form['rol_user']
            
            cursor = db.cursor()
            sql ="UPDATE usuario SET nombre_user = %s, apellido_user = %s, email_user = %s, usuario_user = %s, contraseña_user = %s, rol_user = %s WHERE id_user = %s"
            cursor.execute(sql,(nombreusu,apellidousu,email,usuario,contrasena,rol,id))
            db.commit()
            return redirect(url_for('lista'))
    
        else:
             cursor = db.cursor()
             cursor.execute('SELECT * FROM usuario WHERE id_user = %s',(id,))
             data=cursor.fetchall() 
             cursor.close()

             return render_template('modalusu.html', usuarios=data[0]) 
        
        
#editar tarea
@app.route("/editart/<int:id>", methods=['GET', 'POST'])
def editart(id):


    if request.method == 'POST':
        nombretar = request.form['nombre']
        fechainicio = request.form['fechainicio']
        fechafinal = request.form['fechafinal']
        estado = request.form.get('estado')


        if 'rol_user' == 'administrador':
            cursor = db.cursor()
            sql = "UPDATE tareas SET nombre = %s, fechainicio = %s, fechafinal = %s, estado = %s WHERE id_tarea = %s"
            cursor.execute(sql, (nombretar, fechainicio, fechafinal, estado, id))
            db.commit()
            print("Tarea editada")
            return redirect(url_for('listaT'))
        else:
              cursor = db.cursor()
        sql = "UPDATE tareas SET nombre = %s, fechainicio = %s, fechafinal = %s, estado = %s WHERE id_tarea = %s"
        cursor.execute(sql, (nombretar, fechainicio, fechafinal, estado, id))
        db.commit()
        print("Tarea editada")
        return redirect(url_for('listaTU'))
    else:
        cursor = db.cursor()
        cursor.execute('SELECT * FROM tareas WHERE id_tarea = %s', (id,))
        data = cursor.fetchall()
        cursor.close()

        return render_template('modaltareas.html', tareas=data[0])

#editar tarea usuaria
@app.route("/editartusu/<int:id>", methods=['GET', 'POST'])
def editartusu(id):


    if request.method == 'POST':
        nombretar = request.form['nombre']
        fechainicio = request.form['fechainicio']
        fechafinal = request.form['fechafinal']
        estado = request.form.get('estado')
        

        cursor = db.cursor()
        sql = "UPDATE tareas SET nombre = %s, fechainicio = %s, fechafinal = %s, estado = %s WHERE id_tarea = %s"
        cursor.execute(sql, (nombretar, fechainicio, fechafinal, estado, id))
        db.commit()
        print("Tarea editada")
        return redirect(url_for('listaTU'))
    else:
        cursor = db.cursor()
        cursor.execute('SELECT * FROM tareas WHERE id_tarea = %s', (id,))
        data = cursor.fetchall()
        cursor.close()

        return render_template('modaltareasusu.html', tareas=data[0])
    
#crear las url
@app.route('/registrot', methods=['GET' ,'POST'])
def registrartarea():
    if request.method == 'POST':
        nombret = request.form.get('nombre')
        fechai = request.form.get('fechainicio')
        fechaf = request.form.get('fechafinal')
        estado = request.form.get('estado')
        cursor = db.cursor()
        #verficar el nombre de la tarea no este registrado
        cursor.execute('SELECT * FROM tareas WHERE nombre = %s ', (nombret,))
        
        existe = cursor.fetchone()
        if existe:
            print("Nombre de la tarea ya registrado")
            return render_template('registrot.html')
        else:  
            username = session.get('usuario')
            cursor.execute('SELECT id_user FROM usuario WHERE usuario_user = %s', (username,))
            id_user = cursor.fetchone()[0] 
        #insetar las tareas a la tabla tareas de la db
            cursor.execute("INSERT INTO tareas (nombre,fechainicio,fechafinal,estado,id_user) VALUES(%s,%s,%s,%s,%s)",(nombret,fechai,fechaf,estado,id_user))
            db.commit()
            print("Tarea registrada con exito")
            return render_template('registrot.html')
    return render_template('registrot.html')

@app.route('/registrotu', methods=['GET' ,'POST'])
def registrartareau():
    if request.method == 'POST':
        nombret = request.form.get('nombre')
        fechai = request.form.get('fechainicio')
        fechaf = request.form.get('fechafinal')
        estado = request.form.get('estado')
        cursor = db.cursor()
        #verficar el nombre de la tarea no este registrado
        cursor.execute('SELECT * FROM tareas WHERE nombre = %s ', (nombret,))
        
        existe = cursor.fetchone()
        if existe:
            print("Nombre de la tarea ya registrado")
            return render_template('principaluser.html')
        else: 
            username = session.get('usuario')
            cursor.execute('SELECT id_user FROM usuario WHERE usuario_user = %s', (username,))
            id_user = cursor.fetchone()[0] 
        #insetar las tareas a la tabla tareas de la db
            cursor.execute("INSERT INTO tareas (nombre,fechainicio,fechafinal,estado,id_user) VALUES(%s,%s,%s,%s,%s)",(nombret,fechai,fechaf,estado,id_user))
            db.commit()
            print("Tarea registrada con exito")
            return render_template('principaluser.html')
    return render_template('principaluser.html')

directorio_guardado = "C:/Users/FUNCIONARIO/Desktop/gestor de tareas/app/static/img"

@app.route('/tabla_tareas', methods=['GET', 'POST'])
def tabla_tareas():
    cursor = db.cursor()

   
    cursor.execute("SELECT COUNT(*) FROM usuario")
    usuarios_registrados = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tareas WHERE estado='completada'")
    completadas = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tareas WHERE estado='en_progreso'")
    en_proceso = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tareas WHERE estado='pendiente'")
    pendientes = cursor.fetchone()[0]

    cursor.close()

    # Datos para el gráfico de barras
    categorias = ['Usuarios Registrados', 'Tareas Completadas', 'Tareas en Proceso', 'Tareas Pendientes']
    valores = [usuarios_registrados, completadas, en_proceso, pendientes]

    # Generar el gráfico de barras
    plt.figure(figsize=(8, 6))
    plt.bar(categorias, valores, color=['blue', 'green', 'orange', 'red'])
    plt.xlabel('Categorías')
    plt.ylabel('Cantidad')
    plt.title('Usuarios y Tareas')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Guardar el gráfico como imagen
    if not os.path.exists(directorio_guardado):
        os.makedirs(directorio_guardado)
    
    imagen_path = os.path.join(directorio_guardado, 'grafico.png')
    plt.savefig(imagen_path)
    plt.close()

    print(f"Imagen guardada en: {imagen_path}")


    return render_template('tabla_tareas.html', imagen_path='/static/img/grafico.png')

directorio_guardado1 = "C:/Users/FUNCIONARIO/Desktop/gestor de tareas/app/static/img2"

@app.route('/tareas_usuario', methods=['GET', 'POST'])
def tareas_usuario():
    if 'usuario' in session:
        usuario = session['usuario']

        cursor = db.cursor()

        # Consulta para obtener el número de tareas por estado para el usuario específico
        consulta = """
            SELECT estado, COUNT(*) AS cantidad 
            FROM tareas 
            WHERE id_user = (SELECT id_user FROM usuario WHERE usuario_user = %s)
            GROUP BY estado
        """
        cursor.execute(consulta, (usuario,))
        resultados = cursor.fetchall()

        cursor.close()

        estados = []
        cantidades = []

        for estado, cantidad in resultados:
            estados.append(estado)
            cantidades.append(cantidad)

        # Generar la gráfica de barras
        plt.figure(figsize=(8, 6))
        plt.bar(estados, cantidades, color=['blue', 'green', 'orange', 'red'])
        plt.xlabel('Estados de Tareas')
        plt.ylabel('Cantidad')
        plt.title(f'Tareas Registradas por Estado (Usuario: {usuario})')
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Guardar la gráfica como imagen en el directorio correspondiente

        if not os.path.exists(directorio_guardado1):
            os.makedirs(directorio_guardado1)

        imagen_path = os.path.join(directorio_guardado1, f'grafico_usuario_{usuario}.png')
        plt.savefig(imagen_path)
        plt.close()

        # Renderizar la plantilla HTML con la gráfica
        return render_template('tareas_usuario.html', imagen_path=f'/static/img2/grafico_usuario_{usuario}.png', usuario=usuario)

    # Si no hay usuario en la sesión, redirigir a la página de inicio de sesión
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
    app.add_url_rule('/', view_func=login)