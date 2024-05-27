#!/usr/bin/env python3
import json
import subprocess
import time
import sys

def check_rds_exists(region):
    try:
        result = subprocess.run(['aws', 'rds', 'describe-db-instances', '--region', region], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        response_json = json.loads(result.stdout)
        db_instances = response_json.get('DBInstances', [])
        return bool(db_instances)
    except subprocess.CalledProcessError:
        return False

def get_boolean_input(prompt):
    while True:
        user_input = input(prompt + " (Yes/No): ").lower()
        if user_input == 'yes':
            return True
        elif user_input == 'no':
            return False
        else:
            print('Please give a valid answer.')

def check_status_of_custom_endpoint(rds_custom_endpoint_identifier,selected_region):
    while True:
        # Check the endpoint status using describe-db-cluster-endpoints command
        describe_command = f"aws rds describe-db-cluster-endpoints --db-cluster-endpoint-identifier {rds_custom_endpoint_identifier} --region {selected_region}"
        describe_process = subprocess.run(describe_command, shell=True, capture_output=True, text=True)

        # Parse the JSON output to get the endpoint status
        endpoint_info = json.loads(describe_process.stdout)
        endpoint_status = endpoint_info['DBClusterEndpoints'][0]['Status']
        if endpoint_status == "available":
            return True
        # Wait for a few seconds before checking again
        time.sleep(10)

def main():
    print("We start operations on RDS Custom Endpoint. Welcome :)")
    regions = {
        'us-east-1': 1,
        'us-east-2': 2,
        'us-west-1': 3,
        'us-west-2': 4,
        'af-south-1': 5,
        'ap-east-1': 6,
        'ap-south-1': 7,
        'ap-northeast-1': 8,
        'ap-northeast-2': 9,
        'ap-northeast-3': 10,
        'ap-southeast-1': 11,
        'ap-southeast-2': 12,
        'ca-central-1': 13,
        'cn-north-1': 14,
        'cn-northwest-1': 15,
        'eu-central-1': 16,
        'eu-west-1': 17,
        'eu-west-2': 18,
        'eu-west-3': 19,
        'eu-north-1': 20,
        'me-south-1': 21,
        'sa-east-1': 22,
    }
    while True:
        print("Could you enter the name of the Region where you will work:")
        for region, option in regions.items():
            print(f"{region}: {option}")

        selected_option = input("Enter the number of the option: ")

        # Checking the option entered by the user
        if selected_option.isdigit() and 1 <= int(selected_option) <= len(regions):
            selected_region = list(regions.keys())[int(selected_option) - 1]
            print(f"Selected Region: {selected_region}")
            # Check if there is an RDS instance in the specified region
            if not check_rds_exists(selected_region):
                print(f'Error: RDS has not been started yet for the specified region. -- ({selected_region}) ')
                return {
                    'statusCode': 400,
                    'body': json.dumps(f'Hata: Belirtilen region ({selected_region}) için henüz RDS başlatılmamış.')
                }
            break # Exit the loop if a correct option is entered
        else:
            print("Invalid option. Please enter a valid option number.")
            print("\n----------------------------------------------------------")

    rds_custom_endpoint_identifier = None
    rds_cluster_identifier = None

    rds_custom_endpoint_identifier = input('RDS Custom Endpoint Identifier (for using Create or Modify Operation): ')
    rds_cluster_identifier = input('RDS Cluster Identifier (for using Create or Modify Operation): ')
    valid_endpoint_types = ['ANY', 'READER', 'WRITER']
    while True:
        modify_endpoint_type = input("Add Endpoint Type for using Create or Modify Operation (ANY/READER/WRITER): ").upper()

        if modify_endpoint_type in valid_endpoint_types:
            print(f"Selected Endpoint Type: {modify_endpoint_type}")
            break  # Exit the loop if a correct option is entered
        else:
            print("Invalid option. Please enter a valid option.")

    if not rds_custom_endpoint_identifier or not rds_cluster_identifier:
        print('Error: RDS Custom Endpoint Identifier and RDS Cluster Identifier must be specified. Please try again :)')
        return {
            'statusCode': 400,
            'body': json.dumps('Error: rdsCustomEndpointIdentifier and rdsClusterIdentifier must be specified.')
        }
    
    rds_create_custom_endpoint = get_boolean_input('Create RDS Custom Endpoint?')
    rds_modify_custom_endpoint = get_boolean_input('Modify RDS Custom Endpoint?')
    
    modify_static_member = modify_exclude_member = None
    if rds_modify_custom_endpoint:
        modify_static_member = input('Modify Static Member (if you want to enter a value or just click to enter)?')
        if modify_static_member:  # If modify_static_member value is entered, modify_exclude_member is not asked
            modify_exclude_member = None
        else:
            modify_exclude_member = input('Modify Exclude Member: ')

    if rds_create_custom_endpoint:
        # Generate AWS CLI commands   
        if rds_create_custom_endpoint:
            print("Custom Endpoint creation process has started...")
            aws_command = (f"aws rds create-db-cluster-endpoint --db-cluster-identifier {rds_cluster_identifier} --db-cluster-endpoint-identifier {rds_custom_endpoint_identifier} --endpoint-type {modify_endpoint_type} --region {selected_region} > /dev/null ")
            process = subprocess.run(aws_command, shell=True)
            if process.returncode == 0:
                # If process command is Success.
                if check_status_of_custom_endpoint(rds_custom_endpoint_identifier,selected_region):
                    print("Custom Endpoint creation is completed...")
            else:
                # In case of error, it falls here and you can stop the process
                print(f"An error occurred. Error code: {process.returncode}")
                sys.exit()

    # Generate AWS CLI commands

    if rds_modify_custom_endpoint:
        print("Custom Endpoint Modification process has started...")

        aws_command = f"aws rds modify-db-cluster-endpoint --db-cluster-endpoint-identifier {rds_custom_endpoint_identifier}"

        if modify_static_member:
            aws_command += f" --static-members {modify_static_member}"

        if modify_exclude_member:
            aws_command += f" --excluded-members {modify_exclude_member}"

        if modify_endpoint_type:
            aws_command += f" --endpoint-type {modify_endpoint_type}"

        aws_command += f" --region {selected_region} > /dev/null"

        process = subprocess.run(aws_command, shell=True)
        if process.returncode == 0:
            # If process command is Success.
            if check_status_of_custom_endpoint(rds_custom_endpoint_identifier,selected_region):
                print("Custom Endpoint Modification process completed...")
                print("The work has been completed. We wait again :)")
            sys.exit()
        else:
            # In case of error, it falls here and you can stop the process
            print(f"An error occurred. Error code: {process.returncode}")
            sys.exit()
    print("Sorry.. The work could not be done because you did not select an action :)")
main()