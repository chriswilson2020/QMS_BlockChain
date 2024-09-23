# Blockchain Batch Management Script

This script provides a command-line interface to interact with a Multichain node for managing batch records in the medical device manufacturing industry. It leverages blockchain technology to securely store and verify data, ensuring tamper-proof records of batch information.

## Features

- **Create and Manage Batch Records**: Publish new batch records with manufacturing and expiration dates, and manage their lifecycle through various operations.
- **Quality Control (QC) Tests Management**: Append QC test results to batch records, including test names, results, and associated data hashes for integrity verification.
- **Deviation, CAPA, and OOS Investigations**: Record deviations, Corrective and Preventive Actions (CAPA), and Out-of-Specification (OOS) investigations associated with batches.
- **Batch Release Status Updates**: Update the release status of batches (e.g., pending, released, hold).
- **Batch Data Retrieval**: Retrieve full batch records, batch histories with versioning, and filter batches by expiration dates.
- **Data Integrity Verification**: Generate and compare data fingerprints using order-dependent and order-independent hashing methods.

## Installation

### Prerequisites

- **Python 3.x**
- **Multichain Node**: Access to a Multichain node with RPC credentials.
- To setup a simple network using multichain you can follow the instructions [here](https://github.com/chriswilson2020/Multichain_setup/)
- **Environment Variables**: A `.env` file containing the following variables:
  - `RPC_USER`
  - `RPC_PASSWORD`
  - `RPC_HOST`
  - `RPC_PORT`

### Clone the Repository

```bash
git clone https://github.com/chriswilson2020/QMS_BlockChain.git
cd blockchain_batch_management
```
### Install Dependencies
Install the required Python packages:
```bash
pip install -r requirements.txt
```

Note: The data_fingerprint module is available as a standalone module at https://github.com/chriswilson2020/data_fingerprint/


#### Setup Environment Variables
Create a .env file in the project root directory with the following content (an example is included for you to edit also):
```makefile
RPC_USER=your_rpc_username
RPC_PASSWORD=your_rpc_password
RPC_HOST=localhost
RPC_PORT=your_rpc_port
```

### Usage
You can use the script either standalone or by including it into your jupyter notebook

#### Standalone
```bash
python blockchain_script.py <operation> [<args>]
```

| Use Case                                           | Operation                   | Arguments                                                    | Example                                                                                                                               |
|----------------------------------------------------|-----------------------------|--------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------|
| Create a new batch record                          | `create_batch`              | `<batch_key>` `<manufacture_date>` `<expiration_date>`       | `python blockchain_script.py create_batch BATCH123 2023-10-01 2025-10-01`                                                             |
| Append a QC test result with external hash         | `append_qc_test_with_hash`  | `<batch_key>` `<test_name>` `<test_result>` `<test_hash>`    | `python blockchain_script.py append_qc_test_with_hash BATCH123 "Sterility Test" "Pass" abcdef123456...`                               |
| Append a QC test result, generate hash from file   | `append_qc_test_with_file`  | `<batch_key>` `<test_name>` `<test_result>` `<file_path>`    | `python blockchain_script.py append_qc_test_with_file BATCH123 "Sterility Test" "Pass" /path/to/test_result.txt`                      |
| Update the release status of a batch               | `update_release_status`     | `<batch_key>` `<new_status>`                                 | `python blockchain_script.py update_release_status BATCH123 released`                                                                 |
| Update the expiration date of a batch              | `update_expiration_date`    | `<batch_key>` `<new_expiration_date>`                        | `python blockchain_script.py update_expiration_date BATCH123 2025-12-31`                                                              |
| Retrieve the full batch record in JSON format      | `get_full_batch_record`     | `<batch_key>`                                                | `python blockchain_script.py get_full_batch_record BATCH123`                                                                          |
| Retrieve the history of a batch                    | `get_batch_history`         | `<batch_key>`                                                | `python blockchain_script.py get_batch_history BATCH123`                                                                              |
| List all batch numbers stored on the blockchain    | `list_all_batches`          | None                                                         | `python blockchain_script.py list_all_batches`                                                                                        |
| Retrieve batches by expiration date                | `get_batches_by_expiration` | `<expiration_input>` (formats: `YYYY`, `YYYY-MM`, `YYYY-MM-DD`)| `python blockchain_script.py get_batches_by_expiration 2025-12`                                                                       |
| Get the release status of a batch                  | `get_release_status`        | `<batch_key>`                                                | `python blockchain_script.py get_release_status BATCH123`                                                                             |
| Get the expiration date of a batch                 | `get_expiration_date`       | `<batch_key>`                                                | `python blockchain_script.py get_expiration_date BATCH123`                                                                            |
| Get the manufacture date of a batch                | `get_manufacture_date`      | `<batch_key>`                                                | `python blockchain_script.py get_manufacture_date BATCH123`                                                                           |
| Print the full batch record in human-readable form | `print_full_batch_record`   | `<batch_key>`                                                | `python blockchain_script.py print_full_batch_record BATCH123`                                                                        |
| Get all QC tests associated with a batch           | `get_qc_tests`              | `<batch_key>`                                                | `python blockchain_script.py get_qc_tests BATCH123`                                                                                   |
| Append a deviation record to a batch               | `append_deviation`          | `<batch_key>` `<deviation_id>`                               | `python blockchain_script.py append_deviation BATCH123 DEV001`                                                                        |
| Append a CAPA record to a batch                    | `append_capa`               | `<batch_key>` `<capa_id>`                                    | `python blockchain_script.py append_capa BATCH123 CAPA001`                                                                            |
| Append an OOS investigation to a batch             | `append_oos`                | `<batch_key>` `<oos_id>`                                     | `python blockchain_script.py append_oos BATCH123 OOS001`                                                                              |
| Get all deviations associated with a batch         | `get_deviations`            | `<batch_key>`                                                | `python blockchain_script.py get_deviations BATCH123`                                                                                 |
| Get all CAPA records associated with a batch       | `get_capa`                  | `<batch_key>`                                                | `python blockchain_script.py get_capa BATCH123`                                                                                       |
| Get all OOS investigations associated with a batch | `get_oos_investigations`    | `<batch_key>`                                                | `python blockchain_script.py get_oos_investigations BATCH123`                                                                         |
#### Jupyter Notebook
To use the module inside a jupyter notebook you first need to import it

```python
import blockchain_qms
```

Then you can call the respective function as for the standalone version

```python
blockchain_qms.create_batch_record("B4001-074", "2024-09-24", "2026-09-24")
```

| Use Case                                           | Function                            | Arguments                                            | Example                                                                                                                                       |
|----------------------------------------------------|-------------------------------------|------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------|
| Create a new batch record                          | `create_batch_record`               | `batch_key`, `manufacture_date`, `expiration_date`   | `blockchain_qms.create_batch_record("B4001-074", "2024-09-24", "2026-09-24")`                                                                |
| Append a QC test result with external hash         | `append_qc_test`                    | `batch_key`, `test_name`, `test_result`, `test_hash` | `blockchain_qms.append_qc_test("B4001-074", "Sterility Test", "Pass", "abcdef123456...")`                                                    |
| Append a QC test result, generate hash from file   | `append_qc_test_with_file`          | `batch_key`, `test_name`, `test_result`, `file_path` | `blockchain_qms.append_qc_test_with_file("B4001-074", "Sterility Test", "Pass", "/path/to/test_result.txt")`                                 |
| Update the release status of a batch               | `update_release_status`             | `batch_key`, `new_status`                            | `blockchain_qms.update_release_status("B4001-074", "released")`                                                                              |
| Update the expiration date of a batch              | `update_expiration_date`            | `batch_key`, `new_expiration_date`                   | `blockchain_qms.update_expiration_date("B4001-074", "2026-12-31")`                                                                           |
| Retrieve the full batch record in JSON format      | `get_full_batch_record`             | `batch_key`                                          | `batch_record = blockchain_qms.get_full_batch_record("B4001-074")`                                                                           |
| Retrieve the history of a batch                    | `get_batch_history`                 | `batch_key`                                          | `blockchain_qms.get_batch_history("B4001-074")`                                                                                              |
| List all batch numbers stored on the blockchain    | `list_all_batches`                  | None                                                 | `blockchain_qms.list_all_batches()`                                                                                                           |
| Retrieve batches by expiration date                | `get_batches_by_expiration`         | `expiration_input`                                   | `blockchain_qms.get_batches_by_expiration("2026-09")`                                                                                        |
| Get the release status of a batch                  | `get_release_status`                | `batch_key`                                          | `blockchain_qms.get_release_status("B4001-074")`                                                                                             |
| Get the expiration date of a batch                 | `get_expiration_date`               | `batch_key`                                          | `blockchain_qms.get_expiration_date("B4001-074")`                                                                                            |
| Get the manufacture date of a batch                | `get_manufacture_date`              | `batch_key`                                          | `blockchain_qms.get_manufacture_date("B4001-074")`                                                                                           |
| Print the full batch record in human-readable form | `print_human_readable_batch_record` | `batch_record` (JSON object)                         | `batch_record = blockchain_qms.get_full_batch_record("B4001-074")`<br>`blockchain_qms.print_human_readable_batch_record(batch_record)`       |
| Get all QC tests associated with a batch           | `get_qc_tests`                      | `batch_key`                                          | `blockchain_qms.get_qc_tests("B4001-074")`                                                                                                   |
| Append a deviation record to a batch               | `append_deviation`                  | `batch_key`, `deviation_id`                          | `blockchain_qms.append_deviation("B4001-074", "DEV001")`                                                                                     |
| Append a CAPA record to a batch                    | `append_capa`                       | `batch_key`, `capa_id`                               | `blockchain_qms.append_capa("B4001-074", "CAPA001")`                                                                                         |
| Append an OOS investigation to a batch             | `append_oos`                        | `batch_key`, `oos_id`                                | `blockchain_qms.append_oos("B4001-074", "OOS001")`                                                                                           |
| Get all deviations associated with a batch         | `get_deviation`                     | `batch_key`                                          | `blockchain_qms.get_deviation("B4001-074")`                                                                                                  |
| Get all CAPA records associated with a batch       | `get_capa`                          | `batch_key`                                          | `blockchain_qms.get_capa("B4001-074")`                                                                                                       |
| Get all OOS investigations associated with a batch | `get_oos_investigations`            | `batch_key`                                          | `blockchain_qms.get_oos_investigations("B4001-074")`                                                                                         |


### Notes

* Date Formats: Dates should be provided in YYYY-MM-DD format unless specified otherwise.
* Data Integrity: The script uses data fingerprints for integrity verification. The data_fingerprint module provides functions to generate order-dependent and order-independent hashes.
* Error Handling: The script includes basic error handling for missing or incorrect inputs.
Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

### License

MIT License

### Contact

For any questions or support, please open an issue.
