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
