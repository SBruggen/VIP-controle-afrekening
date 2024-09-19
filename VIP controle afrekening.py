import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
import locale 

# Set the locale to Dutch
locale.setlocale(locale.LC_TIME, 'nl_NL.UTF-8')

### 1. Locaties
    # hardcoded (nog aan te passen)
loc_vip = os.path.join('..','..' , 'data', 'ExportVIPFacturen 20240910.csv')

### 2. Inladen data
df_vip_raw = pd.read_csv(loc_vip, sep=';')

### 3. Functies definiëren
def get_valid_date(prompt="Enter the date (DD-MM-YYYY): ", date_format='%d-%m-%Y'):
    """
    Prompt the user to enter a date in the specified format until a valid date is entered.

    Args:
    - prompt (str): The message to display to the user. Default is "Enter the date (DD-MM-YYYY): ".
    - date_format (str): The format string for the expected date format. Default is '%d-%m-%Y'.

    Returns:
    - datetime object: The validated date as a datetime object.
    """
    while True:
        date_str = input(prompt)
        try:
            dt_date = datetime.strptime(date_str, date_format)
            return dt_date
        except ValueError:
            print("Ongeldige datumnotatie. Gelieve een datum in te geven in het formaat DD-MM-YYYY.")

def get_valid_month_year(prompt="Enter the month and year (MM-YYYY): "):
    """
    Prompt the user to enter a month and year in the specified format until valid inputs are entered.

    Args:
    - prompt (str): The message to display to the user. Default is "Enter the month and year (MM-YYYY): ".

    Returns:
    - tuple: A tuple containing two datetime objects, the first and last day of the specified month.
    """
    date_format = '%m-%Y'
    while True:
        month_year_str = input(prompt)
        try:
            # Parse the month and year string into a datetime object pointing to the first day of the month
            first_day = datetime.strptime(month_year_str, date_format)
            # Compute the last day of the month
            next_month = first_day.replace(day=28) + timedelta(days=4)  # this will never fail
            last_day = next_month - timedelta(days=next_month.day)
            return first_day, last_day
        except ValueError:
            print("Ongeldige invoer. Gelieve een maand en jaar in te geven in het formaat MM-YYYY.")

### 4. Dataframe bijwerken
# vastgelegde waarden en copy dataframe
gem_ret = float(120) # vastgelegde retributie op het moment van schrijven (12/02/2024)
platf_ret = float(36.5)
df_vip = df_vip_raw

# Bedrag aanpassen naar notatie en aandeel aan gemeente gefactureerd
df_vip["Bedrag"] = df_vip["Bedrag"].replace(",", '.', regex=True).astype(float)    # bedragen gescheiden door een komma aanpassen naar gescheiden door een punt

# Omzetten 'AanvraagDatum' naar datetime
df_vip["AanvraagDatum"] = pd.to_datetime(df_vip["AanvraagDatum"], format='%Y-%m-%dT%H:%M:%S.%fZ')

# start- en einddatum
month_filter = input("Wil je de gegevens ophalen voor één volledige maan? (y/n): ")
if month_filter in ['yes', 'y', 'ok']: # berekend start en einddatum voor de gegeven maand
    startdatum, einddatum = get_valid_month_year(prompt="Geef de maand en het jaar van de facturatieperiode (MM-YYYY): ")
else: # manuele input van start en einddatum
    startdatum = get_valid_date(prompt = "Geef de startdatum van de facturatieperiode (DD-MM-YYYY): ")
    einddatum = get_valid_date(prompt = "Geef de einddatum van de facturatieperiode (DD-MM-YYYY): ")

print("Startdatum:", startdatum.strftime('%d-%m-%Y'))
print("Einddatum:", einddatum.strftime('%d-%m-%Y'))

# Aanpassen 'einddatum' om de laatste dag mee te nemen in het resultaat
einddatum += timedelta(days=1)

# Filteren
df_vip_p1 = df_vip.loc[(df_vip['AanvraagDatum'] >= str(startdatum)) & (df_vip['AanvraagDatum'] <= str(einddatum))].copy()

# bedrag aanpassen door subtractie platformretributie 

    # Identificeer rijen waar "Bedrag" gelijk is aan de gemeentelijke retributie + de platformretributie of enkel de platformretributie
rows_to_adjust = df_vip_p1[(df_vip_p1["Bedrag"] == gem_ret + platf_ret) | (df_vip_p1["Bedrag"] == platf_ret)]

    # De platformretributie aftrekken van de geïdentificeerde rijen
df_vip_p1.loc[rows_to_adjust.index, "Bedrag"] -= platf_ret

# Groepeer op 'AanvraagDatum', 'UwReferentie'en sommeer 'Bedrag'
overzicht_p1 = df_vip_p1.groupby(['AanvraagDatum', 'UwReferentie'])['Bedrag'].sum().reset_index()

# Bereken de som van de 'Bedrag' kolom and en benoeming als 'Totaal'
total_sum = overzicht_p1['Bedrag'].sum()
approw = pd.DataFrame({'Bedrag': [total_sum]}, index=['Totaal'])

# Concatenateren van de originele dataframe en de rij met de totale som
overzicht_p1 = pd.concat([overzicht_p1, approw])

# NaN waarden opvullen met een lege string
overzicht_p1 = overzicht_p1.fillna('')

# Datumnotatie aanpassen naar eenvoudiger formaat
overzicht_p1["AanvraagDatum"] =overzicht_p1["AanvraagDatum"].dt.strftime('%Y-%m-%d')

### 4. Exporteren naar excel
loc_excel = os.path.join('..', '..', 'output', 'rapport_afrekening.xlsx')
overzicht_p1.to_excel(loc_excel, sheet_name='aanvragen')
