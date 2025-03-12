from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime
import json
import pytz
import sqlite3
app = Flask(__name__)
from datetime import datetime
import pytz

conn = sqlite3.connect("flponto.db")
conn.row_factory = sqlite3.Row
cur = conn.cursor()
cur.execute('''
CREATE TABLE IF NOT EXISTS folhaponto (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    entrada TEXT,
    saida TEXT
)
''')
conn.commit()
conn.close()
# Definindo o fuso horário de Brasília (BRT - Brasilia Time)
brasilia_tz = pytz.timezone('America/Sao_Paulo')

# Obtendo o horário atual no fuso horário de Brasília
horario_br = datetime.now(brasilia_tz).strftime("%d/%m/%Y %H:%M:%S")



# Lista para armazenar os registros de ponto

def lregistros():
    conn = sqlite3.connect("flponto.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM folhaponto")
    j = [dict(row) for row in cur.fetchall()]
    conn.close()
    return j
def lsavlar():
    with open("listaponto.json", "w") as lre:
        json.dump(registros, lre, indent=4)
registros = lregistros()

@app.route('/')
def index():
    registros = lregistros()
    return render_template('index.html', registros=registros)


@app.route("/<nome>", methods=["GET"])
def requerir(nome):
    registros = lregistros()  # Obtém os registros
    registroreturn = []

    # Loop para filtrar os registros onde 'saida' não é None
    for registro in registros:
        if registro['saida'] is not None:
            registroreturn.append(registro)
    
    # Se você quiser filtrar também pelo 'nome', pode fazer assim:
    registroreturn = [registro for registro in registroreturn if registro['nome'] == nome]
    
    # Retorna a lista filtrada em formato JSON
    return jsonify(registroreturn)

@app.route('/registrar_entrada', methods=['POST'])
def registrar_entrada():
    conn = sqlite3.connect("flponto.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    nome = request.form['nome']
    horario = datetime.now().strftime("%D  %H:%M:%S")
    #horario = datetime.now()
    if registros:
        for registro in registros:
            if registro["nome"] == nome and registro["saida"] is None:
                None
                break
        else:
            #registros.append({"nome": nome, "entrada": horario, "saida": None})
            cur.execute("INSERT INTO folhaponto (nome, entrada, saida)values(?,?,?)",(nome, horario, None))
            conn.commit()
            conn.close()
            #lsavlar()

    else:
        #registros.append({"nome": nome, "entrada": horario, "saida": None})
        cur.execute("INSERT INTO folhaponto (nome, entrada, saida)values(?,?,?)",(nome, horario, None))
        conn.commit()
        conn.close()
        #lsavlar()
    return redirect(url_for('index'))

@app.route('/registrar_saida', methods=['POST'])
def registrar_saida():
    conn = sqlite3.connect("flponto.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    nome = request.form['nome']
    horario = datetime.now().strftime("%D  %H:%M:%S")
    #horario = datetime.now()
    cur.execute("""
    UPDATE folhaponto
    SET saida = ?
    WHERE nome = ? AND saida IS NULL
    """, (horario, nome))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


