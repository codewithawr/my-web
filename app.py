
from Crypto_price.data_colector import write_crypto_data
from flask import Flask
from flask import render_template_string
from Crypto_price.templates.Crypto_home import index_tm
import os
from flask_apscheduler import APScheduler


app=Flask(__name__,template_folder='templates')


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    if path == 'crypto':
        form = index_tm(cryptos = get_crypto_list())
        return render_template_string(form)
    
    return 'Self Web APP'

# @app.route('/', defaults={'path': ''})
# @app.route('/<path:path>')
# def get_dir(path):
#     data = f'https://raw.githubusercontent.com/codewithawr/Crypto_price/main/crypto/{path}_data.csv'
#     # df = pd.read_csv(data)
#     # csv_data = df.to_csv()
#     return jsonify({'data':data})

if __name__ == '__main__':
    os.chdir(r'C:\Users\PunjabLab3078779971\Desktop\Cripto_API\Crypto_price')
    def get_crypto_list():
        with open('settings\\crypto.txt') as f:
            crypto_options = f.readline().split(',')
        crypto_url = []
        for i in crypto_options:
            crypto_url.append({'name': i, 'url':f'https://raw.githubusercontent.com/codewithawr/Crypto_price/main/crypto/{i}_data.csv'})
        return crypto_url
    def up_crypto():
        with open('settings//crypto.txt') as f:
            CRYPTOS = f.readline().split(',')
        CURRENCY = 'USD'
        for CRYPTO in CRYPTOS:
            suced = write_crypto_data(CRYPTO, CURRENCY)

    scheduler = APScheduler()
    scheduler.add_job(func=up_crypto, trigger='interval', id='job', seconds=43200)
    scheduler.start()
    app.run(debug=False, host="0.0.0.0")

    
