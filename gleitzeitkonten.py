import streamlit as st
#import pandas as pd
import math
import locale

feste_feiertage = 5
bewegliche_feiertage = 5
wochentage = 5
jahreswochen = 365.2425/7


# convert Altiums pin csv to Xilinx xgc
st.title(f"Gleitzeitkonten cronologic")
in1, in2, in3 = st.columns(3)
wochenstunden = in1.number_input("Wochenstunden", value=35)
stundenlohn = in2.number_input("Stundenlohn", value=25)
urlaubswochen = in3.number_input("Urlaubswochen", value=5.6, step=0.1)

feste_feiertagsstunden      = feste_feiertage     *wochenstunden/wochentage
bewegliche_feiertagsstunden = bewegliche_feiertage*wochenstunden/7
urlaubsstunden              = urlaubswochen*wochenstunden

bezahlte_stunden = math.ceil(jahreswochen * wochenstunden)
arbeitsstunden = math.floor(bezahlte_stunden - feste_feiertagsstunden - bewegliche_feiertagsstunden - urlaubsstunden)  
monatsbrutto = math.ceil(bezahlte_stunden * stundenlohn /12)
jahresbrutto = monatsbrutto*12 

st.header("Pro Jahr")
res1, res2, res3 = st.columns(3)
res1.metric("arbeiten", f"{arbeitsstunden}h", f"{arbeitsstunden/12:.2f}h pro Monat")
res2.metric("bezahlt", f"{bezahlte_stunden}h", f"{bezahlte_stunden/12:.2f}h pro Monat")

locale.setlocale(locale.LC_ALL, '')
locale._override_localeconv = {'mon_thousands_sep': '.'}
printjahresbrutto = locale.format_string('%.0f', jahresbrutto, grouping=True, monetary=True)
printmonatsbrutto = locale.format_string('%.0f', monatsbrutto, grouping=True, monetary=True)
res3.metric("Bruttogehalt", f"{printjahresbrutto}€",f"{printmonatsbrutto}€ pro Monat")

st.header("Berechnungsgrundlagen")
basis1, basis2, basis3 = st.columns(3)
basis1.metric("Feste Feiertage", feste_feiertage, f"-{feste_feiertagsstunden:.0f}h pro Jahr")
basis2.metric("Bewegliche Feiertage", bewegliche_feiertage, f"-{bewegliche_feiertagsstunden:.0f}h pro Jahr")
basis3.metric("Urlaubstage", f"{urlaubswochen*wochentage:.1f}", f"-{urlaubsstunden:.0f}h pro Jahr")
st.info(f"Berechnet mit {jahreswochen:.4f} Wochen pro Jahr")

"""
___
# Gleitzeitkonten bei cronologic
Mit diesem Tool können Mitarbeitende bei [cronologic GmbH & Co. KG](https://www.cronologic.de/) Berechnungen zu ihren Arbeitsverträgen durchführen. 

## Verwendung
### Online
Dieses Tool wird online gehostet bei [Render](https://gleitzeitkonten.onrender.com/).


### Lokal
Um das Tool lokal zu verwenden muss Python and Streaml.it installiert sein. Kopiere `gleitzeitkonten.py` auf Deinen Computer - oder clone das GitHub repository - und führe dann das folgende Kommando aus:
```shell
streamlit run gleitzeitkonten.py
```

## Quelltext 
Der Quelltext für dieses Tool wird unter [GitHub](https://github.com/cronologic-de/gleitzeitkonen) gehostet. 

## Lizenz

Der Code in diesem Repository steht unter der [Mozilla Public License 2.0](LICENSE). Das bedeutet, dass Du mehr oder weniger mit dem Code tun kannst was Du woll. Wenn Du jedoch Veränderungen an dem Code vornimmst musst Du diese uns oder Dritten auf Anfrage zur Verfügung stellen.
Wenn Du Änderungen an diesem Repository vornimmst, erklärst Du Dich damit bereit, diese uns unter der angegebenen Lizenz zur Verfügung zu stellen.

## Impressum

This Dienst wird bereitgestellt von:

    cronologic GmbH & Co. KG
    Jahnstraße 49
    60318 Frankfurt
    Germany
    https://www.cronologic.de/contact
    ++49 69 173 20 25 61

## Datenschutz
Dieser Dienst wird bei remder.com gehostet. Es gilt deren [Datenschutzerklärung](https://render.com/privacy).
Cronologic hat keine Kontrolle darüber, wie Render Daten erhebt und hat auch keinen Zugang zu diesen Daten.
Cronologic selbst erhebt keine Daten in Verbindung mit diesem Dienst.
Datenschutzveauftragter ist Kolja Sulimma. Er ist unter der oben angegebenen Addresse erreichbar.
"""
