import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar el archivo CSV
file_path = r'C:\Users\bandy\Documents\Datos Masivos\Entregables\T6\BreadBasket_DMS.csv'
bread_basket_data = pd.read_csv(file_path)

# Eliminar las transacciones donde el item es "NONE"
bread_basket_data = bread_basket_data[bread_basket_data['Item'] != 'NONE']

# Inicialización del diccionario
basket_items = {}

# Contar la frecuencia de cada item
for item in bread_basket_data['Item']:
    if item in basket_items:
        basket_items[item] += 1
    else:
        basket_items[item] = 1

# Crear un DataFrame para los ítems y sus frecuencias
items_table = pd.DataFrame({'Names': list(basket_items.keys()),
                            'Frequencies': list(basket_items.values())})

# Graficar las frecuencias
items_table.sort_values('Frequencies', ascending=False).head(20).\
    plot.bar(y='Frequencies', x='Names', figsize=(12, 8))
plt.show()

# Preparación de datos para reglas de asociación
bread_basket_data = bread_basket_data.groupby('Transaction').agg(','.join).reset_index()
bread_basket_data = bread_basket_data.drop(['Date', 'Time'], axis=1)

# Convertir las transacciones a listas
items_list = [item.split(',') for item in bread_basket_data['Item']]

# Codificar los ítems
from mlxtend.preprocessing import TransactionEncoder
transencoder = TransactionEncoder()
transencoder_array = transencoder.fit(items_list).transform(items_list)
encoded_df = pd.DataFrame(transencoder_array, columns=transencoder.columns_)

# Aplicar el algoritmo apriori
item_support_df = apriori(encoded_df, min_support=0.01, use_colnames=True)

# Generar reglas de asociación
rules = association_rules(item_support_df, metric='confidence', min_threshold=0.1)

# Mostrar algunas reglas
print(rules.sample(10))

# Reglas más confiables
print(rules.sort_values('confidence', ascending=False).head(10))

# Filtrar por un antecedente específico
print(rules[rules['antecedents'] == {'Juice'}])