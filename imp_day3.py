from pprint import pprint
import sqlite3
from alpha_vantage.timeseries import TimeSeries

alpha_key = ""


def importacao():
    """
    Extrai os dados utilizando a api alpha_vatage
    verifica se o preço de fechamento para o dia
    ainda não foi gravado no banco.
    :return:
    tiker, data, nome, preço fechamento
    """
    fonte = ['B3SA3.SAO', 'PETR4.SAO']
    for ft in range(len(fonte)):
        chave_direta = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={" \
                       "}&outputsize='full'&interval=5min&apikey={}".format(fonte[ft], alpha_key)

        ts = TimeSeries(key=chave_direta, output_format='pandas', indexing_type='date')
        dados, meta_dados = ts.get_daily(chave_direta)

        ins_tiker = fonte[ft]
        ins_data = dados.index.date.any()
        ins_nome = 'BRASIL'
        ins_prec = str(dados['4. close'].iloc[-1])

        try:
            conn = sqlite3.connect('ativos.db')
            cursor = conn.cursor()

            busca = (""" SELECT preco FROM dados_ativos WHERE preco={}""".format(ins_prec))
            cursor.execute(busca)
            dados_lidos = cursor.fetchall()

            if len(dados_lidos) != 0:
                print("preço já cadastrado")
            else:
                ins_precfech = ins_prec
                ins_dados(ins_tiker, ins_data, ins_nome, ins_precfech, dados)

        except Exception as e:
            print("Uma excessão ocorreu: ", e)
    return


def ins_dados(ins_tiker, ins_data, ins_nome, ins_precfech, dados):
    """
    Após verificar insere os dados extarido na tabela
    dados_ativos.
    :param ins_tiker:
    :param ins_data:
    :param ins_nome:
    :param ins_precfech:
    :param dados:
    :return:
    """
    try:
        conn = sqlite3.connect('ativos.db')
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO dados_ativos(ticker, data, nome, preco, habilitado)
        VALUES (?, ?, ?, ?, ?)   
        """, (ins_tiker, ins_data, ins_nome, ins_precfech, 1))

        conn.commit()
        print('Dados inseridos com sucesso.')

        imprime(dados)

    except Exception as e:
        print("Uma excessão ocorreu: ", e)


def imprime(dados):
    """
    imprime os dados para verificação no terminal
    :param dados:
    :return:
    """
    # pprint(dados.index.date.any())
    # pprint(fonte[ft])
    # pprint(dados['4. close'].iloc[-1])
    # pprint(meta_dados)
    pprint(dados)


importacao()
