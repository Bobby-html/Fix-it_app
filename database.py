import psycopg2

def get_db_connection():
    # Put your Supabase credentials here ONE time
    conn = psycopg2.connect(
        host="db.zyoosirpaokoldrxpzhb.supabase.co",
        database="postgres",
        user="postgres",
        password="Ign1te_Gam1ng",
        port="5432"
    )
    return conn