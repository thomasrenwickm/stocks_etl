#This function is definite. it works well

def transformations(price_data: list):
    #creates columns
    dict_data = price_data[0]
    columns = ['name', 'ticker', 'currency']
    info = dict_data['columns']
    columns.extend(info)
    df = pd.DataFrame(columns=columns)
    
    #Appends the data as rows to the DF
    for i in price_data:
        data = [i['name'], i['ticker'], i['currency']]
        stock_data = i['data'][0]
        data.extend(stock_data)
        df.loc[len(df)] = data

    return df #df here is a local variable

df =transformations(price_data) #here we create the df to be able to save it
df