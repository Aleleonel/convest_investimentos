import sqlite3

# conectando...
conn = sqlite3.connect('ativos.db')
# definindo um cursor
cursor = conn.cursor()

# criando a tabela (schema)
cursor.execute("""
CREATE TABLE dados_ativos (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        ticker TEXT NOT NULL,
        data   DATE NOT NULL,
        nome TEXT NULL,
        preco TEXT NOT NULL,
        habilitado BOOLEAN NOT NULL CHECK (habilitado IN (0,1)))
""")

print('Tabela criada com sucesso.')
# desconectando...
conn.close()