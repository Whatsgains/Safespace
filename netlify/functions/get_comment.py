import json
import psycopg2
from psycopg2.extras import RealDictCursor

def handler(event, context):
    if event['httpMethod'] != 'GET':
        return {
            'statusCode': 405,
            'body': json.dumps({'error': 'Method Not Allowed'})
        }

    try:
        conn = psycopg2.connect(
            dbname="neondb",
            user="neondb_owner",
            password="npg_7MmDGidjKT9z",
            host="ep-little-hat-ae0sgz0x-pooler.c-2.us-east-2.aws.neon.tech",
            port="5432",
            sslmode="require",
            channel_binding="require"
        )

        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT comment_id, content, submitted_at, is_approved FROM comments")
        comments = cur.fetchall()
        cur.close()
        conn.close()

        return {
            'statusCode': 200,
            'body': json.dumps(comments, default=str)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
