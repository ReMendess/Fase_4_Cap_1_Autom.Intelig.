import os
import sys
from datetime import datetime
import csv

import oracledb

DSN = "oracle.fiap.com.br:1521/ORCL"
USER = "RM563145"
PASSWORD = "260399"

# Conexão
def obter_conexao():
    """Tenta criar a conexão com o banco"""
    try:
        conn = oracledb.connect(user=USER, password=PASSWORD, dsn=DSN)
        cursor = conn.cursor()
        return conn, cursor
    except Exception as exc:
        print(f"Erro ao conectar no banco: {exc}")
        return None, None


conn, cursor = obter_conexao()
if conn is None:
    sys.exit(1)


# ---------------------------------------------------------------------------

# Funções


def limpar_tela():
    """Limpa a tela"""
    os.system("cls" if os.name == "nt" else "clear")


def ler_float(msg: str) -> float:
    """Solicita ao usuário um número"""
    while True:
        try:
            return float(input(msg))
        except ValueError:
            print("Valor inválido! Digite um número.")


def ler_int(msg: str) -> int:
    """Solicita ao usuário um inteiro até que ele digite algo válido."""
    while True:
        try:
            return int(input(msg))
        except ValueError:
            print("Digite um número inteiro válido.")


# ---------------------------------------------------------------------------

# CRUD – Inserção


def inserir_sensor_ph(ph_registrado: float, status_sensor: str, loc_sensor: str):
    data_hora = datetime.now()
    cursor.execute(
        """
        INSERT INTO SENSOR_PH (PH_registrado, data_hora, status_sensor, loc_sensor)
        VALUES (:1, :2, :3, :4)
        """,
        (ph_registrado, data_hora, status_sensor, loc_sensor),
    )
    conn.commit()


def inserir_sensor_fosforo(fosforo_registrado: float, status_sensor: str, loc_sensor: str):
    data_hora = datetime.now()
    cursor.execute(
        """
        INSERT INTO SENSOR_FOSFORO (Fosforo_registrado, data_hora, status_sensor, loc_sensor)
        VALUES (:1, :2, :3, :4)
        """,
        (fosforo_registrado, data_hora, status_sensor, loc_sensor),
    )
    conn.commit()


def inserir_sensor_potassio(potassio_registrado: float, status_sensor: str, loc_sensor: str):
    data_hora = datetime.now()
    cursor.execute(
        """
        INSERT INTO SENSOR_POTASSIO (Potassio_registrado, data_hora, status_sensor, loc_sensor)
        VALUES (:1, :2, :3, :4)
        """,
        (potassio_registrado, data_hora, status_sensor, loc_sensor),
    )
    conn.commit()


# ---------------------------------------------------------------------------

# CRUD – Consulta


def consultar(tabela: str):
    cursor.execute(f"SELECT * FROM {tabela}")
    return cursor.fetchall()


# ---------------------------------------------------------------------------

# CRUD – Atualização


def atualizar_sensor_ph(id_sensor_ph: int, novo_valor: float):
    cursor.execute(
        """
        UPDATE SENSOR_PH
        SET PH_registrado = :1
        WHERE id_sensor_ph = :2
        """,
        (novo_valor, id_sensor_ph),
    )
    conn.commit()


def atualizar_sensor_fosforo(id_sensor_fosforo: int, novo_valor: float):
    cursor.execute(
        """
        UPDATE SENSOR_FOSFORO
        SET Fosforo_registrado = :1
        WHERE id_sensor_fosforo = :2
        """,
        (novo_valor, id_sensor_fosforo),
    )
    conn.commit()


def atualizar_sensor_potassio(id_sensor_potassio: int, novo_valor: float):
    cursor.execute(
        """
        UPDATE SENSOR_POTASSIO
        SET Potassio_registrado = :1
        WHERE id_sensor_potassio = :2
        """,
        (novo_valor, id_sensor_potassio),
    )
    conn.commit()


# ---------------------------------------------------------------------------

# CRUD – Remoção


def remover_sensor_ph(id_sensor_ph: int):
    cursor.execute("DELETE FROM SENSOR_PH WHERE id_sensor_ph = :1", (id_sensor_ph,))
    conn.commit()


def remover_sensor_fosforo(id_sensor_fosforo: int):
    cursor.execute(
        "DELETE FROM SENSOR_FOSFORO WHERE id_sensor_fosforo = :1", (id_sensor_fosforo,)
    )
    conn.commit()


def remover_sensor_potassio(id_sensor_potassio: int):
    cursor.execute(
        "DELETE FROM SENSOR_POTASSIO WHERE id_sensor_potassio = :1", (id_sensor_potassio,)
    )
    conn.commit()


# --------------------------------------------------------------------------

# Menu – Camada de Interface


def menu_principal():
    while True:
        limpar_tela()
        print("""\n======= MENU PRINCIPAL =======
1 – Inserir dados
2 – Consultar dados
3 – Atualizar dados
4 – Remover dados
5 – Sair
===============================""")

        opcao = ler_int("Escolha uma opção: ")

        if opcao == 1:
            inserir_dados_cli()
        elif opcao == 2:
            consultar_dados_cli()
        elif opcao == 3:
            atualizar_dados_cli()
        elif opcao == 4:
            remover_dados_cli()
        elif opcao == 5:
            break
        else:
            print("Opção inválida!")
            input("Pressione ENTER para continuar…")

    print("\nObrigado por utilizar a aplicação! :)\n")


# ---------------------------------------------------------------------------

# Funções auxiliares do menu

def escolher_sensor() -> int:
    print("""\n--- Sensores ---
1 – pH
2 – Fósforo
3 – Potássio""")
    return ler_int("Escolha o sensor: ")


#  Inserir

def inserir_dados_cli():
    sensor = escolher_sensor()
    valor = ler_float("Digite o valor registrado: ")
    status = input("Status do sensor: ")
    loc = input("Localização do sensor: ")

    if sensor == 1:
        inserir_sensor_ph(valor, status, loc)
    elif sensor == 2:
        inserir_sensor_fosforo(valor, status, loc)
    elif sensor == 3:
        inserir_sensor_potassio(valor, status, loc)
    else:
        print("Sensor inválido!")
    input("\nDados gravados. Pressione ENTER…")


# Consultar - Atualizado para permitir a exportação dos dados.

def consultar_dados_cli():
    sensor = escolher_sensor()
    tabelas = {1: "SENSOR_PH", 2: "SENSOR_FOSFORO", 3: "SENSOR_POTASSIO"}
    tabela = tabelas.get(sensor)
    if not tabela:
        print("Sensor inválido!")
        input("Pressione ENTER…")
        return

    dados = consultar(tabela)
    if not dados:
        print("\nNão há registros.")
    else:
        for linha in dados:
            print(linha)

    print("\nDeseja exportar os dados para CSV?")
    opcao = input("Digite S para sim, qualquer outra tecla para não: ").strip().lower()
    if opcao == "s":
        exportar_para_csv(tabela)

    input("\nPressione ENTER…")


# Atualizar

def atualizar_dados_cli():
    sensor = escolher_sensor()
    id_registro = ler_int("ID do registro que deseja alterar: ")
    novo_valor = ler_float("Novo valor: ")

    if sensor == 1:
        atualizar_sensor_ph(id_registro, novo_valor)
    elif sensor == 2:
        atualizar_sensor_fosforo(id_registro, novo_valor)
    elif sensor == 3:
        atualizar_sensor_potassio(id_registro, novo_valor)
    else:
        print("Sensor inválido!")
    input("\nRegistro atualizado. Pressione ENTER…")


# Remover

def remover_dados_cli():
    sensor = escolher_sensor()
    id_registro = ler_int("ID do registro que deseja remover: ")

    if sensor == 1:
        remover_sensor_ph(id_registro)
    elif sensor == 2:
        remover_sensor_fosforo(id_registro)
    elif sensor == 3:
        remover_sensor_potassio(id_registro)
    else:
        print("Sensor inválido!")
    input("\nRegistro removido. Pressione ENTER…")


# Função nova para Exportar Dados
def exportar_para_csv(tabela: str):
    dados = consultar(tabela)
    if not dados:
        print("Nenhum dado encontrado para exportar.")
        return

    nomes_colunas = [col[0] for col in cursor.description]
    nome_arquivo = f"{tabela}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    try:
        with open(nome_arquivo, mode="w", newline="", encoding="utf-8") as arquivo_csv:
            writer = csv.writer(arquivo_csv)
            writer.writerow(nomes_colunas)
            writer.writerows(dados)
        print(f"Arquivo CSV salvo com sucesso: {nome_arquivo}")
    except Exception as e:
        print(f"Erro ao salvar CSV: {e}")



# ---------------------------------------------------------------------------

# Execução principal

if __name__ == "__main__":
    try:
        menu_principal()
    finally:
        # Garantir que as conexões sejam fechadas mesmo em caso de erro.
        if cursor:
            cursor.close()
        if conn:
            conn.close()
