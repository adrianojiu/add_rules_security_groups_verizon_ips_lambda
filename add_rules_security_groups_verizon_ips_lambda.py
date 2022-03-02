import json
from urllib.request import urlopen, Request
import boto3

'''
It will add rules for HTTP and HTTPS.
Set variables accordingly.
You need a aws lambda funcion created.
Lambda function definitions: Runtime: Python 3.9. Handler: lambda_function.lambda_handler. Architecture: x86_64. 
Timeout: 5 minutes (at least). Permission: Role wich have permission lo list and write in EC2 and Cloudwatch services.
The security group have to be created and a dummi role have to be created to avoid first execution error.
To ivoke manually run it in aws cli:

aws lambda invoke --function-name PUT_YOUR_LAMBDA_FUNCTION_NAME_HERE output.json

You need an API key authorised in Verizon, if you are a client ask Verion for  it.

Set veriables below as you need.

You need a role attached in lambda funcion, see example in root folder.
'''

def lambda_handler(event, context):

    security_group_id = "sg-01010101010101010"  # Set Security Group ID
    port_range_start = 80                       # Set port range to be opened.
    port_range_end = 80                         # Set port range to be opened.
    port_2_range_start = 443                    # Set port range to be opened, for the second rule.
    port_2_range_end = 443                      # Set port range to be opened, for the second rule.
    protocol = "tcp"                            # Set rule protocol.
    description_all = "VerizonCDNIpRange"       # Rule description.
    url_vz_ip = "https://api.edgecast.com/v2/mcc/customers/superblocks"      # Api url.
    token_vz = 'insert your API token here'                                  # Api token.
    aws_region = "sa-east-1"                                                 # AWS region.
    
    call_api_verizon = Request(url_vz_ip)                                    # Generate api request.
    call_api_verizon.add_header('Authorization', token_vz)                   # Insert autorization to the api call.
    
    try:
        call_api_verizon_content = urlopen(call_api_verizon).read()          # Call api and read content.
    except Exception as error:
        error_strig = str(error)
        print(error_strig)
    
    call_api_verizon_content_json = json.loads(call_api_verizon_content)     # Convert api return to json.
    data_json_ip_v4 = call_api_verizon_content_json['SuperBlockIPv4']        # Getting Verizon ipv4 ips.
    data_json_ip_v6 = call_api_verizon_content_json['SuperBlockIPv6']        # Getting Verizon ipv6 ips.
    data_json_ip_append = data_json_ip_v4 + data_json_ip_v6                  # Put ips together.
    
    # Getting count of itens in variable/key.
    print("Count of IP ranges returned by api.")
    print(len(data_json_ip_append))
    
    # Login aws.
    client = boto3.Session().resource('ec2', region_name=aws_region)
    security_group = client.SecurityGroup(security_group_id)
    
    # Remove all rules, at least one rule have to exist else it could be failed, "try" block avoid this failed.
    try:
        security_group.revoke_ingress(IpPermissions=security_group.ip_permissions)
    
    # Print execption of try failed.
    except Exception as error:
        error_strig = str(error)
        print(error_strig)
    
    # Add rules to the security group.
    for ip_i_all in data_json_ip_append: 
    
        #Filter IPv4 only
        if "." in ip_i_all and "/" in ip_i_all:
            print(ip_i_all)
    
            try:
                # Creating rule for each IP in the list and "port_range_start".
                security_group.authorize_ingress(
                DryRun=False,
                IpPermissions=[
                        {
                            'FromPort': port_range_start,
                            'ToPort': port_range_end,
                            'IpProtocol': protocol,
                            'IpRanges': [
                                {
                                    'CidrIp': ip_i_all,
                                    'Description': description_all
                                },
                            ]
                        }
                    ]
                )
            except Exception as error:
                error_strig = str(error)
                print(error_strig)
    
            try:
                # Creating rule for each IP in the list and "port_2_range_start" .
                security_group.authorize_ingress(
                DryRun=False,
                IpPermissions=[
                        {
                            'FromPort': port_2_range_start,
                            'ToPort': port_2_range_end,
                            'IpProtocol': protocol,
                            'IpRanges': [
                                {
                                    'CidrIp': ip_i_all,
                                    'Description': description_all
                                },
                            ]
                        }
                    ]
                )
            except Exception as error:
                error_strig = str(error)
                print(error_strig)
    
    
        #Filter IPv6 only.
        if ":" in ip_i_all and "/" in ip_i_all:
            print(ip_i_all)
    
            try:
                # Creating rule for each IP in the list and "port_range_start".
                security_group.authorize_ingress(
                DryRun=False,
                IpPermissions=[
                        {
                            'FromPort': port_range_start,
                            'ToPort': port_range_end,
                            'IpProtocol': protocol,
                            'Ipv6Ranges': [
                                {
                                    'CidrIpv6': ip_i_all,
                                    'Description': description_all
                                },
                            ]
                        }
                    ]
                )
            except Exception as error:
                error_strig = str(error)
                print(error_strig)
    
            try:
                # Creating rule for each IP in the list and "port_2_range_start".
                security_group.authorize_ingress(
                DryRun=False,
                IpPermissions=[
                        {
                            'FromPort': port_2_range_start,
                            'ToPort': port_2_range_end,
                            'IpProtocol': protocol,
                            'Ipv6Ranges': [
                                {
                                    'CidrIpv6': ip_i_all,
                                    'Description': description_all
                                },
                            ]
                        }
                    ]
                )
            except Exception as error:
                error_strig = str(error)
                print(error_strig)
