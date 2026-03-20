import os
from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'chave-padrao-segura-123')
SENHA_ADMIN_SISTEMA = os.environ.get('SENHA_ADMIN', 'admin123')

def init_db():
    conn = sqlite3.connect('biblioteca.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS livros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            paginas INTEGER,
            saga TEXT,
            resumo TEXT,
            resumo_8020 TEXT,
            data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('biblioteca.db')
    conn.row_factory = sqlite3.Row
    
    stats_gerais = conn.execute('SELECT COUNT(*), SUM(paginas) FROM livros').fetchone()
    total_livros = stats_gerais[0] or 0
    total_paginas = stats_gerais[1] or 0
    
    autor_fav_row = conn.execute('''
        SELECT autor, SUM(paginas) as total_lido 
        FROM livros 
        GROUP BY autor 
        ORDER BY total_lido DESC 
        LIMIT 1
    ''').fetchone()
    
    autor_favorito = autor_fav_row['autor'] if autor_fav_row else "Nenhum"
    paginas_autor_fav = autor_fav_row['total_lido'] if autor_fav_row else 0

    livros_com_saga = conn.execute('SELECT * FROM livros WHERE saga IS NOT NULL AND saga != "" ORDER BY saga ASC, id ASC').fetchall()
    
    sagas_agrupadas = {}
    for livro in livros_com_saga:
        nome_saga = livro['saga'].strip().title()
        if nome_saga not in sagas_agrupadas:
            sagas_agrupadas[nome_saga] = []
        sagas_agrupadas[nome_saga].append(livro)

    livros_solo = conn.execute('SELECT * FROM livros WHERE saga IS NULL OR saga = "" ORDER BY titulo ASC').fetchall()
    conn.close()
    
    return render_template('index.html', 
                           sagas=sagas_agrupadas, 
                           livros_solo=livros_solo, 
                           stats={
                               'total_livros': total_livros,
                               'total_paginas': total_paginas,
                               'autor_favorito': autor_favorito,
                               'paginas_autor_fav': paginas_autor_fav
                           })

@app.route('/admin/<senha>')
def login_admin(senha):
    if senha == SENHA_ADMIN_SISTEMA: 
        session['admin'] = True
        return redirect(url_for('index'))
    return "Acesso Negado", 403

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('index'))

@app.route('/adicionar', methods=['POST'])
def adicionar():
    if not session.get('admin'):
        return "Erro: Você não tem permissão.", 403
    
    titulo = request.form.get('titulo')
    autor = request.form.get('autor')
    paginas = request.form.get('paginas')
    saga = request.form.get('saga')
    resumo = request.form.get('resumo-geral')
    resumo_8020 = request.form.get('resumo-8020')

    conn = sqlite3.connect('biblioteca.db')
    conn.execute('INSERT INTO livros (titulo, autor, paginas, saga, resumo, resumo_8020) VALUES (?, ?, ?, ?, ?, ?)', 
                 (titulo, autor, paginas, saga, resumo, resumo_8020))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    if not session.get('admin'):
        return "Erro: Acesso restrito.", 403

    conn = sqlite3.connect('biblioteca.db')
    conn.row_factory = sqlite3.Row
    
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        autor = request.form.get('autor')
        paginas = request.form.get('paginas')
        saga = request.form.get('saga')
        resumo = request.form.get('resumo-geral')
        resumo_8020 = request.form.get('resumo-8020')

        conn.execute('UPDATE livros SET titulo=?, autor=?, paginas=?, saga=?, resumo=?, resumo_8020=? WHERE id=?', 
                     (titulo, autor, paginas, saga, resumo, resumo_8020, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    livro = conn.execute('SELECT * FROM livros WHERE id = ?', (id,)).fetchone()
    conn.close()
    return render_template('editar.html', livro=livro) if livro else ("Não encontrado", 404)

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)