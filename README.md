# Introductie

Gemeenten in Vlaanderen zijn allemaal aangesloten aan het VIP-portaal voor de verwerking van stedenbouwkundige inlichtingen tot een VIP-rapport per perceel. Aanvragers dienen hun aanvraag via dit portaal in en moeten hier ook meteen een betaling daarvoor uitvoeren. De aanvragen worden daarna via het Vlaamse VIP-Portaal verwerkt en de gegevens kunnen aangevuld worden via verwerking in een gemeentelijk GIS-systeem. De gemeente valideert het VIP-rapport waarna het afgeleverd wordt aan de aanvrager.

Gezien de verwerking van de betalingen via het VIP-platform gebeurt dienen daarna nog de gemeenten hierop volgend vergoed te worden. Daarvoor komt vanuit Athumi namens Vlaanderen maandelijks een factuur toe waarop de VIP-aanvragen van de voorgaande maand gebundeld staan. Een gemeente kan deze gegevens controleren met de gegevens die zij zelf heeft over de VIP-aanvragen binnen haar grondgebied. Hiertoe kan de data hierrond gedownload worden vanuit het VIP-portaal of vanuit het eigen gemeentelijke GIS-systeem. Het downloadbestand betreft een gestandaardiseerd csv-bestand waarin de gegevens van alle aanvragen binnen het grondgebied van de gemeente verzameld zijn.

Dit script laad de gemeentelijke data in csv-formaat in vanuit het VIP en verwerkt deze tot een rapport. Het geeft standaard de optie om dit te doen voor de periode van 1 maand, maar een andere start- en einddatum kunnen gespecifieerd worden. Zodoende wordt er een rapport bekomen dat gebruikt kan worden ter vergelijking met de gegevens in de factuur die verkregen wordt van Athumi.

# Installatie

Dit is een python script waarbij enkele paketten gebruikt worden. Deze kunnen via een package manager [pip](https://pip.pypa.io/en/stable/) geïnstalleerd worden.

'''bash
pip install pandas==2.2.0 datetime==5.5
'''
