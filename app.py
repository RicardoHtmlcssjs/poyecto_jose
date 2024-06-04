from flask import Flask, render_template, request, session, redirect, session
from model.class_acciones import Acciones
from model.class_usuario import Usuarios
from model.config import Db

app = Flask(__name__)
app.secret_key = "abc1234"
# ruta raiz
@app.route("/")
def index():
    # si la sesion esta creada redirecionara a inicio
    if Acciones().session() == True:
        return redirect('/inicio')
    else:
        return render_template('index.html', login = 0)

# enviar formulario de inicio de sesion
@app.route("/ini_sesion_usu", methods=['POST'])
def ini_sesion_usu():
    usuario = request.form['usuario']
    contrasena = request.form['contrasena']
    # si algun campo esta vacio
    if Acciones().val_cam_vacio(usuario) == False or Acciones().val_cam_vacio(contrasena) == False:
        return render_template('index.html', log_error=1, text_error='Algun campo esta vacio', usuario=usuario)
    login = Usuarios().inicio_sesion(usuario, contrasena)
    # si el usuario inicia sesion correctamente redirecionara a inicio
    if login == True:
        return redirect('/inicio')
    else:
        return render_template('index.html', log_error=1, text_error='Usuario o contraseña incorrecto', usuario=usuario)

# personal se accede como CLIENTE
@app.route("/inicio")
def inicio():
    #si la sesion no esta creada redirecionara a index
    if Acciones().session() == False:
        return redirect("/")
    else:
    #     if session['fk_role'] == 1:
    #         return redirect('/administrador/personal')
    #     else:
            # return redirect('/inicio')
        return render_template('inicio.html', llamar_metodo="ajax.tabla_bombonas", datos_usu = Usuarios().datos_usuario(), datos_cad_bom = Usuarios().catn_bombonas_usu())

# mostrar datos de la persona de sus bombonas
# clientes tabla pagos realizados
@app.route("/bombonas_todas", methods=["POST"])
def bombonas_todas():
    return Usuarios().bombonas_todas()

# agregar bombona como cliente
@app.route("/agregar_bombona")
def agregar_bombona():
    return render_template('agregar_bombona.html', tama_bom = Usuarios().mos_tama_bombo())

# guardar bombona como cliente
@app.route("/guardar_bombona", methods=["POST"])
def guardar_bombona():
    tamano_bom = request.form['tamano_bom']
    insert = Usuarios().guardar_bom(tamano_bom)
    return redirect("/inicio")
# cerrar session y destruir
@app.route("/cerrar_session")
def cerrar_session():
    Acciones().cerrar_session()
    return redirect('/')


#ini servidor
if __name__ == '__main__':
    app.run(port=5000, debug=True)