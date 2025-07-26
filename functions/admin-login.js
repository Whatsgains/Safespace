const { Client } = require('@neondatabase/serverless');

exports.handler = async function (event, context) {
  const client = new Client({
    connectionString: process.env.DATABASE_URL,
  });

  try {
    await client.connect();

    if (event.httpMethod === 'GET') {
      const result = await client.query('SELECT content, created_at FROM comments ORDER BY created_at DESC');
      await client.end();
      return {
        statusCode: 200,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(result.rows),
      };
    }

    if (event.httpMethod === 'POST') {
      const { content } = JSON.parse(event.body);
      if (!content) {
        await client.end();
        return {
          statusCode: 400,
          body: 'Content is required',
        };
      }

      await client.query('INSERT INTO comments (content, created_at) VALUES ($1, NOW())', [content]);
      await client.end();
      return {
        statusCode: 201,
        body: 'Comment submitted successfully',
      };
    }

    await client.end();
    return {
      statusCode: 405,
      body: 'Method Not Allowed',
    };
  } catch (error) {
    await client.end();
    return {
      statusCode: 500,
      body: `Server Error: ${error.message}`,
    };
  }
};