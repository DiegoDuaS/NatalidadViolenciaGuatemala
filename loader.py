
import math
import pandas as pd

def nat_dep_mes(sheet, y, dest):
    if "Regresar" in sheet.columns:
        sheet.pop("Regresar")

    cols = list(sheet.iloc[0])
    sheet.columns = cols
    sheet = sheet[1:].reset_index(drop=True) 
    if "Niñas" in cols:
        sheet.rename(columns={"Niñas": "Mujeres"}, inplace=True)
    if "Niños" in cols:
        sheet.rename(columns={"Niños": "Hombres"}, inplace=True)
    sheet["Anio"] = y
    return pd.concat([dest, sheet], ignore_index=True)

def nat_edad(sheet, y, dest):
    if "Regresar" in sheet.columns:
        sheet.pop("Regresar")
    cols = list(sheet.iloc[0])
    sheet.columns = cols
    sheet = sheet[1:].reset_index(drop=True) 
    sheet["Anio"] = y
    if(int(y)==9):
        sheet = sheet.iloc[:-1]
    return pd.concat([dest, sheet], ignore_index=True)
    
    
def nat_dep_ec(sheet, y, dest):
    if "Regresar" in sheet.columns:
        sheet.pop("Regresar")
    cols = list(sheet.iloc[0])
    sheet.columns = cols
    sheet = sheet[1:].reset_index(drop=True) 
    sheet["Anio"] = y
    return pd.concat([dest, sheet], ignore_index=True)
    
def nat_edad_ec(sheet, y, dest):
    if "Regresar" in sheet.columns:
        sheet.pop("Regresar")
    cols = list(sheet.iloc[0])
    sheet.columns = cols
    sheet = sheet[1:].reset_index(drop=True) 
    sheet["Anio"] = y
    return pd.concat([dest, sheet], ignore_index=True)
    
    
def nat_num(sheet, y, dest):
    if "Regresar" in sheet.columns:
        sheet.pop("Regresar")
    
    cols = list(sheet.iloc[0])
    sheet.columns = cols
    sheet = sheet[1:].reset_index(drop=True) 
    if(int(y)==9):
        sheet["Ignorado"] = 0
    sheet["Anio"] = y
    return pd.concat([dest, sheet], ignore_index=True)

def nat_ocup(sheet, y, dest):
    if "Regresar" in sheet.columns:
        sheet.pop("Regresar")
    
    cols = list(sheet.iloc[0])
    sheet.columns = cols
    sheet = sheet[1:].reset_index(drop=True)
    sheet["Anio"] = y
    return pd.concat([dest, sheet], ignore_index=True)
    
def nat_etnia_area(sheet, y, dest):
    if "Regresar" in sheet.columns:
        sheet.pop("Regresar")
    
    cols = list(sheet.iloc[0])
    sheet.columns = cols
    sheet = sheet[1:].reset_index(drop=True)
    if "Grupo étnico" in sheet.columns:
        sheet.rename(columns={"Grupo étnico": "Pueblo de pertenencia de la madre"}, inplace=True)
    if "Área geográfica" in sheet.columns:
        sheet.pop("Área geográfica")
    sheet["Anio"] = y
    return pd.concat([dest, sheet], ignore_index=True)
    
def nat_loader():
    years = ['09','10','11','12','13','14','15','16','17','18','19','20','21']
    ignore = ["Contenido","Presentación"]
    NatDepMes = pd.DataFrame()
    NatEdad = pd.DataFrame()
    NatDepEC = pd.DataFrame()
    NatEdadEC = pd.DataFrame()
    NatNum = pd.DataFrame()
    NatOcup = pd.DataFrame()
    NatEtniaArea = pd.DataFrame()
    for y in years:
        xlsx_path = f"./raw/nat/{y}.xls"
        if int(y)>=16:
            xlsx_path+="x"
        sheets = pd.read_excel(io=xlsx_path, sheet_name=None)
        sheets = {name: df for name, df in sheets.items() if name not in ignore}
        skeys = list(sheets.keys())
        
        # 1. NatDepMes
        tdep_mes = sheets[skeys[1]]
        NatDepMes = nat_dep_mes(tdep_mes, y, NatDepMes)
        
        # # 2. NatEdad
        t_edad = sheets[skeys[2]]
        NatEdad = nat_edad(t_edad,y,NatEdad)

        # # 3. NatDepEC
        t_dep_ec = sheets[skeys[4]]
        NatDepEC = nat_dep_ec(t_dep_ec, y , NatDepEC)
        
        
        # # 4. NatEdadEc
        t_nat_edad_ec = sheets[skeys[5]]
        NatEdadEC = nat_edad_ec(t_nat_edad_ec, y , NatEdadEC)
        
        # # 5. NatNum
        t_nat_num = sheets[skeys[8]]
        NatNum = nat_num(t_nat_num, y , NatNum)
        
        # # 6. NatOcupacion
        t_nat_ocup = sheets[skeys[13]]
        NatOcup = nat_ocup(t_nat_ocup, y,NatOcup)
        
        # # 7. NatEtniaArea
        t_nat_etnia_area = sheets[skeys[14]]
        NatEtniaArea = nat_etnia_area(t_nat_etnia_area, y,NatEtniaArea)
    
    # Crear Csvs
    NatDepMes.to_csv(f"NatDepMes.csv", index=False)
    NatEdad.to_csv(f"NatEdad.csv", index=False)
    NatDepEC.to_csv(f"NatDepEC.csv", index=False)
    NatEdadEC.to_csv(f"NatEdadEC.csv", index=False)
    NatNum.to_csv(f"NatNum.csv", index=False)
    NatOcup.to_csv(f"NatOcup.csv", index=False)
    NatEtniaArea.to_csv(f"NatEtniaArea.csv", index=False)