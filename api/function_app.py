import azure.functions as func
import logging
import csv
import json
import secrets
import string

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="csv_to_json")
def csv_to_json(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        # Get CSV data from request body
        csv_data = req.get_body().decode('utf-8').strip()

        # Convert CSV data to a list of dictionaries
        csv_reader = csv.DictReader(csv_data.split('\r\n'))
        data = [row for row in csv_reader]

        # Convert to JSON
        json_data = json.dumps(data, indent=2)

        # Return JSON in the response
        return func.HttpResponse(json_data, mimetype="application/json", status_code=200)
    
    except Exception as e:
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)

@app.route(route="password_generator")
def password_generator(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        req_body = req.get_json()
        password_length = req_body.get('length', 50) # Default to 50 if not provided

        if not isinstance(password_length, int) or password_length <= 0:
            return func.HttpResponse("Invalid length provided", status_code=400)
        
        alphabet = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(secrets.choice(alphabet) for _ in range(password_length))

        data = {
            "value": password
        }

        json_data = json.dumps(data, indent=2)

        return func.HttpResponse(json_data, mimetype="application/json", status_code=200)
    
    except Exception as e:
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)