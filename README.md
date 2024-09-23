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
- **Environment Variables**: A `.env` file containing the following variables:
  - `RPC_USER`
  - `RPC_PASSWORD`
  - `RPC_HOST`
  - `RPC_PORT`

### Clone the Repository

```bash
git clone https://github.com/yourusername/blockchain_batch_management.git
cd blockchain_batch_management
```
### Install Dependencies
Install the required Python packages:
```bash
pip install -r requirements.txt
```

Note: The data_fingerprint module is available at https://github.com/chriswilson2020/data_fingerprint/. 
Install it using:
```bash
pip install git+https://github.com/chriswilson2020/data_fingerprint.git
```

#### Setup Environment Variables
Create a .env file in the project root directory with the following content (an example is included for you to edit also):
```makefile
RPC_USER=your_rpc_username
RPC_PASSWORD=your_rpc_password
RPC_HOST=localhost
RPC_PORT=your_rpc_port
```

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
