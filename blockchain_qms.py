"""
This script interacts with a Multichain node to publish, update, and retrieve batch records 
related to medical device manufacturing. It leverages blockchain technology to store and verify 
data in a tamper-proof manner.

Main Features:
1. Publish and manage batch records including expiration date, QC test results, deviations, 
   CAPA records, and OOS investigations.
2. Retrieve and display batch history and detect changes between different versions of batch records.
3. Generate and compare fingerprints for data integrity verification.
4. Retrieve batches by expiration date and list all batches in the blockchain.

Requirements:
- Multichain RPC credentials stored in a '.env' file (RPC_USER, RPC_PASSWORD, RPC_HOST, RPC_PORT).
- External dependencies: `requests`, `dotenv`, `binascii`, `data_fingerprint`, `hashlib`.

data_fingerprint is avaliable from the github repository https://github.com/chriswilson2020/data_fingerprint/

Usage:
    python blockchain_script.py <operation> [<args>]

Available Operations:
1. create_batch <batch_key> <manufacture_date> <expiration_date>
2. append_qc_test <batch_key> <test_name> <test_result> <test_hash>
3. update_release_status <batch_key> <new_status>
4. update_expiration_date <batch_key> <new_expiration_date>
5. get_full_batch_record <batch_key>
6. get_batch_history <batch_key>
7. list_all_batches
8. get_batches_by_expiration <expiration_input>
"""

HELP_STRING = """
Blockchain Batch Management Script

Usage:
    python blockchain_script.py <operation> [<args>]

Available Operations:

1. create_batch <batch_key> <manufacture_date> <expiration_date>
   - Create a new batch record.

2. append_qc_test_with_hash <batch_key> <test_name> <test_result> <test_hash>
   - Append a QC test result to a batch, using a provided data hash.

3. append_qc_test_with_file <batch_key> <test_name> <test_result> <file_path>
   - Append a QC test result to a batch, generating a data hash from a file.

4. update_release_status <batch_key> <new_status>
   - Update the release status of a batch.

5. update_expiration_date <batch_key> <new_expiration_date>
   - Update the expiration date of a batch.

6. get_full_batch_record <batch_key>
   - Retrieve the full batch record in JSON format.

7. get_batch_history <batch_key>
   - Retrieve the history of a batch, showing all versions.

8. list_all_batches
   - List all batch numbers stored on the blockchain.

9. get_batches_by_expiration <expiration_input>
   - Retrieve batches by expiration date (formats: YYYY, YYYY-MM, YYYY-MM-DD).

10. get_release_status <batch_key>
    - Get the release status of a batch.

11. get_expiration_date <batch_key>
    - Get the expiration date of a batch.

12. get_manufacture_date <batch_key>
    - Get the manufacture date of a batch.

13. print_full_batch_record <batch_key>
    - Print the full batch record in a human-readable format.

14. get_qc_tests <batch_key>
    - Get all QC tests associated with a batch.

15. append_deviation <batch_key> <deviation_id>
    - Append a deviation record to a batch.

16. append_capa <batch_key> <capa_id>
    - Append a CAPA record to a batch.

17. append_oos <batch_key> <oos_id>
    - Append an OOS investigation to a batch.

18. get_deviations <batch_key>
    - Get all deviations associated with a batch.

19. get_capa <batch_key>
    - Get all CAPA records associated with a batch.

20. get_oos_investigations <batch_key>
    - Get all OOS investigations associated with a batch.

Notes:
- Dates should be in YYYY-MM-DD format unless specified otherwise.
- For more information, please refer to the documentation or README.
"""

import os
import sys
import json
import json
import binascii
import requests
import data_fingerprint
from hashlib import sha256
from dotenv import load_dotenv
from datetime import datetime

# Function to connect to a Multichain node
def connect_to_multichain(method, params=None):
    # Load environment variables from .env file
    load_dotenv('blockchain.env')
    rpc_user = os.getenv('RPC_USER')
    rpc_password = os.getenv('RPC_PASSWORD')
    rpc_host = os.getenv('RPC_HOST')
    rpc_port = os.getenv('RPC_PORT')
    
    # Construct the URL for the RPC connection
    url = f'http://{rpc_user}:{rpc_password}@{rpc_host}:{rpc_port}'
    headers = {'content-type': 'application/json'}
    payload = {
        "method": method,
        "params": params if params else [],
        "jsonrpc": "2.0",
        "id": 1
    }

    response = requests.post(url, data=json.dumps(payload), headers=headers)
    return response.json()

# Function to hash and add data to the blockchain
def put_hash_on_blockchain(data):
    # Hash the data
    hash_object = sha256(data.encode('utf-8')).hexdigest()
    print(f'Hash: {hash_object}')

    # Create a transaction to add the hash to the blockchain
    result = connect_to_multichain('publish', ['root', 'Testing', hash_object])
    return result

def publish_json_to_blockchain(stream_name, key, json_data):
    # Convert JSON object to string
    json_string = json.dumps(json_data)

    # Convert the string to hexadecimal format
    json_hex = binascii.hexlify(json_string.encode('utf-8')).decode('utf-8')

    # Publish the JSON in hex format to the blockchain
    result = connect_to_multichain('publish', [stream_name, key, json_hex])
    return result

def generate_fingerprints(file_path, data_fingerprint):
    # Order-Dependent Fingerprint
    fingerprint_dep = data_fingerprint.process_file_with_order_dependent_fingerprint(file_path)
    
    # Order-Independent Fingerprint
    fingerprint_indep = data_fingerprint.process_file_with_order_independent_fingerprint(file_path)

    return fingerprint_dep, fingerprint_indep

def get_latest_json_from_blockchain(stream_name, key):
    # Retrieve the latest item associated with the given key
    result = connect_to_multichain('liststreamkeyitems', [stream_name, key])

    if result and 'result' in result and len(result['result']) > 0:
        # Get the latest entry (last one in the list)
        json_hex = result['result'][-1]['data']

        # Convert hex back to string
        json_string = binascii.unhexlify(json_hex).decode('utf-8')

        # Parse string as JSON
        json_data = json.loads(json_string)
        return json_data
    else:
        return None

def create_batch_record(batch_key, manufacture_date, expiration_date):
    # Create initial batch JSON
    batch_data = {
        "batch_number": batch_key,
        "manufacture_date": manufacture_date,
        "expiration_date": expiration_date,
        "release_status": "pending",
        "qc_tests": [],
        "deviations": [],
        "CAPA": [],
        "OOS_investigations": []
    }

    # Publish the initial batch record to the blockchain
    result = publish_json_to_blockchain("root", batch_key, batch_data)
    return result

def append_qc_test(batch_key, test_name, test_result, test_hash):
    # Retrieve the latest batch entry
    existing_json = get_latest_json_from_blockchain("root", batch_key)

    if existing_json:
        # Create a new test result entry
        qc_entry = {
            "test_name": test_name,
            "test_result": test_result,
            "test_hash": test_hash
        }

        # Append the new test result and hash to the qc_tests list
        existing_json['qc_tests'].append(qc_entry)

        # Republish the updated batch record with the appended QC test
        publish_json_to_blockchain("root", batch_key, existing_json)
        print("QC test result and hash appended successfully.")
    else:
        print("No batch data found to update.")

def update_release_status(batch_key, new_status):
    # Retrieve the latest batch entry
    existing_json = get_latest_json_from_blockchain("root", batch_key)

    if existing_json:
        # Update release status
        existing_json['release_status'] = new_status

        # Republish the updated batch record
        publish_json_to_blockchain("root", batch_key, existing_json)
        print("Release status updated successfully.")
    else:
        print("No batch data found to update.")


def append_deviation(batch_key, deviation_id):
    existing_json = get_latest_json_from_blockchain("root", batch_key)

    if existing_json:
        # Append new deviation
        existing_json['deviations'].append(deviation_id)

        # Republish the updated batch record
        publish_json_to_blockchain("root", batch_key, existing_json)
        print("Deviation appended successfully.")
    else:
        print("No batch data found to update.")

def append_capa(batch_key, capa_id):
    existing_json = get_latest_json_from_blockchain("root", batch_key)

    if existing_json:
        # Append new CAPA
        existing_json['CAPA'].append(capa_id)

        # Republish the updated batch record
        publish_json_to_blockchain("root", batch_key, existing_json)
        print("CAPA appended successfully.")
    else:
        print("No batch data found to update.")

def append_oos(batch_key, oos_id):
    existing_json = get_latest_json_from_blockchain("root", batch_key)

    if existing_json:
        # Append new OOS investigation
        existing_json['OOS_investigations'].append(oos_id)

        # Republish the updated batch record
        publish_json_to_blockchain("root", batch_key, existing_json)
        print("OOS investigation appended successfully.")
    else:
        print("No batch data found to update.")


def get_qc_tests(batch_key):
    # Retrieve the latest batch entry
    existing_json = get_latest_json_from_blockchain("root", batch_key)

    if existing_json:
        # Check if 'qc_tests' exists
        if 'qc_tests' in existing_json:
            if len(existing_json['qc_tests']) > 0:
                # If qc_tests list has entries, print them
                for test in existing_json['qc_tests']:
                    print(f"Test: {test['test_name']}, Result: {test['test_result']}, Hash: {test['test_hash']}")
            else:
                # If qc_tests exists but is empty
                print("No QC tests have been appended to this batch yet.")
        else:
            # If qc_tests field does not exist at all
            print("'qc_tests' field does not exist in this batch record.")
    else:
        print("No batch data found for this key.")



def get_capa(batch_key):
    existing_json = get_latest_json_from_blockchain("root", batch_key)

    if existing_json:
        if 'CAPA' in existing_json:
            if len(existing_json['CAPA']) > 0:
                print(f"CAPA records for batch {batch_key}: {existing_json['CAPA']}")
            else:
                print("No CAPA records found for this batch.")
        else:
            print("'CAPA' field does not exist in this batch record.")
    else:
        print("No batch data found for this key.")


def get_deviation(batch_key):
    existing_json = get_latest_json_from_blockchain("root", batch_key)

    if existing_json:
        if 'deviations' in existing_json:
            if len(existing_json['deviations']) > 0:
                print(f"Deviations for batch {batch_key}: {existing_json['deviations']}")
            else:
                print("No deviations found for this batch.")
        else:
            print("'deviations' field does not exist in this batch record.")
    else:
        print("No batch data found for this key.")

def get_oos_investigations(batch_key):
    existing_json = get_latest_json_from_blockchain("root", batch_key)

    if existing_json:
        if 'OOS_investigations' in existing_json:
            if len(existing_json['OOS_investigations']) > 0:
                print(f"OOS investigations for batch {batch_key}: {existing_json['OOS_investigations']}")
            else:
                print("No OOS investigations found for this batch.")
        else:
            print("'OOS_investigations' field does not exist in this batch record.")
    else:
        print("No batch data found for this key.")


def get_release_status(batch_key):
    existing_json = get_latest_json_from_blockchain("root", batch_key)

    if existing_json:
        if 'release_status' in existing_json:
            print(f"Release status for batch {batch_key}: {existing_json['release_status']}")
        else:
            print("'release_status' field does not exist in this batch record.")
    else:
        print("No batch data found for this key.")


def get_expiration_date(batch_key):
    existing_json = get_latest_json_from_blockchain("root", batch_key)

    if existing_json:
        if 'expiration_date' in existing_json:
            print(f"Expiration date for batch {batch_key}: {existing_json['expiration_date']}")
        else:
            print("'expiration_date' field does not exist in this batch record.")
    else:
        print("No batch data found for this key.")


def get_full_batch_record(batch_key):
    existing_json = get_latest_json_from_blockchain("root", batch_key)

    if existing_json:
        # Print the full JSON record nicely formatted
        print(json.dumps(existing_json, indent=4))
    else:
        print(f"No batch data found for batch key {batch_key}.")


def get_manufacture_date(batch_key):
    existing_json = get_latest_json_from_blockchain("root", batch_key)

    if existing_json:
        if 'manufacture_date' in existing_json:
            print(f"Manufacture date for batch {batch_key}: {existing_json['manufacture_date']}")
        else:
            print("'manufacture_date' field does not exist in this batch record.")
    else:
        print("No batch data found for this key.")


def print_human_readable_batch_record(batch_record):
    if batch_record:
        print(f"Batch Number: {batch_record.get('batch_number', 'N/A')}")
        print(f"Manufacture Date: {batch_record.get('manufacture_date', 'N/A')}")
        print(f"Expiration Date: {batch_record.get('expiration_date', 'N/A')}")
        print(f"Release Status: {batch_record.get('release_status', 'N/A')}")
        
        # Printing QC Tests
        print("\nQC Test Results:")
        if 'qc_tests' in batch_record and batch_record['qc_tests']:
            for test in batch_record['qc_tests']:
                print(f"  - Test Name: {test.get('test_name', 'N/A')}")
                print(f"    Result: {test.get('test_result', 'N/A')}")
                print(f"    Hash: {test.get('test_hash', 'N/A')}")
        else:
            print("  No QC tests have been recorded.")
        
        # Printing Deviation Records
        print("\nDeviations:")
        if 'deviations' in batch_record and batch_record['deviations']:
            for deviation in batch_record['deviations']:
                print(f"  - {deviation}")
        else:
            print("  No deviations recorded.")
        
        # Printing CAPA Records
        print("\nCAPA Records:")
        if 'CAPA' in batch_record and batch_record['CAPA']:
            for capa in batch_record['CAPA']:
                print(f"  - {capa}")
        else:
            print("  No CAPA records found.")
        
        # Printing OOS Investigations
        print("\nOOS Investigations:")
        if 'OOS_investigations' in batch_record and batch_record['OOS_investigations']:
            for oos in batch_record['OOS_investigations']:
                print(f"  - {oos}")
        else:
            print("  No OOS investigations recorded.")
    else:
        print("No batch data found.")

def get_batch_history(batch_key):
    # Retrieve all entries associated with the given batch key
    result = connect_to_multichain('liststreamkeyitems', ['root', batch_key])

    if result and 'result' in result and len(result['result']) > 0:
        print(f"History of batch {batch_key}:")
        # Loop through each iteration of the record
        for index, item in enumerate(result['result'], 1):
            # Decode the hex data into JSON format
            json_hex = item['data']
            json_string = binascii.unhexlify(json_hex).decode('utf-8')
            batch_record = json.loads(json_string)
            
            # Print the version number and the JSON object
            print(f"\nVersion {index}:")
            print(json.dumps(batch_record, indent=4))
    else:
        print(f"No history found for batch {batch_key}.")
        
def find_changes(old_version, new_version):
    changes = {}
    for key in new_version:
        if key not in old_version:
            changes[key] = {"old": None, "new": new_version[key]}
        elif old_version[key] != new_version[key]:
            changes[key] = {"old": old_version[key], "new": new_version[key]}
    return changes

def get_batch_changes(batch_key):
    # Retrieve all entries associated with the given batch key
    result = connect_to_multichain('liststreamkeyitems', ['root', batch_key])

    if result and 'result' in result and len(result['result']) > 0:
        print(f"Changes in batch {batch_key}:")
        previous_version = None

        # Loop through each iteration of the record
        for index, item in enumerate(result['result'], 1):
            # Decode the hex data into JSON format
            json_hex = item['data']
            json_string = binascii.unhexlify(json_hex).decode('utf-8')
            current_version = json.loads(json_string)

            # If there is a previous version, compare and find changes
            if previous_version is not None:
                changes = find_changes(previous_version, current_version)
                if changes:
                    print(f"\nChanges from Version {index - 1} to Version {index}:")
                    for key, change in changes.items():
                        print(f"  - {key}:")
                        print(f"    Old: {change['old']}")
                        print(f"    New: {change['new']}")
                else:
                    print(f"\nNo changes from Version {index - 1} to Version {index}.")
            else:
                print(f"\nInitial Version (Version {index}):")
                print(json.dumps(current_version, indent=4))

            # Set the current version as the previous one for the next comparison
            previous_version = current_version
    else:
        print(f"No history found for batch {batch_key}.")

def get_batches_by_expiration(expiration_input):
    # Convert input to datetime format based on the user's input
    try:
        # Try to parse the input in different formats: year, month-year, or day-month-year
        if len(expiration_input) == 4:  # Year only (e.g., '2026')
            expiration_target = datetime.strptime(expiration_input, '%Y')
            check_format = 'year'
        elif len(expiration_input) == 7:  # Month-Year (e.g., '2026-09')
            expiration_target = datetime.strptime(expiration_input, '%Y-%m')
            check_format = 'month'
        elif len(expiration_input) == 10:  # Day-Month-Year (e.g., '2026-09-23')
            expiration_target = datetime.strptime(expiration_input, '%Y-%m-%d')
            check_format = 'day'
        else:
            raise ValueError("Invalid date format. Use 'YYYY', 'YYYY-MM', or 'YYYY-MM-DD'.")
    except ValueError as e:
        print(f"Error parsing date: {e}")
        return

    # Retrieve all entries from the stream ('root' stream)
    result = connect_to_multichain('liststreamitems', ['root'])

    if result and 'result' in result and len(result['result']) > 0:
        latest_batches = {}  # Store the latest version of each batch

        # Loop through all items in the stream
        for item in result['result']:
            # Decode the hex data into JSON format
            json_hex = item['data']
            json_string = binascii.unhexlify(json_hex).decode('utf-8')
            batch_record = json.loads(json_string)

            # Check if the batch has an expiration_date field
            if 'expiration_date' in batch_record:
                # Parse the expiration date from the batch record
                expiration_date = datetime.strptime(batch_record['expiration_date'], '%Y-%m-%d')

                # Store the latest version of the batch (based on batch number)
                batch_number = batch_record['batch_number']
                latest_batches[batch_number] = batch_record

        # Now filter the latest batch versions by the expiration criteria
        batches_expiring_in_criteria = []
        for batch_number, batch_record in latest_batches.items():
            expiration_date = datetime.strptime(batch_record['expiration_date'], '%Y-%m-%d')
            
            # Check if the expiration date matches the criteria
            if check_format == 'year' and expiration_date.year == expiration_target.year:
                batches_expiring_in_criteria.append(batch_record)
            elif check_format == 'month' and expiration_date.year == expiration_target.year and expiration_date.month == expiration_target.month:
                batches_expiring_in_criteria.append(batch_record)
            elif check_format == 'day' and expiration_date == expiration_target:
                batches_expiring_in_criteria.append(batch_record)

        # Print out the batches that match the expiration input
        if batches_expiring_in_criteria:
            print(f"Batches expiring in {expiration_input}:")
            for batch in batches_expiring_in_criteria:
                print(f"  - Batch Number: {batch['batch_number']}, Expiration Date: {batch['expiration_date']}")
        else:
            print(f"No batches expiring in {expiration_input} were found.")
    else:
        print("No batch records found in the blockchain.")
def update_expiration_date(batch_key, new_expiration_date):
    # Retrieve the latest batch entry
    existing_json = get_latest_json_from_blockchain("root", batch_key)

    if existing_json:
        try:
            # Validate the new expiration date format (YYYY-MM-DD)
            new_expiration_date_parsed = datetime.strptime(new_expiration_date, '%Y-%m-%d')
        except ValueError:
            print(f"Error: The provided expiration date '{new_expiration_date}' is not in the correct format (YYYY-MM-DD).")
            return
        
        # Update the expiration date
        existing_json['expiration_date'] = new_expiration_date
        
        # Publish the updated batch record with the new expiration date
        result = publish_json_to_blockchain("root", batch_key, existing_json)
        if result:
            print(f"Expiration date for batch {batch_key} has been successfully updated to {new_expiration_date}.")
        else:
            print(f"Failed to update the expiration date for batch {batch_key}.")
    else:
        print(f"No batch data found for key: {batch_key}.")

def list_all_batches():
    # Retrieve all entries from the stream ('root' stream)
    result = connect_to_multichain('liststreamitems', ['root'])

    if result and 'result' in result and len(result['result']) > 0:
        batch_numbers = set()  # Use a set to store unique batch numbers

        # Loop through all items in the stream
        for item in result['result']:
            # Decode the hex data into JSON format
            json_hex = item['data']
            json_string = binascii.unhexlify(json_hex).decode('utf-8')
            batch_record = json.loads(json_string)

            # Add the batch number to the set
            if 'batch_number' in batch_record:
                batch_numbers.add(batch_record['batch_number'])

        # Output the list of unique batch numbers
        if batch_numbers:
            print("List of all unique batches on the blockchain:")
            for batch_number in batch_numbers:
                print(f"  - Batch Number: {batch_number}")
        else:
            print("No batches found on the blockchain.")
    else:
        print("No batch records found in the blockchain.")


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ('-h', '--help'):
        print(HELP_STRING)
        sys.exit(1)
        
    operation = sys.argv[1]

    if operation == "create_batch":
        if len(sys.argv) != 5:
            print("Usage: create_batch <batch_key> <manufacture_date> <expiration_date>")
            sys.exit(1)
        batch_key = sys.argv[2]
        manufacture_date = sys.argv[3]
        expiration_date = sys.argv[4]
        create_batch_record(batch_key, manufacture_date, expiration_date)

    elif operation == "append_qc_test_with_hash":
        if len(sys.argv) != 6:
            print("Usage: append_qc_test <batch_key> <test_name> <test_result> <test_hash>")
            sys.exit(1)
        batch_key = sys.argv[2]
        test_name = sys.argv[3]
        test_result = sys.argv[4]
        test_hash = sys.argv[5]
        append_qc_test(batch_key, test_name, test_result, test_hash)

    elif operation == "append_qc_test_with_file":
        if len(sys.argv) != 6:
            print("Usage: append_qc_test <batch_key> <test_name> <test_result> <test_hash>")
            sys.exit(1)
        batch_key = sys.argv[2]
        test_name = sys.argv[3]
        test_result = sys.argv[4]
        test_hash = sys.argv[5]
        fingerprint_dep = data_fingerprint.process_file_with_order_dependent_fingerprint(test_hash)
        append_qc_test(batch_key, test_name, test_result, fingerprint_dep)

    elif operation == "update_release_status":
        if len(sys.argv) != 4:
            print("Usage: update_release_status <batch_key> <new_status>")
            sys.exit(1)
        batch_key = sys.argv[2]
        new_status = sys.argv[3]
        update_release_status(batch_key, new_status)

    elif operation == "update_expiration_date":
        if len(sys.argv) != 4:
            print("Usage: update_expiration_date <batch_key> <new_expiration_date>")
            sys.exit(1)
        batch_key = sys.argv[2]
        new_expiration_date = sys.argv[3]
        update_expiration_date(batch_key, new_expiration_date)

    elif operation == "get_full_batch_record":
        if len(sys.argv) != 3:
            print("Usage: get_full_batch_record <batch_key>")
            sys.exit(1)
        batch_key = sys.argv[2]
        get_full_batch_record(batch_key)

    elif operation == "get_batch_history":
        if len(sys.argv) != 3:
            print("Usage: get_batch_history <batch_key>")
            sys.exit(1)
        batch_key = sys.argv[2]
        get_batch_history(batch_key)

    elif operation == "list_all_batches":
        list_all_batches()

    elif operation == "get_batches_by_expiration":
        if len(sys.argv) != 3:
            print("Usage: get_batches_by_expiration <expiration_input (YYYY or YYYY-MM or YYYY-MM-DD)>")
            sys.exit(1)
        expiration_input = sys.argv[2]
        get_batches_by_expiration(expiration_input)

    elif operation == "get_release_status":
        if len(sys.argv) != 3:
            print("Usage: get_release_status <batch_key>")
            sys.exit(1)
        batch_key = sys.argv[2]
        get_release_status(batch_key)

    elif operation == "get_expiration_date":
        if len (sys.argv) != 3:
            print("Useage: get_expiration_date <batch_key>")
            sys.exit(1)
        batch_key = sys.argv[2]
        get_expiration_date(batch_key)
    
    elif operation == "get_manufacture_date":
        if len (sys.argv) != 3:
            print("Useage: get_manufacture_date <batch_key>")
            sys.exit(1)
        batch_key = sys.argv[2]
        get_manufacture_date(batch_key)
        
    elif operation == "print_full_batch_record":
        if len(sys.argv) != 3:
            print("Usage: print_full_batch_record <batch_key>")
            sys.exit(1)
        batch_key = sys.argv[2]
        print_human_readable_batch_record(get_latest_json_from_blockchain("root", batch_key))

    elif operation == "get_qc_tests":
        if len (sys.argv) != 3:
            print("Useage: get_qc_tests <batch_key>")
            sys.exit(1)
        batch_key = sys.argv[2]
        get_qc_tests(batch_key)

    elif operation == "append_deviation":
        if len(sys.argv) != 4:
            print("Usage: append_deviation <batch_key> <dev_number>")
            sys.exit(1)
        batch_key = sys.argv[2]
        deviation_id = sys.argv[3]
        append_deviation(batch_key, deviation_id)

    elif operation == "append_oos":
        if len(sys.argv) != 4:
            print("Usage: append_deviation <batch_key> <dev_number>")
            sys.exit(1)
        batch_key = sys.argv[2]
        oos_id = sys.argv[3]
        append_oos(batch_key, oos_id)

    elif operation == "append_capa":
        if len(sys.argv) != 4:
            print("Usage: append_deviation <batch_key> <dev_number>")
            sys.exit(1)
        batch_key = sys.argv[2]
        capa_id = sys.argv[3]
        append_capa(batch_key, capa_id)
        
    elif operation == "get_deviations":
        if len (sys.argv) != 3:
            print("Useage: get_deviations <batch_key>")
            sys.exit(1)
        batch_key = sys.argv[2]
        get_deviation(batch_key)
        
    elif operation == "get_oos_investigations":
        if len (sys.argv) != 3:
            print("Useage: get_oos_investigations <batch_key>")
            sys.exit(1)
        batch_key = sys.argv[2]
        get_oos_investigations(batch_key)

    elif operation == "get_capa":
        if len (sys.argv) != 3:
            print("Useage: get_capa <batch_key>")
            sys.exit(1)
        batch_key = sys.argv[2]
        get_capa(batch_key)
    
    else:
        print(f"Error: Unknown operation '{operation}'.")
        sys.exit(1)

if __name__ == "__main__":
    main()