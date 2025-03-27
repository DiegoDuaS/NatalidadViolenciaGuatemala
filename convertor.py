import pandas as pd

# Leer el CSV de VifAlfa
vif_df = pd.read_csv('data/vif/VifAlfa.csv')

# Limpiar posibles espacios en blanco y corregir nombres de las columnas
vif_df.columns = vif_df.columns.str.strip()  # Eliminar espacios en blanco en las columnas
vif_df['Grupos de edad'] = vif_df['Grupos de edad'].str.strip()  # Eliminar espacios en blanco en los grupos de edad

# Convertir la columna 'Total' a numérico, manejando los errores (como cadenas vacías o no numéricas)
vif_df['Total'] = pd.to_numeric(vif_df['Total'], errors='coerce')

# Filtrar los datos para eliminar "Total" y "Ignorado"
vif_df = vif_df[vif_df['Grupos de edad'] != 'Total']
vif_df = vif_df[vif_df['Grupos de edad'] != 'Ignorado']

# Inicializar el diccionario de grupos de edad por año
grupos_edad = ["14 o menos", "15-19", "20-24", "25-29", "30-34", "35-39", "40-44", "45-50", "Más de 50"]
anos = range(9, 22)  # Años de 09 a 21

grupos_edad_por_ano = {ano: {grupo: {'Total VI Victima': 0, 'Total VI Agresor': 0} for grupo in grupos_edad} for ano in anos}

# Función para agregar los totales a la estructura
def agregar_total(grupo_edad, anio, victima_o_agresor, total):
    if victima_o_agresor == 'V':
        grupos_edad_por_ano[anio][grupo_edad]['Total VI Victima'] += total
    else:
        grupos_edad_por_ano[anio][grupo_edad]['Total VI Agresor'] += total

# Iterar sobre el DataFrame para sumar los totales por grupo de edad y año
for _, row in vif_df.iterrows():
    if row['Grupos de edad'] in ['7 años', '8 años', '9 años', '10 años', '11 años', '12 años', '13 años', '14 años']:
        agregar_total("14 o menos", row['Anio'], row['Victima o Agresor'], row['Total'])
    elif row['Grupos de edad'] == '15 a 19':
        agregar_total("15-19", row['Anio'], row['Victima o Agresor'], row['Total'])
    elif row['Grupos de edad'] == '20 a 24':
        agregar_total("20-24", row['Anio'], row['Victima o Agresor'], row['Total'])
    elif row['Grupos de edad'] == '25 a 29':
        agregar_total("25-29", row['Anio'], row['Victima o Agresor'], row['Total'])
    elif row['Grupos de edad'] == '30 a 34':
        agregar_total("30-34", row['Anio'], row['Victima o Agresor'], row['Total'])
    elif row['Grupos de edad'] == '35 a 39':
        agregar_total("35-39", row['Anio'], row['Victima o Agresor'], row['Total'])
    elif row['Grupos de edad'] == '40 a 44':
        agregar_total("40-44", row['Anio'], row['Victima o Agresor'], row['Total'])
    elif row['Grupos de edad'] == '45 a 49':
        agregar_total("45-50", row['Anio'], row['Victima o Agresor'], row['Total'])
    elif row['Grupos de edad'] == '50 a 54':
        agregar_total("Más de 50", row['Anio'], row['Victima o Agresor'], row['Total'])
    elif row['Grupos de edad'] == '55 a 59':
        agregar_total("Más de 50", row['Anio'], row['Victima o Agresor'], row['Total'])
    elif row['Grupos de edad'] == '60 a 64':
        agregar_total("Más de 50", row['Anio'], row['Victima o Agresor'], row['Total'])
    elif row['Grupos de edad'] == '65 y más':
        agregar_total("Más de 50", row['Anio'], row['Victima o Agresor'], row['Total'])

# Convertir los resultados a un DataFrame
resultados = []
for ano, grupo_dict in grupos_edad_por_ano.items():
    for grupo, tipo_dict in grupo_dict.items():
        resultados.append([grupo, ano, tipo_dict['Total VI Victima'], tipo_dict['Total VI Agresor']])

# Crear el DataFrame final
resultados_df = pd.DataFrame(resultados, columns=['Grupo de Edad', 'Año', 'Total VI Victima', 'Total VI Agresor'])

# Guardar el resultado en un archivo CSV
resultados_df.to_csv('F1.csv', index=False)

print("CSV generado correctamente.")

# -----------------------------------------------------------------------------------------------------------------------------

# Leer el nuevo CSV con los grupos quinquenales de edad
quinquenales_df = pd.read_csv('data/vif/VifAreaSexoEdad.csv')

# Limpiar posibles espacios en blanco y corregir nombres de las columnas
quinquenales_df.columns = quinquenales_df.columns.str.strip()  # Eliminar espacios en blanco en las columnas
quinquenales_df['Grupos quinquenales de edad'] = quinquenales_df['Grupos quinquenales de edad'].str.strip()  # Eliminar espacios en blanco en los grupos de edad

# Convertir las columnas de total a numérico, manejando errores (por ejemplo, convertir vacíos o no numéricos a NaN)
quinquenales_df['TotalH'] = pd.to_numeric(quinquenales_df['TotalH'], errors='coerce')
quinquenales_df['TotalM'] = pd.to_numeric(quinquenales_df['TotalM'], errors='coerce')
quinquenales_df['Urban'] = pd.to_numeric(quinquenales_df['Urban'], errors='coerce')
quinquenales_df['Rural'] = pd.to_numeric(quinquenales_df['Rural'], errors='coerce')

# Inicializar el diccionario de grupos de edad por año
grupos_edad = ["14 o menos", "15-19", "20-24", "25-29", "30-34", "35-39", "40-44", "45-50", "Más de 50"]
anos = range(9, 22)  # Años de 09 a 21

# Inicializar el diccionario con valores por año y grupo de edad para victimas y agresores por género
grupos_edad_por_ano = {ano: {grupo: {'VI Victima Hombre': 0, 'VI Victima Mujer': 0, 'VI Agresor Hombre': 0, 'VI Agresor Mujer': 0,
                                     'VI Urbano': 0, 'VI Rural': 0} for grupo in grupos_edad} for ano in anos}

# Iterar sobre el DataFrame quinquenales_df para agregar los datos por género, tipo y contexto geográfico
for _, row in quinquenales_df.iterrows():
    # Asignar valores a los grupos de edad
    if row['Grupos quinquenales de edad'] in ['0 a 4', '5 a 9', '10 a 14']:
        grupo = "14 o menos"
    elif row['Grupos quinquenales de edad'] == '15 a 19':
        grupo = "15-19"
    elif row['Grupos quinquenales de edad'] == '20 a 24':
        grupo = "20-24"
    elif row['Grupos quinquenales de edad'] == '25 a 29':
        grupo = "25-29"
    elif row['Grupos quinquenales de edad'] == '30 a 34':
        grupo = "30-34"
    elif row['Grupos quinquenales de edad'] == '35 a 39':
        grupo = "35-39"
    elif row['Grupos quinquenales de edad'] == '40 a 44':
        grupo = "40-44"
    elif row['Grupos quinquenales de edad'] == '45 a 49':
        grupo = "45-50"
    elif row['Grupos quinquenales de edad'] in ['50 a 54', '55 a 59', '60 a 64', '65 y más']:
        grupo = "Más de 50"
    
    # Sumar los casos de violencia por género (Hombre/Mujer) y tipo (Victima/Agresor)
    if row['Victima o Agresor'] == 'V':  # Si es víctima
        if pd.notna(row['TotalH']) and row['TotalH'] > 0:
            grupos_edad_por_ano[row['Anio']][grupo]['VI Victima Hombre'] += row['TotalH']
        if pd.notna(row['TotalM']) and row['TotalM'] > 0:
            grupos_edad_por_ano[row['Anio']][grupo]['VI Victima Mujer'] += row['TotalM']
    elif row['Victima o Agresor'] == 'A':  # Si es agresor
        if pd.notna(row['TotalH']) and row['TotalH'] > 0:
            grupos_edad_por_ano[row['Anio']][grupo]['VI Agresor Hombre'] += row['TotalH']
        if pd.notna(row['TotalM']) and row['TotalM'] > 0:
            grupos_edad_por_ano[row['Anio']][grupo]['VI Agresor Mujer'] += row['TotalM']
    
    # Sumar los casos por contexto geográfico (Urbano y Rural)
    if pd.notna(row['Urban']) and row['Urban'] > 0:
        grupos_edad_por_ano[row['Anio']][grupo]['VI Urbano'] += row['Urban']
    
    if pd.notna(row['Rural']) and row['Rural'] > 0:
        grupos_edad_por_ano[row['Anio']][grupo]['VI Rural'] += row['Rural']

# Convertir los resultados a un DataFrame
resultados = []
for ano, grupo_dict in grupos_edad_por_ano.items():
    for grupo, tipo_dict in grupo_dict.items():
        resultados.append([grupo, ano, tipo_dict['VI Victima Hombre'], tipo_dict['VI Victima Mujer'], tipo_dict['VI Agresor Hombre'], tipo_dict['VI Agresor Mujer'],
                           tipo_dict['VI Urbano'], tipo_dict['VI Rural']])

# Crear el DataFrame final
resultados_df = pd.DataFrame(resultados, columns=['Grupo de Edad', 'Año', 'VI Victima Hombre', 'VI Victima Mujer', 'VI Agresor Hombre', 'VI Agresor Mujer',
                                                  'VI Urbano', 'VI Rural'])

# Guardar el resultado en un archivo CSV
resultados_df.to_csv('F2.csv', index=False)

print("CSV generado correctamente.")

# ------------------------------------------------------------------------------------------------------------------------------------------------------

# Leer el nuevo CSV
nuevo_csv_df = pd.read_csv('data/vif/VifEscolaridad.csv')

# Limpiar posibles espacios en blanco y corregir nombres de las columnas
nuevo_csv_df.columns = nuevo_csv_df.columns.str.strip()  # Eliminar espacios en blanco en las columnas
nuevo_csv_df['Grupo de edades'] = nuevo_csv_df['Grupo de edades'].str.strip()  # Eliminar espacios en blanco en los grupos de edad

# Convertir las columnas de Total a numérico, manejando errores (vacíos o no numéricos convertidos a NaN)
nuevo_csv_df['Total'] = pd.to_numeric(nuevo_csv_df['Total'], errors='coerce')
nuevo_csv_df['Ninguno'] = pd.to_numeric(nuevo_csv_df['Ninguno'], errors='coerce')
nuevo_csv_df['Primaria'] = pd.to_numeric(nuevo_csv_df['Primaria'], errors='coerce')
nuevo_csv_df['Básico'] = pd.to_numeric(nuevo_csv_df['Básico'], errors='coerce')
nuevo_csv_df['Diversificado'] = pd.to_numeric(nuevo_csv_df['Diversificado'], errors='coerce')
nuevo_csv_df['Universitario'] = pd.to_numeric(nuevo_csv_df['Universitario'], errors='coerce')

# Grupos de edad y años ya definidos
grupos_edad = ["14 o menos", "15-19", "20-24", "25-29", "30-34", "35-39", "40-44", "45-50", "Más de 50"]
anos = range(9, 22)  # Años de 09 a 21

# Inicializar el diccionario con valores por año, grupo de edad, nivel educativo, y tipo (victima/agresor)
grupos_edad_por_ano = {ano: {grupo: {nivel: {'VI Victima': 0, 'VI Agresor': 0} for nivel in ['Ninguno', 'Primaria', 'Básico', 'Diversificado', 'Universitario']} 
                                      for grupo in grupos_edad} for ano in anos}

# Iterar sobre el DataFrame para agregar los datos por nivel educativo, tipo de caso y grupo de edad
for _, row in nuevo_csv_df.iterrows():
    # Asignar valores a los grupos de edad
    if row['Grupo de edades'] in ['7 años', '8 años', '9 años', '10 años', '11 años', '12 años', '13 años', '14 años']:
        grupo_edad = "14 o menos"
    elif row['Grupo de edades'] == '15 a 19':
        grupo_edad = "15-19"
    elif row['Grupo de edades'] == '20 a 24':
        grupo_edad = "20-24"
    elif row['Grupo de edades'] == '25 a 29':
        grupo_edad = "25-29"
    elif row['Grupo de edades'] == '30 a 34':
        grupo_edad = "30-34"
    elif row['Grupo de edades'] == '35 a 39':
        grupo_edad = "35-39"
    elif row['Grupo de edades'] == '40 a 44':
        grupo_edad = "40-44"
    elif row['Grupo de edades'] == '45 a 49':
        grupo_edad = "45-50"
    elif row['Grupo de edades'] == '50 a 54':
        grupo_edad = "Más de 50"
    elif row['Grupo de edades'] == '55 a 59':
        grupo_edad = "Más de 50"
    elif row['Grupo de edades'] == '60 a 64':
        grupo_edad = "Más de 50"
    elif row['Grupo de edades'] == '65 y más':
        grupo_edad = "Más de 50"
    else:
        continue  # Si no es un grupo de edad válido, se salta esa fila

    # Asignar el tipo de caso (víctima o agresor)
    if row['Victima o Agresor'] == 'V':  # Si es víctima
        tipo_caso = 'VI Victima'
    elif row['Victima o Agresor'] == 'A':  # Si es agresor
        tipo_caso = 'VI Agresor'
    else:
        continue  # Si no es ni víctima ni agresor, salta esa fila

    # Para cada nivel de escolaridad, sumar los casos
    for nivel in ['Ninguno', 'Primaria', 'Básico', 'Diversificado', 'Universitario']:
        if pd.notna(row[nivel]) and row[nivel] > 0:  # Si hay datos válidos para el nivel de escolaridad
            # Sumar los casos por tipo de caso y nivel educativo
            grupos_edad_por_ano[row['Anio']][grupo_edad][nivel][tipo_caso] += row[nivel]

# Convertir los resultados a un DataFrame
resultados = []
for ano, grupo_dict in grupos_edad_por_ano.items():
    for grupo, nivel_dict in grupo_dict.items():
        row = {'Grupo de Edad': grupo, 'Año': ano}
        for nivel, tipo_dict in nivel_dict.items():
            for tipo_caso, total in tipo_dict.items():
                row[f'{tipo_caso} {nivel}'] = total
        resultados.append(row)

# Crear el DataFrame final
resultados_df = pd.DataFrame(resultados)

# Guardar el resultado en un archivo CSV
resultados_df.to_csv('F3.csv', index=False)

print("CSV generado correctamente.")

# ------------------------------------------------------------------------------------------------------------------------------------------------------

alfabetismo_df = pd.read_csv('data/vif/VifAlfa.csv')

alfabetismo_df.columns = alfabetismo_df.columns.str.strip()  # Eliminar espacios en blanco en las columnas
alfabetismo_df['Grupos de edad'] = alfabetismo_df['Grupos de edad'].str.strip()  # Eliminar espacios en blanco en los grupos de edad

# Convertir las columnas de Total, Alfabeta y Analfabeta a numérico, manejando errores
alfabetismo_df['Total'] = pd.to_numeric(alfabetismo_df['Total'], errors='coerce')
alfabetismo_df['Alfabeta'] = pd.to_numeric(alfabetismo_df['Alfabeta'], errors='coerce')
alfabetismo_df['Analfabeta'] = pd.to_numeric(alfabetismo_df['Analfabeta'], errors='coerce')

# Grupos de edad y años ya definidos
grupos_edad = ["14 o menos", "15-19", "20-24", "25-29", "30-34", "35-39", "40-44", "45-50", "Más de 50"]
anos = range(9, 22)  # Años de 09 a 21

# Inicializar el diccionario con valores por año, grupo de edad, nivel de alfabetismo y tipo (victima/agresor)
grupos_edad_por_ano = {ano: {grupo: {nivel: {'VI Victima': 0, 'VI Agresor': 0} for nivel in ['Alfabeta', 'Analfabeta']} 
                                      for grupo in grupos_edad} for ano in anos}

# Iterar sobre el DataFrame para agregar los datos por nivel de alfabetismo, tipo de caso y grupo de edad
for _, row in alfabetismo_df.iterrows():
    # Asignar valores a los grupos de edad
    if row['Grupos de edad'] in ['7 años', '8 años', '9 años', '10 años', '11 años', '12 años', '13 años', '14 años']:
        grupo_edad = "14 o menos"
    elif row['Grupos de edad'] == '15 a 19':
        grupo_edad = "15-19"
    elif row['Grupos de edad'] == '20 a 24':
        grupo_edad = "20-24"
    elif row['Grupos de edad'] == '25 a 29':
        grupo_edad = "25-29"
    elif row['Grupos de edad'] == '30 a 34':
        grupo_edad = "30-34"
    elif row['Grupos de edad'] == '35 a 39':
        grupo_edad = "35-39"
    elif row['Grupos de edad'] == '40 a 44':
        grupo_edad = "40-44"
    elif row['Grupos de edad'] == '45 a 49':
        grupo_edad = "45-50"
    elif row['Grupos de edad'] == '50 a 54':
        grupo_edad = "Más de 50"
    elif row['Grupos de edad'] == '55 a 59':
        grupo_edad = "Más de 50"
    elif row['Grupos de edad'] == '60 a 64':
        grupo_edad = "Más de 50"
    elif row['Grupos de edad'] == '65 y más':
        grupo_edad = "Más de 50"
    else:
        continue  # Si no es un grupo de edad válido, se salta esa fila

    # Asignar el tipo de caso (víctima o agresor)
    if row['Victima o Agresor'] == 'V':  # Si es víctima
        tipo_caso = 'VI Victima'
    elif row['Victima o Agresor'] == 'A':  # Si es agresor
        tipo_caso = 'VI Agresor'
    else:
        continue  # Si no es ni víctima ni agresor, salta esa fila

    # Para cada nivel de alfabetismo, sumar los casos
    for nivel in ['Alfabeta', 'Analfabeta']:
        if pd.notna(row[nivel]) and row[nivel] > 0:  # Si hay datos válidos para el nivel de alfabetismo
            # Sumar los casos por tipo de caso y nivel de alfabetismo
            grupos_edad_por_ano[row['Anio']][grupo_edad][nivel][tipo_caso] += row[nivel]

# Convertir los resultados a un DataFrame
resultados = []
for ano, grupo_dict in grupos_edad_por_ano.items():
    for grupo, nivel_dict in grupo_dict.items():
        row = {'Grupos de Edad': grupo, 'Año': ano}
        for nivel, tipo_dict in nivel_dict.items():
            for tipo_caso, total in tipo_dict.items():
                row[f'{tipo_caso} {nivel}'] = total
        resultados.append(row)

# Crear el DataFrame final
resultados_df = pd.DataFrame(resultados)

# Guardar el resultado en un archivo CSV
resultados_df.to_csv('F4.csv', index=False)

print("CSV generado correctamente.")