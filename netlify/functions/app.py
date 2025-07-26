from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# Supabase PostgreSQL connection (replace with your connection string)
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="Akanimo2004.",
    host="db.zswsyusnjzawufawhnoy.supabase.co",
    port="5432"
)

@app.route('/submit-comment', methods=['POST'])
def submit_comment():
    data = request.get_json()
    content = data.get('content')
    if not content:
        return jsonify({'error': 'Content is required'}), 400
    
    with conn.cursor() as cur:
        cur.execute("INSERT INTO comments (content) VALUES (%s) RETURNING comment_id", (content,))
        comment_id = cur.fetchone()[0]
        conn.commit()
    return jsonify({'message': 'Comment submitted', 'comment_id': comment_id}), 201

@app.route('/get-comments', methods=['GET'])
def get_comments():
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT comment_id, content, submitted_at, is_approved FROM comments WHERE is_approved = TRUE")
        comments = cur.fetchall()
    return jsonify(comments)

if __name__ == '__main__':
    app.run(debug=True)