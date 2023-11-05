if __name__ == "__main__":

    import sqlite3
    from misc.config import db

    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    query = f'''
    ALTER TABLE groups ADD COLUMN payment
    '''
    

    cursor.execute(query)
    conn.commit()
    conn.close()