<h1 align="center" style="border-bottom: none">
    <a href="//docs.aws.amazon.com" target="_blank"><img alt="RDS Custom Endpoint" src="/documentation/images/og.jpeg"></a><br>RDS Connectify
</h1>

<p align="center">Visit <a href="https://docs.aws.amazon.com/AmazonRDS/latest/APIReference/API_CreateDBClusterEndpoint.html" target="_blank">docs.aws.amazon.com</a> for the full documentation,
examples and guides.</p>

## Overview

`rdsconnectify.py` is a Python script designed to facilitate the management of Amazon RDS (Relational Database Service) custom endpoints. This script allows users to create and modify RDS custom endpoints in different AWS regions.

## Why should we use Tool?
### Advantages of Using Tool
1. As you know, RDS Custom Endpoint can be done via AWS Console. However, we cannot determine the Enpoint type for the relevant RDS Custom Endpoint on the AWS Console. Using this tool, we can now select the type of RDS Custom Endpoint. AWS CLI gives us this advantage. Tool simplifies the process.
2. At the same time, unlike AWS Console, choosing a Static identifier or Exclude Identifier when using the Tool has a more simplified usage.
3. In addition to the above advantages, I decided to further enrich the RDS Custom Endpoint creation process by adding it to the Tool. In this way, we can perform the attached operations one by one using the tool.
   1. Creating an RDS Custom Endpoint
   2. Giving RDS Custom Endpoint Type
   3. Selecting an RDS Custom Endpoint Static instance
   4. Selecting RDS Custom Endpoint Exclude instance

## RDSConnectify Tool Usage Result Scenarios are attached:
1. If we choose Create RDS Custom Endpoint, we have to give the Endpoint Type. If we simply proceed with the Create RDS Custom Endpoint option, we will have a new Custom Enpoint of the type we specified as a result. However, Endpoint will not send traffic to any instance in the back.
2. If we add the Modify Custom Enpoint Option in addition to the Create RDS Custom Endpoint option, then as a result we will have a new RDS Custom Endpoint and we will use options such as Type, Static instance selection and Exlude instance on the Enpoint we have determined.
   1. Custom Endpoint Type consists of 3 certificates. You can only give ANY, READER and WRITER options to the Endpoint you created.
   2. If you use the Exclude member option, no traffic will go to the instance you select via the relevant Enpoint. But keep in mind that you can only select one instance in the Exclude member option and you need to restart the tool to add another instance. At the same time, if you choose the Exclude Member option, then your structure will be Dynamic. So, each newly added instance will actually be added to this Custom Endpoint.
   3. Static instance selection works completely opposite to the Exlude member feature. So you can only choose one of these two options. If you continue with the Static instance selection process, then the structure will also be Static and traffic will be directed only to the instances you specify. At the same time, each newly added instance will not be added to this Endpoint. But remember that the Static instance option can only select one instance, and you need to restart the tool to add another instance.

## Prerequisites

Before using `rdsconnectify.py`, ensure that you have the following prerequisites installed on your local machine:

- Python 3
- AWS CLI (Command Line Interface)

### Addictions and Libraries

1. python 3
   1. pip3
   2. sys
   3. json
   4. subprocess
   5. time

To install AWS CLI, you can follow the instructions provided in the [official documentation](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html).

## Installation

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/thebadalov/RDSConnectify.git

2. Navigate to the project directory:
   ```bash
   cd RDSConnectify
3. Make the script executable:
   ```bash
   chmod +x rdsconnectify.py
4. Move the script to the bin directory:
   ```bash
   mv rdsconnectify.py /usr/local/bin/rdsconnectify

Now, you can run the script from any location on your machine by typing rdsconnectify in the terminal.

## Usage

### Running the Script

To execute the script, open a terminal and run the following command:

1. ```bash
   rdsconnectify

Follow the on-screen instructions to interact with the script.

## Selecting AWS Region
The script will prompt you to enter the name of the AWS region where you want to perform the RDS operations.

## Creating a Custom Endpoint
If you choose to create a custom endpoint, the script will ask for the custom endpoint identifier, RDS cluster identifier, and endpoint type (ANY/READER/WRITER).

The AWS CLI command will be generated and executed to create the custom endpoint.

The process may take some time, and the script will notify you upon completion.

## Modifying a Custom Endpoint
If you choose to modify a custom endpoint, the script will ask if you want to modify the static member or exclude member.

Depending on your selection, additional information may be required.

The AWS CLI command will be generated and executed to modify the custom endpoint.

The process may take some time, and the script will notify you upon completion.

## Exiting the Script
If you do not select any operation (create or modify), the script will exit, and no changes will be made.

## Important Notes
1. Ensure that you have the necessary AWS IAM (Identity and Access Management) permissions to perform RDS operations in the selected region.

2. If an error occurs during script execution, check the error message for details and make necessary corrections.

3. Before running the command, make sure that you are connected to AWS and that you have entered the correct Access and Secret key information on the relevant Account!!!

## Contribution
Contributions to improve and enhance the functionality of the script are welcome. Feel free to fork the repository, make changes, and submit a pull request.

## License
This script is open-source and available under the MIT License. Feel free to use, modify, and distribute it.

## Contributors ✨

<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://www.linkedin.com/in/elman-badalov-284504150/"><img src="https://media.licdn.com/dms/image/C4D03AQHqGfSEnoLeyA/profile-displayphoto-shrink_200_200/0/1622403964253?e=1706745600&v=beta&t=Cu9Qg-NgwTxII2t3zD0Eqm35E_LvsrMGXyVzMDXAMbo" width="100px;" alt="Elman Badalov"/><br /><sub><b>Elman Badalov</b></sub></a><br /><a href="" title="Cloud Native Engineer Tech Lead">💻</a></td>
    </tr>
  </tbody>
</table>