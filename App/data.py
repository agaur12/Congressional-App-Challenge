import boto3
import os

aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')


# send username and password to datatable
def store_login_info(username, password, aws_access_key_id, aws_secret_access_key):
    try:
        dynamodb = boto3.client('dynamodb', region_name='us-east-2', aws_access_key_id=aws_access_key_id,
                                aws_secret_access_key=aws_secret_access_key)
        dynamodb.put_item(
            TableName='Login-Information',
            Item={
                'Username': {'S': username},
                'Password': {'S': password}
            }
        )
    except:
        return "Failed to create login information. Please try again."

# check if username exists in the datatable
def check_username(username, aws_access_key_id, aws_secret_access_key):
    dynamodb = boto3.client('dynamodb', region_name='us-east-2', aws_access_key_id=aws_access_key_id,
                            aws_secret_access_key=aws_secret_access_key)
    success = False
    error = None
    try:
        response = dynamodb.get_item(TableName='Login-Information', Key={'Username': {'S': username}})
        item = response.get('Item')
        if item:
            error = 'Username Already Exists'
        else:
            success = True
    except Exception as e:
        print(str(e))

    return success, error

# check if login information is correctly input
def check_login_info(username, password, aws_access_key_id, aws_secret_access_key):
    dynamodb = boto3.client('dynamodb', region_name='us-east-2', aws_access_key_id=aws_access_key_id,
                            aws_secret_access_key=aws_secret_access_key)
    error = None
    success, _ = check_username(username, aws_access_key_id, aws_secret_access_key)
    if not success:
        response = dynamodb.get_item(TableName='Login-Information', Key={'Username': {'S': username}})
        db_password = response.get('Item', {}).get('Password', {}).get('S')
        if password == db_password:
            success = True
        else:
            error = 'Invalid password'
    else:
        error = 'Invalid username'
    return success, error
