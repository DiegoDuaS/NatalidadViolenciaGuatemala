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
        row = {'Grupo de Edad': grupo, 'Año': ano}
        for nivel, tipo_dict in nivel_dict.items():
            for tipo_caso, total in tipo_dict.items():
                row[f'{tipo_caso} {nivel}'] = total
        resultados.append(row)

# Crear el DataFrame final
resultados_df = pd.DataFrame(resultados)

# Guardar el resultado en un archivo CSV
resultados_df.to_csv('F4.csv', index=False)

print("CSV generado correctamente.")

# ------------------------------------------------------------------------------------------------------------------------------------------------------

# Leer el CSV con los datos de nacimientos
nacimientos_df = pd.read_csv('data/nat/NatEdad.csv')

nacimientos_df.columns = nacimientos_df.columns.str.strip()
nacimientos_df['Edad'] = nacimientos_df['Edad'].astype(str).str.strip()  # Asegurar que 'Edad' sea string
nacimientos_df['Anio'] = nacimientos_df['Anio'].astype(str).str.strip()  # Asegurar que 'Anio' sea string

# Convertir la columna 'Total' a numérico, manejando errores y reemplazando valores NaN con 0
nacimientos_df['Total'] = pd.to_numeric(nacimientos_df['Total'], errors='coerce').fillna(0)

# Definir los grupos de edad
grupos_edad = {
    "14 o menos": ['10', '11', '12', '13', '14'],
    "15-19": ['15', '16', '17', '18', '19'],
    "20-24": ['20', '21', '22', '23', '24'],
    "25-29": ['25', '26', '27', '28', '29'],
    "30-34": ['30', '31', '32', '33', '34'],
    "35-39": ['35', '36', '37', '38', '39'],
    "40-44": ['40', '41', '42', '43', '44'],
    "45-50": ['45', '46', '47', '48', '49', '50'],
    "Más de 50": ['51', '52', '53', '54', '55', '56', '57', '58', '59', '60', '61', '62', '63', '64', '65 y más']
}

# Inicializar diccionario para almacenar los resultados
nacimientos_por_ano = {}

# Iterar sobre el DataFrame
for _, row in nacimientos_df.iterrows():
    edad = row['Edad']
    anio = row['Anio']

    # Omitir la fila 'Todas las edades' y asegurarnos de que 'anio' es un número válido
    if edad == "Todas las edades" or not anio.isdigit():
        continue

    anio = int(anio)  # Convertimos el año a entero

    # Buscar a qué grupo de edad pertenece la fila
    grupo_edad = next((grupo for grupo, edades in grupos_edad.items() if edad in edades), None)
    
    if grupo_edad:
        if anio not in nacimientos_por_ano:
            nacimientos_por_ano[anio] = {grupo: 0 for grupo in grupos_edad.keys()}
        
        # Sumar el total de nacimientos al grupo correspondiente
        nacimientos_por_ano[anio][grupo_edad] += row['Total']

# Convertir los resultados a un DataFrame con el formato deseado
resultados = []
for anio, grupo_dict in nacimientos_por_ano.items():
    for grupo, total in grupo_dict.items():
        resultados.append({'Grupo de Edad': grupo, 'Año': anio, 'Total Nacimientos': total})

# Crear el DataFrame final
resultados_nacimientos_df = pd.DataFrame(resultados)

# Guardar los resultados en un archivo CSV
resultados_nacimientos_df.to_csv('F5.csv', index=False)

print("CSV generado correctamente.")

# ------------------------------------------------------------------------------------------------------------------------------------------------------

estado_civil_df = pd.read_csv('data/nat/NatEdadEC.csv')

# Limpiar nombres de columnas y datos
estado_civil_df.columns = estado_civil_df.columns.str.strip()
estado_civil_df['Grupos de edad'] = estado_civil_df['Grupos de edad'].str.strip()
estado_civil_df['Anio'] = estado_civil_df['Anio'].astype(str).str.strip()

# Convertir las columnas de estado civil a numérico
for col in ['Soltero(a)', 'Casado(a)', 'Unido(a)', 'Ignorado']:
    estado_civil_df[col] = pd.to_numeric(estado_civil_df[col], errors='coerce').fillna(0)

# Definir los grupos de edad estándar
grupos_edad = {
    "14 o menos": ["Menos de 15"],
    "15-19": ["15 - 19"],
    "20-24": ["20 - 24"],
    "25-29": ["25 - 29"],
    "30-34": ["30 - 34"],
    "35-39": ["35 - 39"],
    "40-44": ["40 - 44"],
    "45-50": ["45 - 49"],
    "Más de 50": ["50 y más"]
}

# Diccionario para almacenar los resultados
estado_civil_por_ano = {}

# Iterar sobre el DataFrame
for _, row in estado_civil_df.iterrows():
    grupo = row['Grupos de edad']
    anio = row['Anio']
    progenitor = row['Madre o Padre']  # Identifica si es Madre o Padre

    # Omitir 'Todas las edades' y asegurarnos de que el año es válido
    if grupo == "Todas las edades" or not anio.isdigit():
        continue

    anio = int(anio)  # Convertimos el año a entero

    # Buscar el grupo de edad correspondiente
    grupo_edad = next((g for g, edades in grupos_edad.items() if grupo in edades), None)

    if grupo_edad:
        if anio not in estado_civil_por_ano:
            estado_civil_por_ano[anio] = {g: {'N Soltero Madre': 0, 'N Soltero Padre': 0,
                                              'N Casado Madre': 0, 'N Casado Padre': 0,
                                              'N Unido Madre': 0, 'N Unido Padre': 0,
                                              'N Ignorado Madre': 0, 'N Ignorado Padre': 0}
                                          for g in grupos_edad.keys()}

        # Sumar valores según el progenitor
        if progenitor == "Madre":
            estado_civil_por_ano[anio][grupo_edad]['N Soltero Madre'] += row['Soltero(a)']
            estado_civil_por_ano[anio][grupo_edad]['N Casado Madre'] += row['Casado(a)']
            estado_civil_por_ano[anio][grupo_edad]['N Unido Madre'] += row['Unido(a)']
            estado_civil_por_ano[anio][grupo_edad]['N Ignorado Madre'] += row['Ignorado']
        elif progenitor == "Padre":
            estado_civil_por_ano[anio][grupo_edad]['N Soltero Padre'] += row['Soltero(a)']
            estado_civil_por_ano[anio][grupo_edad]['N Casado Padre'] += row['Casado(a)']
            estado_civil_por_ano[anio][grupo_edad]['N Unido Padre'] += row['Unido(a)']
            estado_civil_por_ano[anio][grupo_edad]['N Ignorado Padre'] += row['Ignorado']

# Convertir resultados a DataFrame
resultados = []
for anio, grupo_dict in estado_civil_por_ano.items():
    for grupo, valores in grupo_dict.items():
        row = { 'Grupo de Edad': grupo,'Año': anio, **valores}
        resultados.append(row)

# Crear DataFrame final
resultados_estado_civil_df = pd.DataFrame(resultados)

# Guardar en un archivo CSV
resultados_estado_civil_df.to_csv('F6.csv', index=False)

print("CSV generado correctamente.")

# ------------------------------------------------------------------------------------------------------------------------------------------------------

# Leer el CSV con los datos de grupos ocupacionales
ocupaciones_df = pd.read_csv('data/nat/NatOcup.csv')

ocupaciones_df.columns = ocupaciones_df.columns.str.strip()
ocupaciones_df['Grupos ocupacionales'] = ocupaciones_df['Grupos ocupacionales'].str.strip()
ocupaciones_df['Anio'] = ocupaciones_df['Anio'].astype(str).str.strip()

# Convertir las columnas de edad a numérico
columnas_edad = ['Menos de 15', '15 - 19', '20 - 24', '25 - 29', '30 - 34', '35 - 39', '40 - 44', '45 - 49', '50 y más']
for col in columnas_edad:
    ocupaciones_df[col] = pd.to_numeric(ocupaciones_df[col], errors='coerce').fillna(0)

# Definir los grupos de edad estándar
grupos_edad = {
    "14 o menos": "Menos de 15",
    "15-19": "15 - 19",
    "20-24": "20 - 24",
    "25-29": "25 - 29",
    "30-34": "30 - 34",
    "35-39": "35 - 39",
    "40-44": "40 - 44",
    "45-50": "45 - 49",
    "Más de 50": "50 y más"
}

# Ocupaciones a excluir
excluir_ocupaciones = {"Ignorado", "Total República", "No especificado en otro grupo", "Todos los grupos ocupacionales"}

# Diccionario para almacenar los resultados
ocupaciones_por_ano = {}

# Iterar sobre el DataFrame
for _, row in ocupaciones_df.iterrows():
    grupo_ocupacional = row['Grupos ocupacionales']
    anio = row['Anio']

    # Omitir las ocupaciones excluidas y asegurarnos de que el año es válido
    if grupo_ocupacional in excluir_ocupaciones or not anio.isdigit():
        continue

    anio = int(anio)  # Convertimos el año a entero

    # Iterar sobre los grupos de edad
    for grupo_edad, columna in grupos_edad.items():
        if anio not in ocupaciones_por_ano:
            ocupaciones_por_ano[anio] = {g: {} for g in grupos_edad.keys()}

        # Agregar la cantidad de nacimientos por grupo ocupacional
        ocupaciones_por_ano[anio][grupo_edad][grupo_ocupacional] = row[columna]

# Convertir resultados a DataFrame
resultados = []
for anio, grupo_dict in ocupaciones_por_ano.items():
    for grupo, ocupaciones in grupo_dict.items():
        row = {'Grupo de Edad': grupo ,'Año': anio, **ocupaciones}
        resultados.append(row)

# Crear DataFrame final
resultados_ocupaciones_df = pd.DataFrame(resultados)

# Guardar en un archivo CSV
resultados_ocupaciones_df.to_csv('F7.csv', index=False)

print("CSV generado correctamente.")

# ------------------------------------------------------------------------------------------------------------------------------------------------------

hijos_df = pd.read_csv('data/nat/NatNum.csv')

# Limpiar nombres de columnas y datos
hijos_df.columns = hijos_df.columns.str.strip()
hijos_df['Edad de la madre'] = hijos_df['Edad de la madre'].astype(str).str.strip()
hijos_df['Anio'] = hijos_df['Anio'].astype(str).str.strip()

# Convertir las columnas numéricas
columnas_hijos = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10 y más']
for col in columnas_hijos:
    hijos_df[col] = pd.to_numeric(hijos_df[col], errors='coerce').fillna(0)

# Definir los grupos de edad
grupos_edad = {
    "14 o menos": ['10', '11', '12', '13', '14'],
    "15-19": ['15', '16', '17', '18', '19'],
    "20-24": ['20', '21', '22', '23', '24'],
    "25-29": ['25', '26', '27', '28', '29'],
    "30-34": ['30', '31', '32', '33', '34'],
    "35-39": ['35', '36', '37', '38', '39'],
    "40-44": ['40', '41', '42', '43', '44'],
    "45-50": ['45', '46', '47', '48', '49', '50'],
    "Más de 50": ['51', '52', '53', '54', '55', '56', '57', '58', '59']
}

# Diccionario para almacenar los resultados
resultados_promedio = []

# Iterar sobre los años
for anio in hijos_df['Anio'].unique():
    for grupo, edades in grupos_edad.items():
        # Filtrar por año y grupo de edad
        df_filtrado = hijos_df[(hijos_df['Anio'] == anio) & (hijos_df['Edad de la madre'].isin(edades))]

        # Calcular el total de madres en el grupo
        total_madres = df_filtrado[columnas_hijos].sum().sum()

        # Calcular el total de hijos en el grupo
        total_hijos = sum(df_filtrado[col] * int(col.split()[0]) for col in columnas_hijos)

        # Calcular el promedio de hijos por madre
        promedio_hijos = total_hijos.sum() / total_madres if total_madres > 0 else 0

        # Agregar resultado
        resultados_promedio.append({'Grupo de Edad': grupo , 'Año': anio,'Promedio de Hijos': round(promedio_hijos, 2)})

# Convertir a DataFrame
resultados_promedio_df = pd.DataFrame(resultados_promedio)

# Guardar en CSV
resultados_promedio_df.to_csv('F8.csv', index=False)

print("CSV generado correctamente.")

# ------------------------------------------------------------------------------------------------------------------------------------------------------

import glob

# Lista de archivos CSV
archivos_csv = ["F1.csv", "F2.csv", "F3.csv", "F4.csv", "F5.csv", "F6.csv", "F7.csv", "F8.csv"]

# Leer el primer archivo para establecer la base de la fusión
df_final = pd.read_csv(archivos_csv[0])

# Fusionar los demás archivos
for archivo in archivos_csv[1:]:
    df_temp = pd.read_csv(archivo)
    df_final = pd.merge(df_final, df_temp, on=['Año', 'Grupo de Edad'], how='outer')

# Guardar el resultado final
df_final.to_csv("DataFinal.csv", index=False)

print("CSV combinado generado correctamente: DataFinal.csv")

