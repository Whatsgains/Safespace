import json
from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
import os
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

# Neon database connection using environment variables
conn = psycopg2.connect(
    dbname=os.environ.get("DB_NAME", "neondb"),
    user=os.environ.get("DB_USER", "neondb_owner"),
    password=os.environ.get("DB_PASSWORD", "npg_7MmDGidjKT9z"),
    host=os.environ.get("DB_HOST", "ep-little-hat-ae0sgz0x-pooler.c-2.us-east-2.aws.neon.tech"),
    port=os.environ.get("DB_PORT", "5432"),
    sslmode="require",
    channel_binding="require"
)

@app.route('/login', methods=['POST'])
def login():
    logging.debug('Login attempt received')
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            return jsonify({'error': 'Username and password are required'}), 400
        with conn.cursor() as cur:
            cur.execute("SELECT password_hash FROM users WHERE username = %s", (username,))
            result = cur.fetchone()
            if result and result[0] == password:
                return jsonify({'message': 'Login successful'}), 200
            return jsonify({'error': 'Invalid credentials'}), 401
    except psycopg2.Error as e:
        logging.error(f'Database error: {e}')
        return jsonify({'error': 'Database connection failed'}), 500
    except Exception as e:
        logging.error(f'Unexpected error: {e}')
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/get-comments', methods=['GET'])
def get_comments():
    try:
      with conn.cursor(cursor_factory=RealDictCursor) as cur:
          cur.execute("SELECT comment_id, content, submitted_at, is_approved FROM comments")
          comments = cur.fetchall()
      return jsonify(comments)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/submit-comment', methods=['POST'])
def submit_comment():
    try:
        data = request.get_json()
        content = data.get('content')
        if not content:
            return jsonify({'error': 'Content is required'}), 400
        with conn.cursor() as cur:
            cur.execute("INSERT INTO comments (content) VALUES (%s) RETURNING comment_id", (content,))
            comment_id = cur.fetchone()[0]
            conn.commit()
        return jsonify({'message': 'Comment submitted', 'comment_id': comment_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
