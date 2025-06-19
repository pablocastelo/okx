# OKX Payment Disbursement Tool

A command-line tool for automating bulk payments through the OKX exchange API. This tool reads payment data from a CSV file and processes withdrawals to email addresses.

## Features

- **Bulk Payment Processing**: Process multiple payments from a CSV file
- **Balance Validation**: Automatically checks available balance before processing
- **Rate Limiting**: Built-in rate limiting to comply with API restrictions
- **Progress Tracking**: Visual progress bar during payment processing
- **Output Logging**: Generates detailed CSV output with transaction IDs and timestamps
- **Multiple Currency Support**: Supports USDT and MXN currencies

## Prerequisites

- Python 3.7+
- OKX API credentials (API Key, Secret Key, and Passphrase)
- UV package manager

## Installation

1. Clone or download this repository
2. Install dependencies using UV:

```bash
uv sync
```

## Configuration

Create a `.env` file in the project root with your OKX API credentials:

```env
API_KEY=your_api_key_here
SECRET_KEY=your_secret_key_here
PASSPHRASE=your_passphrase_here
```

**Important**: 
- Use paper trading mode for testing (set `flag = '1'` in main.py)
- Use live trading mode only when ready for production (set `flag = '0'` in main.py)

## Input CSV Format

Create a CSV file with the following columns:

| Column | Description | Required |
|--------|-------------|----------|
| `email` | Recipient email address | Yes |
| `amount` | Payment amount | Yes |

Example:
```csv
email,amount
user1@example.com,100.50
user2@example.com,75.25
user3@example.com,200.00
```

## Usage

### Basic Usage

```bash
uv run main.py
```

The tool will prompt you for:
1. Path to your payment CSV file
2. Currency to use (USDT or MXN)

### Advanced Usage

```bash
uv run main.py -f payments.csv -c USDT
```

### Command Line Options

- `-f, --file`: Path to the payment CSV file
- `-c, --currency`: Currency to use (Only USDT is supported, default: USDT)

## How It Works

1. **Authentication**: Validates your OKX API credentials
2. **Balance Check**: Verifies sufficient balance for all payments
3. **Payment Processing**: Processes each payment with rate limiting (6 per second)
4. **Output Generation**: Creates a timestamped CSV file with transaction details

## Output

The tool generates a CSV file in the `processed/` directory with the following columns:

- `wdId`: Withdrawal transaction ID
- `timestamp`: Processing timestamp
- `email`: Recipient email
- `amount`: Payment amount
- `code`: API response code

## Safety Features

- **Balance Validation**: Prevents processing if insufficient funds
- **Confirmation Prompt**: Requires user confirmation before processing
- **Rate Limiting**: Respects API rate limits (6 requests per second)
- **Error Handling**: Graceful handling of API errors

## Troubleshooting

### Authentication Failed
- Verify your API credentials in the `.env` file
- Ensure your API keys have withdrawal permissions
- Check if you're using the correct trading mode (paper/live)

### Insufficient Balance
- Check your available balance for the selected currency
- Ensure the total payment amount doesn't exceed available funds

### Currency Not Found
- Verify the currency is supported (USDT, MXN)
- Check if you have a balance in the selected currency

## Security Notes

- Never commit your `.env` file to version control
- Use paper trading mode for testing
- Review all payments before confirming
- Keep your API credentials secure

## API Documentation

This tool uses the OKX Funding API. For more information, visit the [OKX API Documentation](https://www.okx.com/docs-v5/).

## License

This project is for educational and personal use. Please ensure compliance with OKX's terms of service and applicable regulations.
