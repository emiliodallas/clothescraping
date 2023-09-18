import pandas as pd
import numpy as np

def categorize_product(title):
    if 'Camisa' in title or 'Polo' in title:
        return 'Camisa'
    if 'Camiseta' in title:
        return 'Camiseta'
    elif 'Calça' in title:
        return 'Calca'
    elif 'Sapato' in title or 'Tenis' in title:
        return 'Calcados'
    elif 'Bermuda' in title or 'Shorts' in title or 'Regata' in title or 'Sunga' in title or 'Chinelo' in title:
        return 'Verao'
    elif 'Blusa' in title or 'Blusão' in title or 'Moletom' in title or 'Suéter' in title or 'Jaqueta' in title:
        return 'Inverno'
    elif 'Cueca' in title or 'Meia' in title or 'Pijama' in title or 'Samba' in title:
        return 'Intimas'
    else:
        return 'Other'

df = pd.read_csv('dafiti_male_products.csv')

del df['Image URL']

df['Price To'] = df['Price To'].astype(str)
df['Price From'] = df['Price From'].astype(str)

df['Price To'] = df['Price To'].str.extract(r'R\$\s*([\d\.,]+)')
df['Price To'] = df['Price To'].str.replace('.', '')
df['Price To'] = df['Price To'].str.replace(',', '.').astype(float)

df['Price From'] = df['Price From'].str.extract(r'R\$\s*([\d\.,]+)')
df['Price From'] = df['Price From'].str.replace('.', '')
df['Price From'] = df['Price From'].str.replace(',', '.').astype(float)

df['Promo'] = df['Price To'] != df['Price From']

df['Discount'] = round((df['Price To']/df['Price From'])*100, 0)

df['Categoria'] = df['Product Title'].apply(categorize_product)

output_file = 'silver_male_products.csv'
df.to_csv(output_file, index=False)
print('File loaded')
