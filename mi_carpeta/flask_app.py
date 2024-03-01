from flask import Flask, request, send_file, render_template_string
import os
import pandas as pd
import re

app = Flask(__name__)

# Define la ruta absoluta para la carpeta de 'uploads'
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')

# Verifica si la carpeta de 'uploads' existe, si no, la crea
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']

        # Verificación del tipo de archivo (debe ser .csv)
        if not file or not file.filename.endswith('.csv'):
            return '''
            <!doctype html>
            <html>
            <head>
                <title>Formato de Archivo Incorrecto</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        background-color: #fff3cd;
                        color: #856404;
                        text-align: center;
                        padding: 50px;
                    }
                    h1 {
                        color: #721c24;
                    }
                    p {
                        font-size: 1.1em;
                    }
                </style>
            </head>
            <body>
                <h1>Formato de Archivo Incorrecto</h1>
                <p>Por favor, sube un archivo en formato .csv.</p>
                <img src="https://cdn.dribbble.com/users/2469324/screenshots/6538803/comp_3.gif" alt="Error" style="margin-top: 20px; height: 200px;">
            </body>
            </html>
            '''

        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        tipo_archivo = request.form.get('tipo-archivo', 'biblia-academica')

        try:
            df = pd.read_csv(filepath, encoding='utf-8', sep=',', quotechar='"')
            for columna in df.columns:
                df[columna] = df[columna].apply(limpiar_y_formatear_valor)
            if tipo_archivo == 'biblia-academica':
                columnas_requeridas = [
                    "Ciclo Lectivo", "Organización Académica Curso", "Nro Catalogo", "Créd Curso",
                    "Estado del Curso", "Id Estudiante", "Nombres y Apellidos", "Grado Académico Unificado",
                    "Programa Académico Unificado", "Definitiva", "Tipo documento", "documento",
                    "PCN", "PLC", "PMA", "PSC", "estrato", "val_matricula", "Ciudad", "Departamento",
                    "calendario colegio", "periodo ingreso", "exámen de conocimiento física",
                    "exámen de conocimiento química", "exámen de conocimiento matemáticas"
                ]
            elif tipo_archivo == 'matriculados-otras-universidades':
                columnas_requeridas = [
                    "INSTITUCIÓN DE EDUCACIÓN SUPERIOR (IES)", "PRINCIPAL O SECCIONAL", "SECTOR IES", "IES ACREDITADA",
                    "CARACTER IES", "DEPARTAMENTO DE DOMICILIO DE LA IES", "MUNICIPIO DE DOMICILIO DE LA IES",
                    "PROGRAMA ACADÉMICO", "PROGRAMA ACREDITADO", "NIVEL ACADÉMICO", "NIVEL DE FORMACIÓN", "METODOLOGÍA",
                    "ÁREA DE CONOCIMIENTO", "NÚCLEO BÁSICO DEL CONOCIMIENTO (NBC)", "DESC CINE CAMPO AMPLIO",
                    "DEPARTAMENTO DE OFERTA DEL PROGRAMA", "MUNICIPIO DE OFERTA DEL PROGRAMA", "SEXO", "AÑO", "SEMESTRE",
                    "CANTIDAD", "Política de admisión"
                    ]
            elif tipo_archivo == 'tipo-generico':
                # No necesita verificar las columnas, así que simplemente prosigue con la limpieza
                pass

            columnas_faltantes = [columna for columna in columnas_requeridas if columna not in df.columns]
            if len(columnas_faltantes) > 0:
                mensaje_error = '''
                <!doctype html>
                <html>
                <head>
                    <title>El archivo no contiene las siguientes columnas requeridas</title>
                    <style>
                        body {
                            font-family: Arial, sans-serif;
                            background-color: #f0f8ff;
                            color: #2e3a4d;
                            text-align: center;
                            padding: 50px;
                        }

                        h1 {
                            color: #721c24;
                        }

                        ul {
                            list-style-type: none;
                            padding: 0;
                        }

                        li {
                            background-color: #EFEFEF;
                            margin: 5px;
                            padding: 10px;
                            border-radius: 5px;
                            display: inline-block;
                        }
                    </style>
                </head>
                <body>
                    <h1>El archivo no contiene las siguientes columnas requeridas</h1>
                    <p>Por favor, agrega las siguientes columnas o revisa la ortografía de los nombres</p>
                    <ul>
                '''

                for columna in columnas_faltantes:
                    mensaje_error += '<li>{}</li>'.format(columna)

                mensaje_error += '''
                    </ul>
                    <img src="https://cloud.educaplay.com/recursos/356/11406016/image6205df7f1b090.gif" alt="Error" style="margin-top: 10px; height: 200px;">
                </body>
                </html>
                '''
                return mensaje_error

            if tipo_archivo == 'biblia-academica':
                valores_con_numeros = []
                def limpiar_y_detectar_numeros(valor):
                    try:
                        float(valor)
                        valores_con_numeros.append(valor)
                    except :
                        valor_limpio = valor.strip().upper()
                        return valor_limpio

                df['Tipo documento'].apply(limpiar_y_detectar_numeros).astype(str)

                if len(valores_con_numeros)>0:
                    primer_valor_con_problema = valores_con_numeros[0]
                    tipodocumento = f"""
                            Se detectaron valores con formatos incorrectos en la columna 'Tipo documento', por ejemplo: {primer_valor_con_problema}.\n
                            Las filas que contenían estos valores han sido eliminadas del archivo.
                            \n\n
                            Si desea conservar todas las filas, le sugerimos revisar el archivo original y dirigirse a la página principal para cargarlo nuevamente.\n
                            En caso contrario, el archivo ha sido procesado y está listo para su descarga.
                            """

                else:
                    df['Tipo documento'] = df['Tipo documento'].apply(limpiar_y_detectar_numeros).astype(str)
                    tipodocumento = ""


        except Exception as e:
            return "Hubo un error al leer el archivo: " + str(e)
        return (
        '<!doctype html>'
        '<html>'
        '<head>'
        '<title>Archivo Procesado con Éxito</title>'
        '<style>'
        'body {'
        'font-family: Arial, sans-serif;'
        'background-color: #f8f8f8;'
        'text-align: center;'
        'padding: 50px;'
        '}'
        'h1 {'
        'color: #333;'
        '}'
        '.download-button {'
        'display: inline-block;'
        'margin-top: 20px;'
        'padding: 10px 20px;'
        'background-color: #98FB98; /* Color pastel */'
        'color: white;'
        'border: none;'
        'border-radius: 4px;'
        'text-decoration: none;'
        'font-size: 1.2em;'
        '}'
        '.download-button:hover {'
        'background-color: #98FB98; /* Color pastel más claro */'
        '}'
        '</style>'
        '</head>'
        '<body>'
        '<h1>Archivo Procesado con Éxito</h1>'
        f'<a href="/download/{file.filename}" class="download-button">Descargar Archivo Procesado</a>'
        '<div class="mensaje-container">'
        f'<p>{tipodocumento}</p>'  # Inserta el mensaje aquí
        '</div>'
        '<img src="https://cdn-icons-gif.flaticon.com/11614/11614843.gif" alt="Error" style="margin-top: 20px; height: 200px;">'
        '</body>'
        '</html>'
    )
    return '''
    <!doctype html>
    <html>
    <head>
        <title>Análisis y Limpieza de Datos</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f8f8f8;
                text-align: center;
                padding: 50px;
            }
            .container {
                margin: auto;
                width: 100%;
                padding: 10px;
            }
            select, input[type=file], input[type=submit] {
                width: autio;
                margin: 10px 0;
            }
            .download-button {
                display: inline-block;
                padding: 10px 20px;
                background-color: #98FB98; /* Color pastel */
                color: white;
                border: none;
                border-radius: 4px;
                text-decoration: none;
                font-size: 1.2em;
            }
            .download-button:hover {
                background-color: #98FB98; /* Color pastel más claro */
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Bienvenido a tu Asistente de Limpieza de Datos</h1>
            <p>
                ¿Tienes un archivo de Excel y necesitas verificar la completitud de tus columnas o limpiar los datos?
                ¡Estás en el lugar correcto! Sube tu archivo y nosotros nos encargaremos de analizarlo y limpiarlo para ti.
                Es rápido, fácil y seguro.
            </p>
            <label for="tipo-archivo">Selecciona el tipo de archivo:</label>
            <select name="tipo-archivo" id="tipo-archivo">
                <option value="biblia-academica">Biblia académica</option>
                <option value="matriculados-otras-universidades">Matriculados otras universidades</option>
                <option value="tipo-generico">Tipo Genérico</option>
            </select>
            <form method="post" enctype="multipart/form-data">
                <div class="file-input-container">
                    <input type="file" name="file">
                </div>
                <div class="submit-button-container">
                    <input type="submit" value="Cargar y Limpiar" class="download-button">
                </div>
            </form>
            <img src="https://media.tenor.com/T4664VfiM0cAAAAC/asistente-robot.gif" alt="Asistente" style="margin-top: 20px; height: 200px;">
        </div>
    </body>
    </html>
    '''

def formatear_nombres_df(df, nombre):
    def formatear_nombre(nombre):
        palabras = nombre.lower().split()
        palabras_capitalizadas = [palabra.capitalize() for palabra in palabras]
        nombre_formateado = ' '.join(palabras_capitalizadas)
        return nombre_formateado
    df[nombre] = df[nombre].apply(formatear_nombre)
    return df


@app.route('/download/<filename>')
def download_file(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return send_file(filepath, as_attachment=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'csv'

def limpiar_y_formatear_valor(valor):
    # Elimina espacios al principio y al final
    valor = str(valor).strip()

    # Elimina caracteres extraños, excepto letras, números y espacios
    valor = re.sub(r'[^a-zA-Z0-9\s]', '', valor)

    try:
        # Intenta convertir a float si es posible
        return float(valor)
    except ValueError:
        # Si no es numérico, capitaliza la primera letra sin cambiar el resto
        return valor[0].upper() + valor[1:] if valor else valor

