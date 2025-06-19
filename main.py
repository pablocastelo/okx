import click
from dotenv import load_dotenv
import os
import csv
from datetime import datetime
import time

load_dotenv()
api_key = os.getenv("API_KEY")
secret_key = os.getenv("SECRET_KEY")
passphrase = os.getenv("PASSPHRASE")

import okx.Funding as Funding

flag = '0'  # '0' for live trading, '1' for paper trading
funding = Funding.FundingAPI(api_key, secret_key, passphrase, False, flag)
default_ccy = 'USDT'
valid_currencies = ['USDT']
expected_columns = ['email', 'amount']
output_headers = ['wdId', 'timestamp', 'email', 'amount', 'code']

withdrawal_rate_limit = 6 # per second

@click.command()
@click.option('-f', '--file', help='path to the file to upload', prompt='payment csv file')
@click.option('-c', '--currency', help='currency to use', default=default_ccy, type=click.Choice(valid_currencies))
def main(file, currency):
    now = datetime.now()
    bal = funding.get_balances()

    # msg should be empty if auth was successful
    msg = bal.get('msg', '')
    if msg == '':
        click.echo('Authenticated')
    else:
        click.echo(f'Authentication failed: {msg}')
        # exit with error code
        exit(1)
        
    click.echo("=================================")
    click.echo(f"Using currency: {currency}")
    currency_bals = [b for b in bal['data'] if b['ccy'] == currency]
    if not currency_bals:
        click.echo(f"Currency {currency} not found")
        click.echo("Account Balances:")
        click.echo("=================================")
        for b in bal['data']:
            click.echo(f"Currency: {b['ccy']} | Balance: ${float(b['bal']):.2f} | Available: ${float(b['availBal']):.2f}")
        exit(1)
    elif len(currency_bals) > 1:
        click.echo(f"Multiple currencies found: {currency_bals}")
        exit(1)
        
    currency_bal = currency_bals[0]
    click.echo(f"Currency: {currency} | Balance: ${float(currency_bal['bal']):.2f} | Available: ${float(currency_bal['availBal']):.2f}")
    click.echo("=================================")

    available_balance = float(currency_bal['availBal'])
    
    # read the file
    rows_to_process = 0
    total_to_disburse = 0
    payment_data = []
    with open(file, 'r') as file:
        reader = csv.reader(file)
        for i, row in enumerate(reader):
            if i == 0:
                # find the columns for amount, network and address
                email_col = row.index('email')
                amount_col = row.index('amount')
                continue
            rows_to_process += 1
            total_to_disburse += float(row[amount_col])
            
            row_dict = {
                'amount': float(row[amount_col]),
                'email': row[email_col],
            }
            payment_data.append(row_dict)
            
    click.echo(f"Total to disburse: {total_to_disburse}")
    
    if total_to_disburse > available_balance:
        click.echo("Not enough balance to disburse all payments")
        exit(1)
    
    confirm = click.confirm("Do you want to proceed?", default=False)
    if not confirm:
        click.echo("Aborted")
        exit(1)
        
    click.echo("Processing payments...")
    output_file_name = f"processed/{now:%Y-%m-%d_%H-%M-%S}_output.csv"
    
    with open(output_file_name, 'w') as output_file:
        writer = csv.writer(output_file)
        writer.writerow(output_headers)
        
        with click.progressbar(payment_data, length=len(payment_data)) as bar:
            for row in bar:
                amount = row['amount']
                email = row['email']
                
                res = funding.withdrawal(
                    ccy=currency,
                    toAddr=email,
                    amt=amount,
                    dest="3"
                )
                code = res['code']
                if code == '0':
                    tx_id = res['data'][0]['wdId']
                else:
                    tx_id = res['msg']
                timestamp = f"{datetime.now():%Y-%m-%d %H:%M:%S}"
                
                writer.writerow([tx_id, timestamp, email, amount, code])
                time.sleep(1 / withdrawal_rate_limit)
        
    click.echo(f"Payments processed successfully. Output file: {output_file_name}. Waiting for confirmations...")
    
if __name__ == "__main__":
    main()
