import pandas as pd

def area_sexo_edad_v(sheet, y, dest):
    if "Regresar" in sheet.columns:
        sheet.pop("Regresar")
    values = [
        "Total", "TotalH", "TotalM", 
        "Urban", "UrbanH", "UrbanM", 
        "Rural", "RuralH", "RuralM", 
        "Ignorado", "IgnoradoH", "IgnoradoM"
    ]
    sheet.iloc[3, 1:len(values) + 1] = values
    cols = list(sheet.iloc[3])
    sheet.columns = cols
    sheet = sheet[6:].reset_index(drop=True) 
    if len(sheet.columns)>13:
        sheet = sheet.iloc[:, :-2] 
    sheet["Victima o Agresor"] = "V"
    sheet["Anio"] = y
    return pd.concat([dest, sheet], ignore_index=True)

def area_sexo_edad_a(sheet, y, dest):
    if "Regresar" in sheet.columns:
        sheet.pop("Regresar")
    sheet.iloc[4,0] = "Grupos quinquenales de edad"
    values = [
        "Total", "TotalH", "TotalM", 
        "Urban", "UrbanH", "UrbanM", 
        "Rural", "RuralH", "RuralM", 
        "Ignorado", "IgnoradoH", "IgnoradoM"
    ]
    sheet.iloc[4, 1:len(values) + 1] = values
    cols = list(sheet.iloc[4])
    sheet.columns = cols
    sheet = sheet[7:].reset_index(drop=True)
    sheet["Victima o Agresor"] = "A"
    sheet["Anio"] = y
    sheet = sheet.iloc[:-1]
    return pd.concat([dest, sheet], ignore_index=True)
    
def psr(sheet, y, dest):
    if "Regresar" in sheet.columns:
        sheet.pop("Regresar")
    cols = list(sheet.iloc[4])
    cols[0] = "Relacion"
    sheet.columns = cols
    sheet = sheet[5:].reset_index(drop=True) 
    sheet.loc[12:21, "Sexo"] = "H"
    sheet.loc[23:,"Sexo"] = "M"
    sheet = sheet.iloc[12:]
    sheet = sheet.drop(22)
    sheet = sheet.iloc[:-1]
    
    sheet.loc[sheet["Relacion"].str.startswith("Hijastr", na=False), "Relacion"] = "Hijastros(as)"
    sheet.loc[sheet["Relacion"].str.startswith("Espos", na=False), "Relacion"] = "Esposos(as)"
    sheet.loc[sheet["Relacion"].str.startswith("Herman", na=False), "Relacion"] = "Hermanos(as)"
    sheet.loc[sheet["Relacion"].str.startswith("Ex", na=False), "Relacion"] = "Ex cónyuges"
    sheet.loc[sheet["Relacion"].str.startswith("Otro", na=False), "Relacion"] = "Otro"
    sheet.loc[sheet["Relacion"].str.startswith("Niet", na=False), "Relacion"] = "Nietos(as)"
    sheet.loc[sheet["Relacion"].str.startswith("Conviv", na=False), "Relacion"] = "Convivientes"
    sheet.loc[sheet["Relacion"].str.startswith("Sueg", na=False), "Relacion"] = "Suegros(as)"
    sheet.loc[sheet["Relacion"].str.startswith("Pad", na=False), "Relacion"] = "Padres/Madres"
    sheet.loc[sheet["Relacion"].str.startswith("Mad", na=False), "Relacion"] = "Padres/Madres"
    sheet.loc[
        (sheet["Relacion"].str.startswith("Hij", na=False)) & (sheet["Relacion"] != "Hijastros(as)"), 
        "Relacion"
    ] = "Hijos(as)"
    sheet["Anio"] = y
    return pd.concat([dest, sheet], ignore_index=True)

def escolaridad(sheet, y, is_victim, dest):
    if "Regresar" in sheet.columns:
        sheet.pop("Regresar")
    cols = list(sheet.iloc[4])
    cols[0] = "Grupo de edades"
    sheet.columns = cols
    sheet = sheet[5:].reset_index(drop=True) 
    men_id = sheet[sheet["Grupo de edades"] == "Hombres"].index.tolist()[0]
    women_id = sheet[sheet["Grupo de edades"] == "Mujeres"].index.tolist()[0]
    sheet.loc[men_id+1:women_id-1, "Sexo"] = "H"
    sheet.loc[women_id+1:, "Sexo"] = "M"
    sheet = sheet.drop(women_id)
    sheet = sheet.iloc[men_id+1:].reset_index(drop=True) 
    if is_victim:
        sheet["Victima o Agresor"] = "V"
    else: 
        sheet = sheet.iloc[:-1]
        sheet["Victima o Agresor"] = "A"
    sheet["Anio"] = y
    return pd.concat([dest, sheet], ignore_index=True) 
    
def alfabetismo(sheet, y, is_victim, dest):
    if "Regresar" in sheet.columns:
        sheet.pop("Regresar")
    if is_victim:
        dfh = pd.DataFrame(columns=["Grupos de edad", "Total","Alfabeta","Analfabeta","Ignorado","Sexo"])
        dfh["Grupos de edad"] = list(sheet.iloc[7:,0])
        dfh["Total"] = list(sheet.iloc[7:,2])
        dfh["Alfabeta"] = list(sheet.iloc[7:,5])
        dfh["Analfabeta"] = list(sheet.iloc[7:,8])
        dfh["Ignorado"] = list(sheet.iloc[7:,11])
        dfh["Sexo"] = "H"
        dfm = pd.DataFrame(columns=["Grupos de edad", "Total","Alfabeta","Analfabeta","Ignorado","Sexo"])
        dfm["Grupos de edad"] = list(sheet.iloc[7:,0])
        dfm["Total"] = list(sheet.iloc[7:,3])
        dfm["Alfabeta"] = list(sheet.iloc[7:,6])
        dfm["Analfabeta"] = list(sheet.iloc[7:,9])
        dfm["Ignorado"] = list(sheet.iloc[7:,12])
        dfm["Sexo"] = "M"
        rslt = pd.concat([dfh, dfm], ignore_index=True)
        rslt["Victima o Agresor"] = "V"
        rslt["Anio"] = y
        return pd.concat([dest, rslt], ignore_index=True)
    else:
        upper = 20
        dfh = pd.DataFrame(columns=["Grupos de edad", "Total","Alfabeta","Analfabeta","Ignorado","Sexo"])
        dfh["Grupos de edad"] = list(sheet.iloc[7:upper,0])
        dfh["Total"] = list(sheet.iloc[7:upper,2])
        dfh["Alfabeta"] = list(sheet.iloc[7:upper,5])
        dfh["Analfabeta"] = list(sheet.iloc[7:upper,8])
        dfh["Ignorado"] = list(sheet.iloc[7:upper,11])
        dfh["Sexo"] = "H"
        dfm = pd.DataFrame(columns=["Grupos de edad", "Total","Alfabeta","Analfabeta","Ignorado","Sexo"])
        dfm["Grupos de edad"] = list(sheet.iloc[7:upper,0])
        dfm["Total"] = list(sheet.iloc[7:upper,3])
        dfm["Alfabeta"] = list(sheet.iloc[7:upper,6])
        dfm["Analfabeta"] = list(sheet.iloc[7:upper,9])
        dfm["Ignorado"] = list(sheet.iloc[7:upper,12])
        dfm["Sexo"] = "M"
        rslt = pd.concat([dfh, dfm], ignore_index=True)
        rslt["Victima o Agresor"] = "A"
        rslt["Anio"] = y
        return pd.concat([dest, rslt], ignore_index=True)
        
    
def vif_loader():
    years = ['09','10','11','12','13','14','15','16','17','18','19','20','21']
    ignore = ["Indice","Índice","Metodología","Directorio","Presentación"]
    
    VifAreaSexoEdad = pd.DataFrame()
    VifPuebloSexoRelacion = pd.DataFrame()
    VifEscolaridad = pd.DataFrame()
    VifAlfa = pd.DataFrame()
    for y in years:
        xlsx_path = f"./raw/vif/{y}.xlsx"
        sheets = pd.read_excel(io=xlsx_path, sheet_name=None)
        sheets = {name: df for name, df in sheets.items() if name not in ignore}
        skeys = list(sheets.keys())
        
        # # 1. VifAreaSexoEdad
            ## Victima
        t_area_sexo_edad_v = sheets[skeys[0]]
        VifAreaSexoEdad = area_sexo_edad_v(t_area_sexo_edad_v, y, VifAreaSexoEdad)
            ## Agresor
        aggkey1 = 36
        if int(y) >=14:
            aggkey1+=2
        elif int(y) >=12:
            aggkey1+=1
        t_area_sexo_edad_a = sheets[skeys[aggkey1]]
        VifAreaSexoEdad = area_sexo_edad_a(t_area_sexo_edad_a, y, VifAreaSexoEdad)
        
        # 2. VifPuebloSexoRelacion
        t_psr = sheets[skeys[1]]
        VifPuebloSexoRelacion = psr(t_psr, y, VifPuebloSexoRelacion)
        
        # 3. VifEscolaridad
        t_escolaridad_v = sheets[skeys[7]]
        VifEscolaridad = escolaridad(t_escolaridad_v, y, True,VifEscolaridad)
        aggkey2 = 40
        if int(y)>=14:
            aggkey2+=2
        elif int(y)>=12:
            aggkey2+=1
        t_escolaridad_a = sheets[skeys[aggkey2]]
        VifEscolaridad = escolaridad(t_escolaridad_a, y, False, VifEscolaridad)
        
        # 4. Alfabetismo
        t_alfa = sheets[skeys[6]]
        VifAlfa = alfabetismo(t_alfa, y,True,VifAlfa)
        aggkey3 = 41
        if int(y)>=14:
            aggkey3+=2
        elif int(y)>=12:
            aggkey3+=1
        t_alfa_a = sheets[skeys[aggkey3]]
        VifAlfa = alfabetismo(t_alfa_a, y, False, VifAlfa)
        
        
    VifAreaSexoEdad.to_csv(f"./data/vif/VifAreaSexoEdad.csv", index=False)
    VifPuebloSexoRelacion.to_csv(f"./data/vif/VifPuebloSexoRelacion.csv", index=False)
    VifEscolaridad.to_csv(f"./data/vif/VifEscolaridad.csv", index=False)
    VifAlfa.to_csv(f"./data/vif/VifAlfa.csv", index=False)