from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Lista para almacenar los favoritos en memoria
favoritos = []

# Ruta para mostrar los favoritos de un usuario
@app.route('/usuarios/<int:id_usuario>/favoritos', methods=['GET'])
def ver_favoritos(id_usuario):
    # Filtrar los favoritos que pertenecen al usuario actual
    favoritos_usuario = [f for f in favoritos if f['id_usuario'] == id_usuario]
    return render_template('index.html', favoritos=favoritos_usuario, id_usuario=id_usuario)

# Ruta para añadir un favorito
@app.route('/usuarios/<int:id_usuario>/favoritos', methods=['POST'])
def agregar_favorito(id_usuario):
    titulo_libro = request.form.get('titulo_libro')
    autor = request.form.get('autor')
    
    # Validar que ambos campos no estén vacíos
    if titulo_libro and autor:
        # Generar un ID único para el favorito
        nuevo_id = len(favoritos) + 1 if favoritos else 1
        nuevo_favorito = {
            'id_favorito': nuevo_id,
            'id_usuario': id_usuario,
            'titulo_libro': titulo_libro,
            'autor': autor
        }
        favoritos.append(nuevo_favorito)
        return redirect(url_for('ver_favoritos', id_usuario=id_usuario))
    else:
        # Si los campos están vacíos, redirigir con un mensaje de error (podemos mejorar esto luego)
        return redirect(url_for('ver_favoritos', id_usuario=id_usuario))

# Ruta para eliminar un favorito
@app.route('/usuarios/<int:id_usuario>/favoritos/<int:id_favorito>', methods=['POST'])
def eliminar_favorito(id_usuario, id_favorito):
    global favoritos
    # Filtrar y mantener solo los favoritos que no coinciden con el id_favorito
    favoritos = [f for f in favoritos if not (f['id_usuario'] == id_usuario and f['id_favorito'] == id_favorito)]
    return redirect(url_for('ver_favoritos', id_usuario=id_usuario))

if __name__ == '__main__':
    app.run(debug=True)
