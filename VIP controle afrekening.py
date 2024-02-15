import pandas as pd
import numpy as np
import os
from datetime import datetime
import locale 

# Set the locale to Dutch
locale.setlocale(locale.LC_TIME, 'nl_NL.UTF-8')

### 1. Locaties
loc_vip = os.path.join('..','..' , 'data', 'ExportVIPFacturen 20240205.csv')

### 2. Inladen data
df_vip_raw = pd.read_csv(loc_vip, sep=';')

### 3. Dataframe bijwerken
# vastgelegde waarden en copy dataframe
platformretributie = float(36.5) # vastgelegde retributie op het moment van schrijven (12/02/2024)
df_vip = df_vip_raw

# Bedrag aanpassen naar notatie en aandeel aan gemeente gefactureerd
df_vip["Bedrag"] = df_vip["Bedrag"].replace(",", '.', regex=True).astype(float)    # bedragen gescheiden door een komma aanpassen naar gescheiden door een punt
df_vip["Bedrag"] = df_vip["Bedrag"] - platformretributie # platform retributie wordt niet aan de stad doorbetaald, maar zit wel in de csv-export

# Omzetten 'AanvraagDatum' naar datetime
df_vip["AanvraagDatum"] = pd.to_datetime(df_vip["AanvraagDatum"], format='%Y-%m-%dT%H:%M:%S.%fZ')

# Omzetten 'AanvraagDatum' naar '%Y-%m-%d'
df_vip["AanvraagDatum"] = df_vip["AanvraagDatum"].dt.strftime('%Y-%m-%d')

# Filteren van de data en copy aanmaken
df_vip_p1 = df_vip.loc[(df_vip['AanvraagDatum'] >= '2024-01-01') & (df_vip['AanvraagDatum'] < '2024-01-18')].copy()

# Group by 'AanvraagDatum', 'UwReferentie'en sommeer 'Bedrag'
overzicht_p1 = df_vip_p1.groupby(['AanvraagDatum', 'UwReferentie'])['Bedrag'].sum().reset_index()

#totaal = np.sum(df_vip_p1.Bedrag)

# Calculate the sum of the 'Bedrag' column and rename the result
total_sum = overzicht_p1['Bedrag'].sum()
approw = pd.DataFrame({'Bedrag': [total_sum]}, index=['Totaal'])

# Concatenate the original DataFrame and the row containing the sum
overzicht_p1 = pd.concat([overzicht_p1, approw])

# Fill NaN values with an empty string
overzicht_p1 = overzicht_p1.fillna('')

### 4. Export to excel
loc_excel = os.path.join('..', '..', 'output', 'rapport_afrekening.xlsx')
overzicht_p1.to_excel(loc_excel, sheet_name='aanvragen')
