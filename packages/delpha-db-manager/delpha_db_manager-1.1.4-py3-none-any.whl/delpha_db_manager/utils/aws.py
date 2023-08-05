import boto3

def start_s3(key, secret, region = 'us-east-2'):
    s3 = boto3.client("s3", region_name = region, aws_access_key_id = key, aws_secret_access_key = secret)
    return s3

def start_appflow(key, secret, region = 'us-east-2'):
    af = boto3.client("appflow", region_name = region, aws_access_key_id = key, aws_secret_access_key = secret)
    return af