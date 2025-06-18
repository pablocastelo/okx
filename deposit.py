import okx.Funding as Funding

api_key = "XXXXXXXXXXXXXXXXXXXXXXXXXXX"
secret_key = "XXXXXXXXXXXXXXXXXXXXXXXXXXX"
passphrase = "XXXXXXXXXXXXXXXXXXXXXXXXXXX"

flag = '0'  # '0' for live trading, '1' for paper trading
funding = Funding.FundingAPI(api_key, secret_key, passphrase, False, flag)
## Get available balance

bal = funding.get_balances()
print("Account Balances:")
print("=================================")
for b in bal['data']:
    print(f"Currency: {b['ccy']} | Balance: ${float(b['bal']):.2f} | Available: ${float(b['availBal']):.2f}")
ccy = 'USDT'
usdt_bal = [b for b in bal['data'] if b['ccy'] == ccy][0]

## Make deposits
result = funding.withdrawal(
    ccy=ccy,
    toAddr="pontabraham@gmail.com",
    amt="1",
    dest="3"
)
result
funding.get_deposit_withdraw_status(
    wdId=result['data'][0]['wdId']
)
