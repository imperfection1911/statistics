import psycopg2


class Db:

    def __init__(self):
        try:
            self.connection = psycopg2.connect("dbname='statistics' user='postgres' host='postgres' password='1qaz2wsx'")
        except Exception as e:
            print("unable to connect to database: ", e)

    # инсерт пачки в базу
    def insert(self, rows):
        query = "INSERT INTO public.statistics VALUES"
        row_index = 0
        # формирование пачки
        for row in rows:
            if row_index < len(rows) - 1:
                query += "('{0}', '{1}'),".format(row[0], row[1].replace(':', ''))
            else:
                query += "('{0}', '{1}');".format(row[0], row[1].replace(':', ''))
            row_index += 1
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            self.connection.commit()
            cursor.close()
        except Exception as e:
            print(query)
            print(e)
            self.connection.rollback()
