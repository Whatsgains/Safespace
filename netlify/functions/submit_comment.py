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
        content = data.get('content')

        if not content:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Content is required'})
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
        cur.execute("INSERT INTO comments (content) VALUES (%s) RETURNING comment_id", (content,))
        comment_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()

        return {
            'statusCode': 201,
            'body': json.dumps({'message': 'Comment submitted', 'comment_id': comment_id})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
