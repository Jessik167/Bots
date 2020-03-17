import pymysql

DB_HOST = '3.231.20.132'
DB_USER = 'apdif'
DB_PASSWORD = 'K3XyRwLjPtkui6qJ'
DB_NAME = 'apdif'


def crea_tabla():
    con = pymysql.connect(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)
    
    sql = "CREATE TABLE IF NOT EXISTS `prueba` (id INT NOT NULL AUTO_INCREMENT," \
          "PRIMARY KEY (id), titulo VARCHAR(100), cantante VARCHAR(100), album VARCHAR(100)," \
          "referer VARCHAR(255), infringe VARCHAR(255), fecha VARCHAR(100), dominio_id INT," \
          "FOREIGN KEY (dominio_id) REFERENCES `dominios` (dominio_id) ON UPDATE CASCADE ON DELETE CASCADE);"
    with con:
        cur = con.cursor()
        cur.execute(sql)


def crea_tabla_relacion():
    con = pymysql.connect(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)
    
    sql = "CREATE TABLE IF NOT EXISTS `dominios` (dominio_id INT NOT NULL," \
          "PRIMARY KEY (id), dominio VARCHAR(100), fecha VARCHAR(100));"
    with con:
        cur = con.cursor()
        cur.execute(sql)

def artist_itunes(id_artista):
    con = pymysql.connect(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)
    
    with con:
        cur = con.cursor()
        sql = ('''SELECT t1.id, t1.artist, t2.song, t2.album FROM `itunes_artist` AS t1 INNER JOIN `itunes_link` AS t2 ON t1.id = t2.artist_id WHERE t1.id = '%s' ''')% (id_artista)
        cur.execute(sql)

        results = cur.fetchall()

        return results
    
def existe_inf(ref):
    con = pymysql.connect(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)
    
    with con:
        cur = con.cursor()
        sql = ('''SELECT infringe FROM `prueba` where infringe = "%s" ''' % ref)
        cur.execute(sql)

        resultado = cur.fetchone()
        if resultado:
            return True
        else:
            return False
        
def existe_ref(ref):
    con = pymysql.connect(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)
    
    with con:
        cur = con.cursor()
        sql = ('''SELECT referer FROM `prueba` where referer = "%s" ''' % ref)
        cur.execute(sql)

        resultado = cur.fetchone()
        if resultado:
            return True
        else:
            return False

def inserta_item(titulo, cantante, album, referer, infringe, fecha, dominio_id):
    con = pymysql.connect(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)
    with con:
        cur = con.cursor()
        sql = ('''INSERT INTO `prueba` VALUES (DEFAULT, "%s", "%s", "%s", "%s", "%s", "%s", "%s") ''' % (titulo, cantante, album, referer, infringe, fecha, dominio_id) )
        cur.execute(sql)
        return True

def inserta_uno_relacional(id, dominio, fecha):
    con = pymysql.connect(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)
    with con:
        cur = con.cursor()
        sql = ('''INSERT INTO `dominios` VALUES ('%s', '%s', '%s')''' % (id, dominio, fecha) )
        cur.execute(sql)
        return True
        
def ultimo_id():
    con = pymysql.connect(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)
    with con:
        cur = con.cursor()
        sql = ('''SELECT max(dominio_id) FROM `dominios`''')
        cur.execute(sql)
        results = cur.fetchone()
        return results[0]
    
    
def existe_id(dominio):
    con = pymysql.connect(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)
    with con:
        cur = con.cursor()
        sql = ('''SELECT dominio_id FROM `dominios` where dominio = '%s' '''% (dominio))
        cur.execute(sql)
        results = cur.fetchone()
        if results:
            return results[0]
        else:
            return False


def existe_ultimoId(dominio):
    con = pymysql.connect(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)
    with con:
        cur = con.cursor()
        sql = ('''SELECT dominio FROM `dominios` WHERE dominio = '%s' '''% (dominio))
        cur.execute(sql)
        results = cur.fetchone()
        if results:
            return True
        else:
            return False
        