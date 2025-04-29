import logging
from datetime import datetime, timedelta

import psycopg2


def main():
    conn = psycopg2.connect("dbname=dbname user=dbuser password=dbpass host=dbhost")
    cur = conn.cursor()

    cur.execute("SELECT COALESCE(MAX(time), '1970-01-01') FROM mms")
    last_time = cur.fetchone()[0]

    from_time = last_time + timedelta(seconds=1)
    to_time = datetime.now()

    logging.info(f"Buscando dados de {from_time} até {to_time}")

    novos_dados = [
        ("BTC-BRL", to_time, 100.5, 101.2, 102.3),
    ]

    for pair, timestamp, mms_20, mms_50, mms_200 in novos_dados:
        cur.execute(
            "INSERT INTO pair (pair, timestamp, mms_20, mms_50, mms_200) VALUES (%s, %s, %s, %s, %s)",
            (pair, timestamp, mms_20, mms_50, mms_200),
        )

    conn.commit()
    cur.close()
    conn.close()

    logging.info("Job concluído.")


if __name__ == "__main__":
    main()
