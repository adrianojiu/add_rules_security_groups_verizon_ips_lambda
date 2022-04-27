# add_rules_security_groups_verizon_ips_lambda

This script can be used in a lambda function to add Verizon cdn ips in a security group automatically.
The script add IPv4 and IPv6.
Ask AWS to increase the number of rules per security group to 200 before run it, it can take few days.
To trigger this function you can use Jenkins, Run Deck or a simple cron but I recommend user AWS CloudWatch Events and trigger that at least once a day.

To trigger manually:

aws lambda invoke --function-name PUT_YOUR_LAMBDA_FUNCTION_NAME_HERE output.json

Look to file roleExample.yml to see a policy example for a lambda role, dont forget do insert your account id in "insert your account id here", maybe you don´t need give permission to S3 it´s yout choise remove s3 from a policy.

