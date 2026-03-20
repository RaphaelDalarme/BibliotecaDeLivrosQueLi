# 📚 BioShelf — Sua Estante Digital Inteligente

<p align="center">
  <img src="https://img.shields.io/badge/Status-Em%20Desenvolvimento-green?style=for-the-badge" alt="Status">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite">
</p>

O **BioShelf** é um sistema de gerenciamento de leituras focado em produtividade e retenção de conhecimento. Ele permite organizar livros, sagas e armazenar resumos baseados no princípio de Pareto (80/20).

---

## 🎯 O Projeto

Diferente de uma lista de leitura comum, o BioShelf foi projetado para ser um **repositório de insights**. Ele separa o que é leitura de entretenimento (Sagas) de livros de estudo (Solo), fornecendo métricas em tempo real sobre o progresso do leitor.

### 🛠️ Principais Funcionalidades
* **Gestão de Acervo:** Cadastro completo com título, autor, páginas e resumos.
* **Agrupamento por Sagas:** Organização automática de volumes de uma mesma série.
* **Dashboard de Métricas:** Contador de livros, total de páginas lidas e destaque para o autor mais lido.
* **Painel Administrativo:** Área restrita para edição e exclusão de registros.

---

## 🛡️ Segurança e Arquitetura Backend

Como um projeto focado em **Backend**, a segurança foi priorizada através de práticas de mercado:

1.  **Variáveis de Ambiente (`Environment Variables`):** O sistema utiliza o módulo `os` para carregar chaves secretas e senhas diretamente do servidor, impedindo que dados sensíveis fiquem expostos no código-fonte.
2.  **Proteção de Rotas:** Implementação de controle de sessão (`flask.session`) para validar o acesso administrativo.
3.  **Persistência de Dados:** Uso de **SQLite3** com comandos SQL otimizados para filtragem e agrupamento (`GROUP BY`, `SUM`, `ORDER BY`).
4.  **Deploy Profissional:** Configurado para rodar com **Gunicorn** em ambiente de produção (PaaS).

---

## 💻 Como rodar este projeto

```bash
# Clone este repositório
$ git clone [https://github.com/RaphaelDalarme/BibliotecaDeLivrosQueLi.git](https://github.com/RaphaelDalarme/BibliotecaDeLivrosQueLi.git)

# Acesse a pasta do projeto
$ cd BibliotecaDeLivrosQueLi

# Instale as dependências
$ pip install -r requirements.txt

# Execute a aplicação
$ python app.py
