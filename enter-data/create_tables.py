import pymysql.cursors
import os

def create_tables():
    conn = pymysql.connect(
        host=os.environ.get("MYSQL_HOST", "127.0.0.1"),
        port=int(os.environ.get("MYSQL_PORT", "3306")),
        password=os.environ.get("MYSQL_PASSWORD", "password"),
        user=os.environ.get("MYSQL_USER", "root"),
        database=os.environ.get("MYSQL_DATABASE", "data-db"),
        cursorclass=pymysql.cursors.DictCursor
    )

    with conn:
        with conn.cursor() as c:
            c.execute('''
                CREATE TABLE IF NOT EXISTS `temperatures` (
                    `id` INT NOT NULL AUTO_INCREMENT,
                    `max_temp` FLOAT NOT NULL,
                    `min_temp` FLOAT NOT NULL,
                    `timestamp` DATETIME NOT NULL,
                    PRIMARY KEY (`id`)
                );
            ''')
        conn.commit()