import json
import boto3pyth
import botocore.config
from datetime import datetime

###aws bedrock call##
#{
# "modelId": "meta.llama4-scout-17b-instruct-v1:0",
# "contentType": "application/json",
# "accept": "application/json",
# "body": "{\"prompt\":\"this is where you place your input text\",\"max_gen_len\":512,\"temperature\":0.5,\"top_p\":0.9}"
#}

#{
# "modelId": "meta.llama3-3-70b-instruct-v1:0",
# "contentType": "application/json",
# "accept": "application/json",
# "body": "{\"prompt\":\"this is where you place your input text\",\"max_gen_len\":512,\"temperature\":0.5,\"top_p\":0.9}"
#}

def content_generration(blogtopic:str)->str:
    prmpt = f"Write a blog on {blogtopic} in 500 words"
    body = {
        "prompt": prmpt,
        "max_gen_len":512,
        "temperature": 0.7,
        "top_p": 0.9,
    }
    try:
        bedrock = boto3.client(
            service_name='bedrock-runtime',
            region_name='us-east-1',
            config=botocore.config.Config(
                read_timeout=60,
                retries={
                    'max_attempts': 10,
                    'mode': 'standard'
                },
                connect_timeout=60
            )
        )
        response = bedrock.invoke_model(
            modelId='us.meta.llama4-scout-17b-instruct-v1:0',
            body=json.dumps(body),
            contentType='application/json',
            accept='application/json'
        )
        response_content = response.get("body").read()
        response_data = json.loads(response_content)
        #print(response_data)
        print(f"Response from Bedrock: {response_data}")
        blog_details = response_data["generation"]
        return blog_details
    
       # response_content = response['body'].read().decode('utf-8')
        #response_json = json.loads(response_content)    
        #print(f"Response from Bedrock: {response_json}")
       # blog_details = response_json.get('content', '')
       # return blog_details
    except Exception as e:
        print(f"Error creating Bedrock client: {e}")
        return None

##S3 uploader function##
def s3_uploader(s3_key,s3_bucket, generate_blog):
    s3 = boto3.client('s3')
    
    
    #bucket_name = 'radarchstaticwebsite'  # Replace with your S3 bucket name
    #file_name = f"{generate_blog.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    try:
        s3.put_object(
            Bucket=s3_bucket,
            Key=s3_key,
            Body=generate_blog
        )
        print(f"File uploaded successfully to {s3_bucket}")
    except Exception as e:
        print(f"Error uploading file to S3: {e}")    

##Main lambda handler function##
def lambda_handler(event, context):
    event=json.loads(event['body'])
    blogtopic = event.get('blogtopic', 'Default Blog Topic')
    print(f"Received blog topic: {blogtopic}")

    generate_blog = content_generration(blogtopic)
    if generate_blog:
        current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
        s3_key = f"blogs/{blogtopic.replace(' ', '_')}_{current_time}.txt"
        s3_bucket = 'radarchstaticwebsite'
        s3_uploader(s3_key, s3_bucket, generate_blog)
    else:
        print("Failed to generate blog content.")
       
       
    return {
        'statusCode': 200,
        'body': json.dumps('Blog is generaTED successfully!')
    }

#Json for post API
#{
#    "blogtopic":"AI in healhcare industry"
#    }
