# coding: utf-8
import os
from werkzeug import secure_filename
from flask import (
    Flask, request, current_app, send_from_directory, render_template
)

from db import escolaAzul

app = Flask("escolaAzul")

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

#configurando para inserir arquivos de media na pasta media_files que deve estar na raiz
app.config['MEDIA_ROOT'] = os.path.join(PROJECT_ROOT,'media_files')

@app.route("/alunos/cadastro", methods =["GET","POST"])
def cadastro_alunos():
	if request.method == "POST":

		dados_do_formulario = request.form.to_dict()
		imagem = request.files.get('imagem')

		if imagem:
			filename = secure_filename(imagem.filename)
			path = os.path.join(current_app.config['MEDIA_ROOT'], filename)
			imagem.save(path)
			dados_do_formulario['imagem'] = filename

		print(dados_do_formulario)
		id_aluno = escolaAzul.insert(dados_do_formulario)
		return render_template('cadastro_sucesso.html', id_aluno = id_aluno)

	return render_template('cadastro.html')

@app.route("/")
def index():
	todos_alunos = escolaAzul.all()
	return render_template('index.html',todos_alunos = todos_alunos)

@app.route("/alunos/<int:aluno_ra>")
def aluno(aluno_ra):
	aluno = escolaAzul.find_one(id=aluno_ra)
	return render_template('ficha_aluno.html', aluno=aluno)

@app.route('/media/<path:filename>')
def media(filename):
	return send_from_directory(current_app.config.get('MEDIA_ROOT'), filename)

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)