from flask import Flask, session
from datetime import datetime
import json
from model.config import Db

class Usuarios():
	# inicio de sesion en el formulario
    def inicio_sesion(self, usuario, contrasena):
        datos_usu = Db().fetchall("SELECT id_usuario, usuario, contrasena, fk_role FROM usuarios WHERE usuario = '"+usuario+"'")
        contra = ""
        for row in datos_usu:
            contra = row[2]
        if contrasena == contra:
            session['id_usu_log'] = row[0]
            session['usu_log'] = row[1]
            session['fk_role'] = row[3]
            return True
        else:
            return False
    # registrar un usuario
    def registrar_usuario(self, nombre, cedula, usuario, contrasena, correo):
        guar_usu = Db().insertar("INSERT INTO usuarios (nombre, cedula, usuario, correo, contrasena, fk_role) VALUES ('"+ nombre +"', '"+ cedula +"', '"+ usuario +"', '"+ correo +"', '"+ contrasena +"', 2)")
        return guar_usu
    # bombonas por persona
    def bombonas_todas(self):
        json_data = []
        datos_db = Db().fetchall("SELECT usuarios.id_usuario, tamano_bombona.nombre, estatus_bombona.descripcion, estatus_bombona.id_estatus, entrega_bombona.id_entraga_bombona FROM entrega_bombona INNER JOIN tamano_bombona ON tamano_bombona.id_bombona = entrega_bombona.fk_tamano INNER JOIN estatus_bombona ON estatus_bombona.id_estatus = entrega_bombona.fk_estatus_bombona INNER JOIN usuarios ON usuarios.id_usuario = entrega_bombona.fk_usuario WHERE fk_usuario = "+ str(session['id_usu_log']) +"")
        print("si corrio")
        n = 0
        for row in datos_db:
            n = n + 1
            json_data.append({                
                "num": str(n), 
                "tamano_bombona": row[1],
                "estatus": row[2],
                "id_estatus": row[3],
                "id_entrega_bombona": row[4]
                })
        return json_data
    # datos de un usuario en espesifico
    def datos_usuario(self):
        datos_usuario = Db().fetchall("SELECT nombre, cedula FROM usuarios WHERE id_usuario  = "+ str(session['id_usu_log']) +"")
        return datos_usuario
    # cantidad de bombonas por usuario
    def catn_bombonas_usu(self):
        catn_bombonas_usu =  Db().fetchall("select fk_usuario FROM entrega_bombona where fk_usuario = "+ str(session['id_usu_log']) +"")
        n = 0
        for row in catn_bombonas_usu:
            n = n + 1
        return str(n)
    # mostrar tamaño de bombonas
    def mos_tama_bombo(self):
        mos_tama_bombo = Db().fetchall("SELECT * FROM tamano_bombona")
        return mos_tama_bombo
    # insertar bombona de un usuario por si solo
    def guardar_bom(self, tamano_bom):
        bom_guardado = Db().insertar("INSERT INTO entrega_bombona (fk_usuario, fk_tamano, fk_estatus_bombona) VALUES ("+ str(session['id_usu_log']) +", "+ str(tamano_bom) +", 2)")
        return bom_guardado
    # eliminar bombona de un usuario en espesifico, como cliente
    def eliminar_bombona(self, id_bom):
        eli_bom = Db().insertar("DELETE FROM entrega_bombona WHERE id_entraga_bombona = "+ str(id_bom) +"")
        return eli_bom
    