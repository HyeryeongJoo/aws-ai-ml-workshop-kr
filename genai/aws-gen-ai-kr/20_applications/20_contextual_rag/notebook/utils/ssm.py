import os
import boto3
import re

class parameter_store():
    
    def __init__(self, region_name="ap-northeast-2"):
        
        self.ssm = boto3.client('ssm', region_name=region_name)
        
    def put_params(self, key, value, dtype="String", overwrite=False, enc=False):
        
        # Specify the parameter name, value, and type
        if enc: dtype="SecureString"

        try:
            # Put the parameter
            response = self.ssm.put_parameter(
                Name=key,
                Value=value,
                Type=dtype,
                Overwrite=overwrite  # Set to True if you want to overwrite an existing parameter
            )

            # Print the response
            print('Parameter stored successfully.')
            #print(response)

        except Exception as e:
            print('Error storing parameter:', str(e))

    def get_params(self, key, enc=False):

        if enc: WithDecryption = True
        else: WithDecryption = False
        response = self.ssm.get_parameters(
            Names=[key,],
            WithDecryption=WithDecryption
        )

        return response['Parameters'][0]['Value']

    def get_all_params(self, ):

        response = self.ssm.describe_parameters(MaxResults=50)

        return [dicParam["Name"] for dicParam in response["Parameters"]]

    def delete_param(self, listParams):

        response = self.ssm.delete_parameters(
            Names=listParams
        )
        print (f"  parameters: {listParams} is deleted successfully")
        

    def parse_opensearch_endpoint(self, endpoint):
        if not endpoint.startswith('https://'):
            endpoint = 'https://' + endpoint
            
        pattern = r'https://([a-zA-Z0-9-]+)\.([a-z0-9-]+)\.es\.amazonaws\.com'

        match = re.match(pattern, endpoint)

        if match:
            full_domain_name = match.group(1)

            parts = full_domain_name.split('-')
            if len(parts) > 1:
                prefix = parts[0]
                domain_name = '-'.join(parts[1:])
            else:
                prefix = ''
                domain_name = full_domain_name

            return prefix, domain_name
        else:
            return None