import json
import psycopg2

def handler(event, context):
    if event['httpMethod'] != 'POST':
        return {
            'statusCode': 405,
            'body': json.dumps({'error': 'Method Not Allowed'})
        }

    try:
        data = json.loads(event['body'])
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Username and password are required'})
            }

        conn = psycopg2.connect(
            dbname="neondb",
            user="neondb_owner",
            password="npg_7MmDGidjKT9z",
            host="ep-little-hat-ae0sgz0x-pooler.c-2.us-east-2.aws.neon.tech",
            port="5432",
            sslmode="require",
            channel_binding="require"
        )

        cur = conn.cursor()
        cur.execute("SELECT password_hash FROM users WHERE username = %s", (username,))
        result = cur.fetchone()
        cur.close()
        conn.close()

        if result and result[0] == password:
            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'Login successful'})
            }
        else:
            return {
                'statusCode': 401,
                'body': json.dumps({'error': 'Invalid credentials'})
            }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
