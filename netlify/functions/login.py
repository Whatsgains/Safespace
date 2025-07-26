import json

def handler(event, context):
    # Only allow POST method
    if event["httpMethod"] != "POST":
        return {
            "statusCode": 405,
            "body": json.dumps({"error": "Method not allowed"})
        }

    try:
        # Parse the request body
        data = json.loads(event["body"])
        username = data.get("username")
        password = data.get("password")

        # Basic credential check (replace this with real database logic)
        if username == "admin" and password == "pass":
            return {
                "statusCode": 200,
                "body": json.dumps({"message": "Login successful"})
            }
        else:
            return {
                "statusCode": 401,
                "body": json.dumps({"error": "Invalid credentials"})
            }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal server error", "details": str(e)})
        }
