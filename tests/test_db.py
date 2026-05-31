import psycopg2

conn = psycopg2.connect(
    host="ep-patient-pine-apzp99to-pooler.c-7.us-east-1.aws.neon.tech",
    database="neondb",
    user="neondb_owner",
    password="npg_MBzm0KaY2TUg",
    port="5432",
    sslmode="require"
)

print("Connected Successfully!")
conn.close()
