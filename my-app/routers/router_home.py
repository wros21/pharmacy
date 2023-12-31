from app import app
from flask import render_template, request, flash, redirect, url_for, session,  jsonify
from mysql.connector.errors import Error


# Importando cenexión a BD
from controllers.funciones_home import *

PATH_URL_EMPLEADOS = "public/empleados"
PATH_URL_PROVEEDORES = "public/proveedores"
PATH_URL_PRODUCTOS = "public/productos"


#@app.route('/ruta-de-empleados', methods=['GET'])
#def rutaEmpleados():
@app.route('/registrar-empleado', methods=['GET'])
def viewFormEmpleado():
    if 'conectado' in session:
        return render_template(f'{PATH_URL_EMPLEADOS}/form_empleado.html')
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


@app.route('/form-registrar-empleado', methods=['POST'])
def formEmpleado():
    if 'conectado' in session:
        if 'foto_empleado' in request.files:
            foto_perfil = request.files['foto_empleado']
            resultado = procesar_form_empleado(request.form, foto_perfil)
            if resultado:
                return redirect(url_for('lista_empleados'))
            else:
                flash('El empleado NO fue registrado.', 'error')
                return render_template(f'{PATH_URL_EMPLEADOS}/form_empleado.html')
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


@app.route('/lista-de-empleados', methods=['GET'])
def lista_empleados():
    if 'conectado' in session:
        return render_template(f'{PATH_URL_EMPLEADOS}/lista_empleados.html', empleados=sql_lista_empleadosBD())
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


@app.route("/detalles-empleado/", methods=['GET'])
@app.route("/detalles-empleado/<int:idEmpleado>", methods=['GET'])
def detalleEmpleado(idEmpleado=None):
    if 'conectado' in session:
        # Verificamos si el parámetro idEmpleado es None o no está presente en la URL
        if idEmpleado is None:
            return redirect(url_for('inicio'))
        else:
            detalle_empleado = sql_detalles_empleadosBD(idEmpleado) or []
            return render_template(f'{PATH_URL_EMPLEADOS}/detalles_empleado.html', detalle_empleado=detalle_empleado)
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


# Buscadon de empleados
@app.route("/buscando-empleado", methods=['POST'])
def viewBuscarEmpleadoBD():
    resultadoBusqueda = buscarEmpleadoBD(request.json['busqueda'])
    if resultadoBusqueda:
        return render_template(f'{PATH_URL_EMPLEADOS}/resultado_busqueda_empleado.html', dataBusqueda=resultadoBusqueda)
    else:
        return jsonify({'fin': 0})


@app.route("/editar-empleado/<int:id>", methods=['GET'])
def viewEditarEmpleado(id):
    if 'conectado' in session:
        respuestaEmpleado = buscarEmpleadoUnico(id)
        if respuestaEmpleado:
            return render_template(f'{PATH_URL_EMPLEADOS}/form_empleado_update.html', respuestaEmpleado=respuestaEmpleado)
        else:
            flash('El empleado no existe.', 'error')
            return redirect(url_for('inicio'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


# Recibir formulario para actulizar informacion de empleado
@app.route('/actualizar-empleado', methods=['POST'])
def actualizarEmpleado():
    resultData = procesar_actualizacion_form(request)
    if resultData:
        return redirect(url_for('lista_empleados'))


@app.route("/lista-de-usuarios", methods=['GET'])
def usuarios():
    if 'conectado' in session:
        resp_usuariosBD = lista_usuariosBD()
        return render_template('public/usuarios/lista_usuarios.html', resp_usuariosBD=resp_usuariosBD)
    else:
        return redirect(url_for('inicioCpanel'))


@app.route('/borrar-usuario/<string:id>', methods=['GET'])
def borrarUsuario(id):
    resp = eliminarUsuario(id)
    if resp:
        flash('El Usuario fue eliminado correctamente', 'success')
        return redirect(url_for('usuarios'))


@app.route('/borrar-empleado/<string:id_empleado>/<string:foto_empleado>', methods=['GET'])
def borrarEmpleado(id_empleado, foto_empleado):
    resp = eliminarEmpleado(id_empleado, foto_empleado)
    if resp:
        flash('El Empleado fue eliminado correctamente', 'success')
        return redirect(url_for('lista_empleados'))

###Proveedores###
@app.route('/ruta-de-proveedores', methods=['GET'])
#def rutaProveedores():
##@app.route('/registrar-proveedor', methods=['GET'])
def viewFormProveedor():
    if 'conectado' in session:
        return render_template(f'{PATH_URL_PROVEEDORES}/form_proveedor.html')
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


@app.route('/form-registrar-proveedor', methods=['POST'])
def formProveedor():
    if 'conectado' in session:
        if 'foto_proveedor' in request.files:
            foto_perfil = request.files['foto_proveedor']
            resultado = procesar_form_proveedor(request.form, foto_perfil)
            if resultado:
                return redirect(url_for('lista_proveedores'))
            else:
                flash('El proveedor NO fue registrado.', 'error')
                return render_template(f'{PATH_URL_PROVEEDORES}/form_proveedor.html')
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


@app.route('/lista-de-proveedores', methods=['GET'])
def lista_proveedores():
    if 'conectado' in session:
        return render_template(f'{PATH_URL_PROVEEDORES}/lista_proveedores.html', proveedores=sql_lista_proveedoresBD())
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


@app.route("/detalles-proveedor/", methods=['GET'])
@app.route("/detalles-proveedor/<int:idProveedor>", methods=['GET'])
def detalleproveedor(idProveedor=None):
    if 'conectado' in session:
        # Verificamos si el parámetro idproveedor es None o no está presente en la URL
        if idProveedor is None:
            return redirect(url_for('inicio'))
        else:
            detalle_proveedor = sql_detalles_proveedoresBD(idProveedor) or []
            return render_template(f'{PATH_URL_PROVEEDORES}/detalles_proveedor.html', detalle_proveedor=detalle_proveedor)
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


# Buscadon de proveedores
@app.route("/buscando-proveedor", methods=['POST'])
def viewBuscarproveedorBD():
    resultadoBusqueda = buscarproveedorBD(request.json['busqueda'])
    if resultadoBusqueda:
        return render_template(f'{PATH_URL_PROVEEDORES}/resultado_busqueda_proveedor.html', dataBusqueda=resultadoBusqueda)
    else:
        return jsonify({'fin': 0})


@app.route("/editar-proveedor/<int:id>", methods=['GET'])
def viewEditarproveedor(id):
    if 'conectado' in session:
        respuestaproveedor = buscarproveedorUnico(id)
        if respuestaproveedor:
            return render_template(f'{PATH_URL_PROVEEDORES}/form_proveedor_update.html', respuestaproveedor=respuestaproveedor)
        else:
            flash('El proveedor no existe.', 'error')
            return redirect(url_for('inicio'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


# Recibir formulario para actulizar informacion de proveedor
@app.route('/actualizar-proveedor', methods=['POST'])
def actualizarproveedor():
    resultData = procesar_actualizacion_form(request)
    if resultData:
        return redirect(url_for('lista_proveedores'))


@app.route('/borrar-proveedor/<string:id_proveedor>/<string:foto_proveedor>', methods=['GET'])
def borrarproveedor(id_proveedor, foto_proveedor):
    resp = eliminarproveedor(id_proveedor, foto_proveedor)
    if resp:
        flash('El proveedor fue eliminado correctamente', 'success')
        return redirect(url_for('lista_proveedores'))





###Fin proveedores


####Productos ####
@app.route('/ruta-de-productos', methods=['GET'])
#def rutaProductos():
##@app.route('/registrar-producto', methods=['GET'])
def viewFormproducto():
    if 'conectado' in session:
        return render_template(f'{PATH_URL_PRODUCTOS}/form_producto.html')
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


@app.route('/form-registrar-producto', methods=['POST'])
def formproducto():
    if 'conectado' in session:
        if 'foto_producto' in request.files:
            foto_perfil = request.files['foto_producto']
            resultado = procesar_form_producto(request.form, foto_perfil)
            if resultado:
                return redirect(url_for('lista_productos'))
            else:
                flash('El producto NO fue registrado.', 'error')
                return render_template(f'{PATH_URL_PRODUCTOS}/form_producto.html')
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


@app.route('/lista-de-productos', methods=['GET'])
def lista_productos():
    if 'conectado' in session:
        return render_template(f'{PATH_URL_PRODUCTOS}/lista_productos.html', productos=sql_lista_productosBD())
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


@app.route("/detalles-producto/", methods=['GET'])
@app.route("/detalles-producto/<int:idProducto>", methods=['GET'])
def detalleproducto(idProducto=None):
    if 'conectado' in session:
        # Verificamos si el parámetro idproducto es None o no está presente en la URL
        if idProducto is None:
            return redirect(url_for('inicio'))
        else:
            detalle_producto = sql_detalles_productosBD(idProducto) or []
            return render_template(f'{PATH_URL_PRODUCTOS}/detalles_producto.html', detalle_producto=detalle_producto)
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


# Buscadon de productos
@app.route("/buscando-producto", methods=['POST'])
def viewBuscarproductoBD():
    resultadoBusqueda = buscarproductoBD(request.json['busqueda'])
    if resultadoBusqueda:
        return render_template(f'{PATH_URL_PRODUCTOS}/resultado_busqueda_producto.html', dataBusqueda=resultadoBusqueda)
    else:
        return jsonify({'fin': 0})


@app.route("/editar-producto/<int:id>", methods=['GET'])
def viewEditarproducto(id):
    if 'conectado' in session:
        respuestaproducto = buscarproductoUnico(id)
        if respuestaproducto:
            return render_template(f'{PATH_URL_PRODUCTOS}/form_producto_update.html', respuestaproducto=respuestaproducto)
        else:
            flash('El producto no existe.', 'error')
            return redirect(url_for('inicio'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


# Recibir formulario para actulizar informacion de producto
@app.route('/actualizar-producto', methods=['POST'])
def actualizarproducto():
    resultData = procesar_actualizacion_form(request)
    if resultData:
        return redirect(url_for('lista_productos'))


@app.route('/borrar-producto/<string:id_producto>/<string:foto_producto>', methods=['GET'])
def borrarproducto(id_producto, foto_producto):
    resp = eliminarproducto(id_producto, foto_producto)
    if resp:
        flash('El producto fue eliminado correctamente', 'success')
        return redirect(url_for('lista_productos'))



### fin productos###"""


@app.route("/descargar-informe-empleados/", methods=['GET'])
def reporteBD():
    if 'conectado' in session:
        return generarReporteExcel()
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))
