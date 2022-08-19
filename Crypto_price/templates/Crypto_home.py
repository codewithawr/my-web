
def index_tm(cryptos):
    cryptos_div = ''
    for crypto in cryptos:
        crypto= dict(crypto)
        cryptos_div = cryptos_div + f'''
<div>
    <div><p id = 'name'>{crypto.get("name")}</p> <p id = "price{crypto.get('name')}">--</p></div>
    <div id= "{crypto.get('name')}"></div>
</div>

<py-script>

# importing
from time import sleep
# using pyodide for requsting. Only wey workes in PyScript
from pyodide.http import pyfetch
import asyncio
# defining key/request url
key = f"https://api.binance.com/api/v3/ticker/price?symbol={crypto.get('name')}USDT"

while True:
    # requesting data from url using pyfetch
    data = await pyfetch(url=key, method="GET")
    data = await data.json()
    sleep(2)
    pyscript.write('price{crypto.get('name')}',  data['symbol']+'/'+ data['price'])

</py-script>

<py-script output="{crypto.get('name')}">

    from pyodide.http import pyfetch,open_url
    import altair as alt
    from js import console
    import pandas
    import asyncio


    data = open_url("{crypto.get('url')}")

    crypto_data = pandas.read_csv(data)
    open_close_color = alt.condition("datum.Open <= datum.Close",alt.value("#06982d"),alt.value("#ae1325"))

    base = alt.Chart(crypto_data).encode(alt.X('Date:T',axis=alt.Axis(format='%d-%m-%y',labelAngle=-45,title='Date in 2009' )),color=open_close_color)
    
    rul = base.mark_bar().encode(alt.Y('Open:Q'),alt.Y2('Close:Q'))
    
    br = base.mark_rule().encode(alt.Y('Low:Q',title='Price'),alt.Y2('High:Q'))
    
    bre = rul + br
    bre = bre.properties(width=700,height=400).interactive()
    bre
</py-script>


'''
    main = f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <link rel="stylesheet" href="https://pyscript.net/alpha/pyscript.css" />
    <script defer src="https://pyscript.net/alpha/pyscript.js"></script>

    <title>Document</title>
</head>
<body>
    <py-env>
    - pandas
    - altair
    </py-env>
''' + cryptos_div +'''
</body>
</html>
'''
    return str(main)