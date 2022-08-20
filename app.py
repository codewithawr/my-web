from Crypto_price.data_colector import write_crypto_data
from flask import Flask
from flask import render_template_string
from Crypto_price.templates.Crypto_home import index_tm
from flask_apscheduler import APScheduler

import os

MYDIR = os.path.dirname(__file__)

settings_path = MYDIR +'/'+'Crypto_price/settings/crypto.txt'


def get_crypto_list():
    with open(settings_path) as f:
        crypto_options = f.readline().split(',')
    crypto_url = []
    for i in crypto_options:
        crypto_url.append({'name': i, 'url':f'https://raw.githubusercontent.com/codewithawr/my-web/main/Crypto_price/crypto/{i}_data.csv'})
    return crypto_url

def upd_crypto():
    print('updating')
    with open(settings_path) as f:
        crypto_options = f.readline().split(',')
    CURRENCY = 'USD'
    for CRYPTO in crypto_options:
        suced = write_crypto_data(CRYPTO, CURRENCY)

scheduler = APScheduler()
scheduler.add_job(func=upd_crypto, trigger='interval', id='job', seconds=43200)
scheduler.start()

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
    app.run()

    
