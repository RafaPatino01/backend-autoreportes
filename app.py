import os
from flask import Flask, request
import numpy as np
import pandas as pd


UPLOAD_FOLDER = '/Users/rafaelpatino/Desktop/backend-autoreportes/files'
ALLOWED_EXTENSIONS = {'txt', 'csv'}

app = Flask(__name__)

@app.route('/')
def index():
    return ["backend-autoreportes API"]

#CSV Upload form handle
@app.route('/uploadCSV',methods = ['POST'])
def upload_file():
    if request.method == 'POST':
        uploaded_file1 = request.files['new']
        uploaded_file2 = request.files['old']

        flag = 0

        if uploaded_file1.filename != '':
            uploaded_file1.save("files/" + "input_new.csv")
            flag += 1

        if uploaded_file2.filename != '':
            uploaded_file2.save("files/" + "input_old.csv")
            flag += 1
        
        if(flag == 2):
            res = procesar_lista()
        
        return res
    
# Función de procesamiento del CSV
def procesar_lista():
    print("Procesando lista...")

    new_df = pd.read_csv("files/input_new.csv")
    old_df = pd.read_csv("files/input_old.csv")

    # Asesores del ciclo actual
    new_asesores = new_df.NAME
    new_asesores = new_asesores.unique() # Eliminar repetidos
    new_asesores = set(new_asesores.flatten())

    # Asesores del ciclo pasado
    old_asesores = old_df.NAME
    old_asesores = old_asesores.unique() # Eliminar repetidos
    old_asesores = set(old_asesores.flatten())

    # Asesores que están en ambos registros
    l1 = new_asesores.intersection(old_asesores)
    print("Count: " + str(len(l1)))
    print(type(l1))

    # Profesores que dejaron de ser asesores
    l3 = [x for x in list(old_asesores) if x not in list(l1)]
    print("Count: " + str(len(l3)))
    print(l3)

    # Asesores nuevos
    l4 = [x for x in list(new_asesores) if x not in list(l1)]
    print("Count: " + str(len(l4)))
    print(l4)

    print("Procesando HTML...")
    return(buildHTML(list(new_asesores), list(l1), list(l3), list(l4)))


# Build the template to show in HTML
def buildHTML(asesores_current, asesores_both, not_asesores, asesores_new):

    parsed_current = ""
    parsed_both = ""
    parsed_not_asesores = ""
    parsed_new = ""

    for i in range(1, len(asesores_current)):
        parsed_current = parsed_current + "<p class='border-bottom'>" + asesores_current[i] + "</p>"

    for i in range(1, len(asesores_both)):
        parsed_both = parsed_both + "<p class='border-bottom'>" + asesores_both[i] + "</p>"

    for i in range(1, len(not_asesores)):
        parsed_not_asesores = parsed_not_asesores + "<p class='border-bottom'>" + not_asesores[i] + "</p>"

    for i in range(1, len(asesores_new)):
        parsed_new = parsed_new + "<p class='border-bottom'>" + asesores_new[i] + "</p>"

    # Build result
    html_result = """\
    <html>
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="image_src" href="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRpgLFFQwrT5BdbszkAENbkEKoezi6GV-oxU-yXLVD66bq8sjwKQ0vdGfHCByKGH7lrJMg&usqp=CAU" />
        <link rel="icon" type="image/x-icon" href="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRpgLFFQwrT5BdbszkAENbkEKoezi6GV-oxU-yXLVD66bq8sjwKQ0vdGfHCByKGH7lrJMg&usqp=CAU">
        <title>AutoReportes</title>

        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
        <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/popper.js@1.14.7/dist/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/danfojs@1.1.0/lib/bundle.min.js"></script>
    </head>
    <body>
        <div class="container p-5">
            <h1>Reporte de asesores: </h1>
            <br>
            <br>
            <div class="row">
                <div class="col-6">
                    <div class="bg-light p-3">
                        <hr>
                        <h2> <span class="bg-dark text-white">[ {d1} ]</span> Asesores del ciclo actual:</h2>
                            <div class="row">
                                <div class="col-3"> 
                                    <a class="btn btn-primary" data-toggle="collapse" href="#collapse1" role="button" aria-expanded="false" aria-controls="collapse1">Mostrar 👀</a>
                                </div>
                                <div class="col-4"> 
                                    <a class="btn btn-secondary" >Descargar ⬇️ </a>
                                </div>
                            </div>
                        
                        <br>
                        <div class="collapse multi-collapse" id="collapse1">
                            {d2}
                        </div>
                        <hr>
                    </div>
                </div>

                <div class="col-6">
                    <div class="bg-light p-3">
                        <hr>
                        <h2><span class="bg-dark text-white">[ {d3} ]</span> Asesores en ambos registros: </h2>
                            <div class="row">
                                <div class="col-3"> 
                                    <a class="btn btn-primary" data-toggle="collapse" href="#collapse2" role="button" aria-expanded="false" aria-controls="collapse2">Mostrar 👀</a>
                                </div>
                                <div class="col-4"> 
                                    <a class="btn btn-secondary" >Descargar ⬇️ </a>
                                </div>
                            </div>
                        
                        <br>
                        <div class="collapse multi-collapse" id="collapse2">
                            {d4}
                        </div>
                        <hr>
                    </div>
                </div>
            </div>

            <br>
            <br>


            <div class="row">
                <div class="col-6">
                    <div class="bg-light p-3">
                        <hr>
                        <h2> <span class="bg-dark text-white">[ {d5} ]</span> Dejaron de ser asesores:</h2>
                            <div class="row">
                                <div class="col-3"> 
                                    <a class="btn btn-primary" data-toggle="collapse" href="#collapse3" role="button" aria-expanded="false" aria-controls="collapse3">Mostrar 👀</a>
                                </div>
                                <div class="col-4"> 
                                    <a class="btn btn-secondary" >Descargar ⬇️ </a>
                                </div>
                            </div>
                        
                        <br>
                        <div class="collapse multi-collapse" id="collapse3">
                            {d6}
                        </div>
                        <hr>
                    </div>
                </div>

                <div class="col-6">
                    <div class="bg-light p-3">
                        <hr>
                        <h2><span class="bg-dark text-white">[ {d7} ]</span> Asesores nuevos: </h2>
                            <div class="row">
                                <div class="col-3"> 
                                    <a class="btn btn-primary" data-toggle="collapse" href="#collapse4" role="button" aria-expanded="false" aria-controls="collapse4">Mostrar 👀</a>
                                </div>
                                <div class="col-4"> 
                                    <a class="btn btn-secondary" >Descargar ⬇️ </a>
                                </div>
                            </div>
                        
                        <br>
                        <div class="collapse multi-collapse" id="collapse4">
                            {d8}
                        </div>
                        <hr>
                    </div>
                </div>
            </div>

        </div>
        
    </body>
    </html>
    """.format(d1=len(asesores_current), 
               d2=parsed_current, 
               d3=len(asesores_both), 
               d4=parsed_both,
               d5=len(not_asesores), 
               d6=parsed_not_asesores, 
               d7=len(asesores_new), 
               d8=parsed_new)
    
    return html_result