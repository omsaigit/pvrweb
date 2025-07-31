import requests


def update_token_api(userid,entoken,funds):
    upate_token_api='https://trading.omsaiservices.in/update-token'
    # New data you want to update
    update_token = {
        "user_id": userid,
        "entoken": entoken,
        "funds":funds
    }   
    # Making a PUT or PATCH request with the new data
    response = requests.post(url=upate_token_api, data=update_token)  # Use 'requests.patch' for a PATCH request
    # Checking if the request was successful (status code 200 for successful update)
    if response.status_code == 200:
        updated_data = response.json()  # Assuming the API returns updated data
        print(updated_data)  # Display or handle the updated data
    else:
        print('Failed to update data via the API')

def insert_api(register):
    insert_url='https://trading.omsaiservices.in/create-user'
    
    response = requests.post(url=insert_url,data=register)  # Use 'requests.patch' for a PATCH request

    # Checking if the request was successful (status code 200 for successful update)
    if response.status_code == 200:
        updated_data = response.json()  # Assuming the API returns updated data
        print("Data updated successfully:")
        print(updated_data)  # Display or handle the updated data
    else:
        print('Failed to update data via the API')


def insert_api_hist(historical_data):
    insert_url='https://trading.omsaiservices.in/historical_data'
    
    response = requests.post(url=insert_url,data=historical_data)  # Use 'requests.patch' for a PATCH request

    # Checking if the request was successful (status code 200 for successful update)
    if response.status_code == 200:
        updated_data = response.json()  # Assuming the API returns updated data
        # print("Data updated successfully:")
        print(updated_data)  # Display or handle the updated data
    else:
        print('Failed to update data via the API')
def insert_api_quote(quote):
    insert_url='https://trading.omsaiservices.in/quote'
    
    response = requests.post(url=insert_url,data=quote)  # Use 'requests.patch' for a PATCH request

    # Checking if the request was successful (status code 200 for successful update)
    if response.status_code == 200:
        updated_data = response.json()  # Assuming the API returns updated data
        # print("Data updated successfully:")
        # print(updated_data)  # Display or handle the updated data
    else:
        print('Failed to update data via the API')

def margins_api(register):
    insert_url='https://trading.omsaiservices.in/margins'
    
    response = requests.post(url=insert_url,data=register)  # Use 'requests.patch' for a PATCH request

    # Checking if the request was successful (status code 200 for successful update)
    if response.status_code == 200:
        updated_data = response.json()  # Assuming the API returns updated data
        print("Data Margins Inserted Successfully:")
        print(updated_data)  # Display or handle the updated data
    else:
        print('Failed to insert data via the API')
def funds_api(funds):
    insert_url='https://trading.omsaiservices.in/funds'
    
    response = requests.post(url=insert_url,data=funds)  # Use 'requests.patch' for a PATCH request
    print(response)
    # Checking if the request was successful (status code 200 for successful update)
    if response.status_code == 200:
        updated_data = response.json()  # Assuming the API returns updated data
        print("Data Funds Inserted Successfully:")
        print(updated_data)  # Display or handle the updated data
    else:
        print('Failed to insert data via the API')
def positions_api(json_data):
    url='https://trading.omsaiservices.in/positions'
    # Set headers
    headers = {'Content-Type': 'application/json'}

    # Send POST request
    response = requests.post(url, data=json_data, headers=headers)

    # Check the response
    if response.status_code == 200:
        print("Data sent successfully!")
        print("Response:", response.text)
    else:
        print("Failed to send data. Status code:", response.status_code)            


def indices_api(json_data):
    url='https://trading.omsaiservices.in/indices_data'
    # Set headers
    headers = {'Content-Type': 'application/json'}

    # Send POST request
    response = requests.post(url, data=json_data, headers=headers)

    # Check the response
    if response.status_code == 200:
        print("Data sent successfully!")
        print("Response:", response.text)
    else:
        print("Failed to send data. Status code:", response.status_code)            
    
def quote_data_api(json_data):
    url='https://trading.omsaiservices.in/quote_data_api'
    # Set headers
    headers = {'Content-Type': 'application/json'}

    # Send POST request
    response = requests.post(url, data=json_data, headers=headers)

    # Check the response
    if response.status_code == 200:
        print("Data sent successfully!")
        print("Response:", response.text)
    else:
        print("Failed to send data. Status code:", response.status_code)     


def sec_data_api(sec):
    insert_url='https://trading.omsaiservices.in/sec-data'
    
    response = requests.post(url=insert_url,data=sec)  # Use 'requests.patch' for a PATCH request

    # Checking if the request was successful (status code 200 for successful update)
    if response.status_code == 200:
        updated_data = response.json()
    else:
        print('Failed to insert data via the API')
def back_test_api(register):
    insert_url='https://trading.omsaiservices.in/back-test'
    
    response = requests.post(url=insert_url,data=register)  # Use 'requests.patch' for a PATCH request
    print(response)
    # Checking if the request was successful (status code 200 for successful update)
    if response.status_code == 200:
        print("Response:", response.text)
    else:
        print('Failed to insert data via the API')
def user_details():
    get_user_url='https://trading.omsaiservices.in/user'
    response = requests.get(url=get_user_url)  
    if response.status_code == 200:
        user_data = response.json() 
        return user_data  # Display or handle the updated data
    else:
        print('Failed to update data via the API')

user_details()