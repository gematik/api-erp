# **E-Rezept@RU**
Redaktion:  Wolfgang Hahn (Operations/Transition Manager E-Rezept)
Status:        ![(Warnung)](Aspose.Words.290423e4-b2cb-4eac-a77c-884c5f8c8e33.001.png) Diese Seiten werden permanent aktualisiert. Bitte schauen Sie öfter vorbei.


**News**

**Informationen zur RU:**
Bitte rechnen Sie mit eingeschränkter Erreichbarkeit der E-Rezept Komponenten Fachdienst (FD), Identity Provider (IDP) und des Apotheken-Verzeichnis (APOVZD) in der Umgebung RU** an den folgenden Tagen und Zeiträumen.

- **05.06.23 - 07.06.23 FD** 
  - TI-CHG-00015850 Performace-Tests
  - 05./06.06.23, 17:00 - 09:00
  - 06./07.06.23, 17:00 - 09:00 (optional)
- **05.06.2023 IDP** 
  - TI-CHG-00015701 Wartungsarbeiten RZ
  - 00:00 - 05:00
- **25.05.2023 IDP** 
  - TI-CHG-00015560 Patchday für IDP-Infrastruktur Q2-2023
  - 09:00 - 17:00
## <a name="erezept@ru-kapitel"></a>**Kapitel**
- [**E-Rezept@RU**](#e-rezeptru)
  - [**Kapitel**](#kapitel)
  - [**FAQ/Informationen**](#faqinformationen)
  - [**Umgebungsstatus und -forecast**](#umgebungsstatus-und--forecast)
  - [**Release Hinweise E-Rezept Komponenten**](#release-hinweise-e-rezept-komponenten)
    - [**Fachdienst (FD)**](#fachdienst-fd)
    - [**Identity Provider (IdP)**](#identity-provider-idp)
    - [**Front-End des Versicherten (FdV) - iOS**](#front-end-des-versicherten-fdv---ios)
    - [**Front-End des Versicherten (FdV) - Android und Harmony**](#front-end-des-versicherten-fdv---android-und-harmony)
    - [**Anwendung des Versicherten (AdV)**](#anwendung-des-versicherten-adv)
    - [**Apotheken-Verzeichnisdienst (APOVZD)**](#apotheken-verzeichnisdienst-apovzd)
    - [**Nutzungsplan - Test**](#nutzungsplan---test)
## <a name="erezept@ru-faq/informationen"></a>**FAQ/Informationen**
**Bereitstellung der RU-DEV**

Mit der RU-DEV wurde neben der RU, TU und PU eine neue Instanz der RU implementiert. Die Instanz dient zur frühzeitigen Bereitstellung von zukünftigen Entwicklungsstufen des E-Rezept Fachdienstes zum Zweck der Validierung von Änderungen an den Primärsystemen. Es erfolgt keine Einbindung in das TI-ITSM und die Umgebung unterliegt keinen Service Leveln. Die Steuerung erfolgt in direkter Abstimmung zwischen der gematik und IBM. Über den aktuellen Release-Stand und Downtimes wird auf dieser Seite informiert. Alle Primärsystem-Hersteller die über eine Registrierung am IDP für das E-Rezept verfügen, haben Informationen zur Herstellung der Anbindung erhalten und können diese individuell nutzen. 

**Bundesweite Testphase zur Einführung des E-Rezeptes**

Die Einführung wird durch die gematik koordiniert und u.a. durch die Etablierung des Industriepartner-Formums unterstützt. Hierin finden Sie Informationen zu den Teilnehmern (ARZ, Hersteller AVS/PVS/KIS, Kassen, Kassen-Dienstleister und Projektpartner), Verweise auf weitere Abstimmungsformate, Informationen über den Hochlauf der E-Rezept Nutzung sowie Protokolle der Abstimmungen der Industriepartner.
Informationen zum Forum:  [Stabilisierung und Interoperabilität](file:///C:/pages/viewpage.action?pageId=444108929).

**FHIR-Release-Pakete und Verfügbarkeit in der RU**

Es wird eine Übersicht der FHIR-Release-Pakete der Prozessbeteiligten KBV, DAV, GKV, PKV und gematik zur Verfügung gestellt. Alle Prozessbeteiligten verantworten je mindestens ein FHIR-Profilierungs-Projekt, das im E-Rezept verwendet wird. Die dort dokumentierte Planung repräsentiert die PU.
Informationen zum Forum:  [E-Rezept FHIR-Package Versionsmanagement](https://github.com/gematik/api-erp/blob/master/docs/erp_fhirversion.adoc "Verknüpfung folgen")
Aktuelle gematik E-Rezept FHIR-Konfiguration RU:  [de.gematik.erezept-workflow.r4 #1.1.1](https://simplifier.net/packages/de.gematik.erezept-workflow.r4/1.1.1)

**Verfügbarkeiten E-Rezept / Monitoring TI-Lagebild der RU**

Die Verfügbarkeit der zum E-Rezept Service zugehöhrenden Anwendungen und Dienste wird im [Monitoring TI-Lagebild der RU](https://ti-lage.prod.ccs.gematik.solutions/d/Nuoeai0nk/lagebild-ru-referenzumgebung?orgId=1&kiosk) fortlaufend aktualisiert. 

**Zugang zu Know-how, Best Practise und Services**

Die gematik stellt ein Portal zur Verfügung, in dem Auffälligkeiten und erkannte Fehler u.a. zum E-Rezept eingestellt werden können. Im Ergebnis werden hierin zu Fehlern, Auffälligkeiten und weiteren Themen Lösungswege und Zusatzinformationen kommuniziert. 
Informationen zum Forum:  [Jira Servicedesk](https://gematik.atlassian.net/jira/servicedesk/projects/ANFERP/knowledge/articles/781779028 "Verknüpfung folgen")

**Zugang zu Produktinformationen**

Im [Fachportal](https://fachportal.gematik.de/dokumentensuche) der gematik werden u.a. Informationen zu den Spezifikationen der zum E-Rezept zugehörenden Produkttypen wie folgt bereitgestellt.
Die jeweils aktuellsten Produkttypversionen sind:. 

- Fachdienst:  [PTV 1.6.0-0](https://fachportal.gematik.de/dokumentensuche?tx_gemcharacteristics_productlist%5BformIdentifier%5D=form-2849&tx_gemcharacteristics_productlist%5Btype%5D=ProdT&tx_gemcharacteristics_productlist%5Bproducttype%5D=107&tx_gemcharacteristics_productlist%5Bproducttypeversion%5D=19#c2849)
- Identity Provider:  [PTV 2.4.0-0](https://fachportal.gematik.de/dokumentensuche?tx_gemcharacteristics_productlist%5BformIdentifier%5D=form-2849&tx_gemcharacteristics_productlist%5Btype%5D=ProdT&tx_gemcharacteristics_productlist%5Bproducttype%5D=101&tx_gemcharacteristics_productlist%5Bproducttypeversion%5D=105#c2849)
- Frontend des Versicherten:  [PTV 1.5.0-0](https://fachportal.gematik.de/dokumentensuche?tx_gemcharacteristics_productlist%5BformIdentifier%5D=form-2849&tx_gemcharacteristics_productlist%5Btype%5D=ProdT&tx_gemcharacteristics_productlist%5Bproducttype%5D=108&tx_gemcharacteristics_productlist%5Bproducttypeversion%5D=75#c2849)
- Anwendung des Versicherten:  n.a.
- Apothekenverzeichnis:  [APOVZD 1.3.0-0](https://fachportal.gematik.de/dokumentensuche?tx_gemcharacteristics_productlist%5BformIdentifier%5D=form-2849&tx_gemcharacteristics_productlist%5Btype%5D=ProdT&tx_gemcharacteristics_productlist%5Bproducttype%5D=166&tx_gemcharacteristics_productlist%5Bproducttypeversion%5D=30#c2849)

**Integrative Erpobung für Hersteller**

Das E-Rezept wird kontinuierlich weiterentwickelt und gepflegt. Um Herstellern von Primärsystemen frühzeitig Möglichkeiten für den Test der entsprechenden Änderungen zu ermöglichen, werden auf der RU Konnekthatons durchgführt. Informationen über erfolgte und geplante Konnektathons oder die Teilnahme an zukünftigen Veranstaltungen stehen im [Fachportal der gematik](https://fachportal.gematik.de/veranstaltungen?no_cache=1&tx_sfeventmgt_pievent%5Baction%5D=list&tx_sfeventmgt_pievent%5Bcontroller%5D=Event&cHash=aea5ea3ef553f996dbbaa376d60f6c1b) zur Verfügung.

## <a name="erezept@ru-umgebungsstatusund-forecast"></a>**Umgebungsstatus und -forecast**
In Ergänzung zu den Informationen zur RU werden für die Komponenten des E-Rezeptes im Folgenden die aktuellen und geplanten Installationsstände der Umgebungen dokumentiert. Detailinformationen zu dedizierten E-Rezept Releases finden sich in den Release Hinweisen.

Status; Entwurf
Legende: i.A. - In Abstimmung  I  **ROT** - Zeitfenster mit besonderen Anforderungen an Umgebungsverfügbarkeit  I  **BLAU** - Deployments (beim FD mit oder ohne Anpassung FHIR-Konfiguration)

| eRp FD (inkl. System- bzw. FHIR-Konfiguration) | eRp IDP                                           | eRp FdV (iOS)                   | eRp FdV (Android)            | eRp AdV        | APOVZD         |
|-----------------------------------------------------------------------------------------------------|---------------------------------------------------|---------------------------------|------------------------------|----------------|----------------|
| Events                                                                                              | RU-DEV                                            | RU                  | TU               | PU | RU | TU | PU | PU | PU | PU | RU | PU |
| Heute                                                                                               | 1.11.0 RC3„Vor Übergangszeit“                     | 1.10.0-2„Während Übergangszeit“ | 1.10.0-2„Nach Übergangszeit“ | 1.9.0-2        | 3.0.4-6        | 3.0.4-6        | 3.0.4-6        | 1.8.0          | 1.10.0         | 1.2.1          | 1.3.0-1            | 1.0.0-13       |
| 31\.03.23                                                                                           | 1\.11.0  RC3„Vor Übergangszeit“                   |
| 05\.06.23                                                                                           | 1\.10.0-2„Nach Übergangszeit“(konfigurativ)       |
| 07\.06.23                                                                                           | 1\.10.0-2„Vor Übergangszeit“(konfigurativ)        |
| 09\.06.23                                                                                           | 1\.10.0-2„Während Übergangszeit“(konfigurativ)    |
| 20\.06.23                                                                                           | 1\.10.0-2„Vor Übergangszeit“                      |
| 21\.06.23                                                                                           | Installation VSDM HMAC-Schlüssel in VAU eRp FD    |
| 22\.06.23                                                                                           | Installation VSDM HMAC-Schlüssel in VSDM-Systemen |
| 01\.07.23                                                                                           | 1\.10.0-2„Während Übergangszeit“ (konfigurativ)   |


**Informationen zur RU-DEV:**
In der RU-DEV werden durch den Anbieter IBM frühzeitig in Umsetzung befindliche Änderungen am E-Rezept Fachdienst installiert und für Tests durch periphere Anwendungen und Komponenten bereitgestellt. 
Im Folgenden werden Installationen oder Aktivitäten angezeigt, die Einfluss auf die Verfügbarkeit des Service haben.

- Die Konfiguration des FD in der RU-DEV wurde am 12.05.23 wieder auf „Vor Übergangszeit" (mit PKV) geändert. 
- Die Installation eRp FD 1.11.0 RC3 erfolgte am 31.05.23 mit derselben Konfiguration.

**Informationen zur RU:**

- Die Installation eRp FD 1.10.0-2 ist am 23.05.23 erfolgt (s. unten Details).
- FHIR: 
  - Die Umstellung auf die Konfiguration „Während Übergangszeit“ erfolgte am 09.05.23. Dies erfolgt durch konfigurative Änderungen in der aktuellen Produktversion.
  - Für weitere Informationen siehe auch: [github.com/.../erp_versionsuebergang/...](https://github.com/gematik/api-erp/blob/master/docs/erp_versionsuebergang.adoc#zust%C3%A4nde-des-fachdienstes-im-zusammenhang-mit-dem-%C3%BCbergangszeitraum)

**Informationen zur TU:**

- Die Installation eRp FD 1.10.0-2 ist am 24.05.23 erfolgt (s. unten Details).
- Für Zulassungstests eRp FD wird das Verhalten der FHIR-Validierung mehrfach konfigurativ geändert. Die EInstellungen sind der o.a. Tabelle zu entnehmen.

**Informationen zur PU:**

- Die Installation eRp FD 1.9.0-2 ist am 09.05.23 erfolgt.
- Für das Feature "eGK in der Apotheke" (Verifikation mit Prüfziffer (VSDM++)) werden am 21.06.23 und am 22.06.23 HMAC-Schlüssel in die Systeme des E-Rezept Fachdienstes und der VSDM-Systeme eingebracht. Das Feature ist somit ab dem 23.06.23 produktiv.

**Informationen zu APOVZD:**

- APOVZD 1.3.0-0 
  - Beim APOVZD findet eine Reorganisation der Versions-Nummerierung statt. Die aktuelle Version 1.0.1-0 wird demnach mit den hier adressierten Änderungen auf die Produktversion 1.3.0-0 gehoben und orientiert sich zukünftig an den Produktsteckbriefen APOVZD. 
  - Die Produktiversion enthält die Funktionalität für "Einlösen E-Rezept ohne Anmeldung am E-Rezept-Fachdienst".
  - Die eRp FdV werden korrespondierend dazu bereitgestellt.
- APOVZD 1.3.0-1 
  - Betrieblicher Patch (s. unten Details).

..
## <a name="erezept@ru-releasehinweisee-rezeptkomponenten"></a>**Release Hinweise E-Rezept Komponenten**
Es wird fortlaufend über geplante und in Umsetzung befindliche E-Rezept Release berichtet. Informationen, die älter als 1 Jahr sind, werden entfernt.
### <a name="erezept@ru-fachdienst(fd)"></a>**Fachdienst (FD)** 
Legende:  i.A. - in Abstimmung

|**Label......................**|**Produkt<br>Version**|**Inhalt/Umfang**|**Zusatz-informationen**|**Deployment.....**|
| :- | :- | :- | :- | :- |
|eRp FD 1.11.0-0|1\.11.0-0|<p>Funktionale Änderungen:</p><p>- E-Rezept: Übergangsfrist für die Nutzung des Packages</p><p>- E-Rezept-Fachdienst: Prüfung Gültigkeit Profilversionen</p><p>- Einführung Föderierter IdP (geplant)</p><p>- ...</p><p>Betriebliche Änderungen:</p><p>- BDE v2 Erweiterung Meesagefeld</p><p>- ...</p><p>Fehlerbehebungen:</p><p>- ...</p>||RU-DEV: 31.05.23 RC3<br>RU: 04.07.23<br>TU: 08.08.23<br>PU: 22.08.2|
|eRp FD 1.10.0-2|1\.10.0-2|<p>Änderungen:</p><p>- erp-processing (VAU)</p><p>- Austausch FHIR Profil Package "kbv.ita.erp" 1.1.1</p><p>- Retry-Verfahren an Web-Schnittstelle</p><p>- Performanceverbesserungen</p><p>- Fehlerbehebungen</p>|<p>eRp FD 1.10.0-2:<br>[Release Note](file:///C:/download/attachments/444109897/ERP-E-Rezept_Fachdienst_Produktversion_1.10.0-2-ReleaseNote1.0.pdf?version=1&modificationDate=1684240512555&api=v2)</p><p>eRp FD 1.10.0-1:<br>[Release Note](file:///C:/download/attachments/444109897/E-Rezept_Fachdienst_Produktversion_1.10.0-1-ReleaseNote1.0.pdf?version=1&modificationDate=1682676448534&api=v2)</p><p>eRp FD 1.10.0-0:<br>[Release Note](file:///C:/download/attachments/444109897/E-Rezept_Fachdienst_Produktversion_1.10.0-ReleaseNote1.1.pdf?version=2&modificationDate=1684240584037&api=v2)</p>|RU-DEV: -<br>RU: 23.05.23<br>TU: 24.05.23<br>PU: 20.06.23|
|eRp FD 1.10.0-1|1\.10.0-1|<p>Änderungen:</p><p>- FehlerFix bzgl. Validierung ungültiger FHIR-Profile</p>|[Release Note](file:///C:/download/attachments/444109897/E-Rezept_Fachdienst_Produktversion_1.10.0-1-ReleaseNote1.0.pdf?version=1&modificationDate=1682676448534&api=v2)|RU-DEV: -<br>RU: 04.05.23<br>TU: 05.05.23<br>PU: 20.06.23|
|eRp FD 1.10.0-0|1\.10.0-0|<p>Funktionale Änderungen:</p><p>- Einlösen E-Rezept mit eGK in der Apotheke mit Verifikation mittels strukturierter Prüfziffer (VSDM++)</p><p>- Bereitstellung FHIR Profile (gültig ab 01.07.23)</p><p>- Statusanzeige Gelöschtes E-Rezept in der E-Rezept-App</p><p>- Korrektur FHIR Namingsystem E-Rezept</p><p>- Korrektur Bezeichner AccessCode in A\_22128</p><p>- MVO: Prüfung Startdatum nicht vor Ausstelldatum, Prüfung Endedatum</p><p>- Ablehnung unbekannte Extension</p><p>- Abrechnungsinformation ändern - kein AccessCode an abgebende LEI</p><p>- Festlegungen zur Validierung der FHIR-Ressource nach dem 01.07.23</p>|[Release Note](file:///C:/download/attachments/444109897/E-Rezept_Fachdienst_Produktversion_1.10.0-ReleaseNote1.1.pdf?version=2&modificationDate=1684240584037&api=v2)|RU-DEV: 12.04.23<br>RU: 20.04.23<br>TU: -<br>PU: -|
|eRp FD 1.9.0-2|1\.9.0-2|<p>Änderungen: </p><p>- Verbesserung Logging Timer Task</p><p>- Fehlerbehebung</p>|[Release Note](file:///C:/download/attachments/444109897/E-Rezept_Fachdienst_Produktversion_1.9.0-2-ReleaseNote1.0.pdf?version=1&modificationDate=1682679352679&api=v2)|RU-DEV: -<br>RU: -<br>TU: 02.05.23<br>PU: 09.05.23|
|eRp FD 1.9.0-1|1\.9.0-1|<p>Änderungen: </p><p>- Umstellung auf Rohdatenlieferung V2 (aktiv)</p>|[Release Note](file:///C:/download/attachments/444109897/E-Rezept_Fachdienst_Produktversion_1.9.0-2-ReleaseNote1.0.pdf?version=1&modificationDate=1682679352679&api=v2)|RU-DEV: -<br>RU: 28.03.23<br>TU: 29.03.23<br>PU: 18.04.23|
|eRp FD 1.9.0-0|1\.9.0-0|<p>Funktionale Änderungen (Wirksamkeit in PU ab 11.04.23):</p><p>- Quittung erstellen (OCSP-Response nicht älter als 24 Stunden)</p><p>- Konsolidierung Anforderung für Gültigkeitsprüfung Signaturzertifikat</p><p>- MVO: Prüfung Rezeptdatum (Endedatum nach Startdatum)</p><p>- MVO: Datumsformat in OperationOutcome</p><p>- Löschfrist abgelaufener Rezepte auf 5 Tage</p><p>- TaskID = RezeptID</p><p>Funktionale Änderungen (Wirksamkeit ab 01.07.23):</p><p>- Aktualisierung der 2023 gematik/KBV/DAV FHIR Profile</p><p>- PKV: verschreibungspflichtige Arzneimittel (Restarbeiten Stufe 2)</p><p>- PKV: Ergänzungen (Prüfung/Übergabe AccessCode, Handhabung von Abgabeinformationen (Löschen von Nachrichten/Ressourcen), Korrektur Workflow 209 (Task abrufen und E-Rezept löschen) </p><p>- Korrektur WF 209 (Trennung Workflow und Abrechnungsinformationen)</p><p>Betriebliche Änderungen:</p><p>- Umstellung auf Rohdatenlieferung V2 (inaktiv)</p><p>Fehlerbehebungen:</p><p>- Verwaltung DB-Connection</p><p>- GET Communication/Task/AuditEvent</p><p>- Prüfung Unfallkennzeichen</p><p>- Handling FdV (VAU decrytion)</p><p>- Referenz(en) auf Medication</p><p>- Validierung URL Attribute in FHIR-Ressourcen</p>|[Release Note](file:///C:/download/attachments/444109897/ERP-E-Rezept_Fachdienst_Produktversion_1.9.0-ReleaseNote1.0.pdf?version=1&modificationDate=1676962671871&api=v2)|RU-DEV: 20.02.23 (RC4)<br>RU: 21.02.23<br>TU: -<br>PU: -|
|eRp FD 1.8.1-1|1\.8.1-1|<p>Fehlerbehebungen:</p><p>- Fix des Subscription-Servers</p>|[Release Note](file:///C:/download/attachments/444109897/ERP-E-Rezept_Fachdienst_Produktversion_1.8.1-1-ReleaseNote1.0.pdf?version=1&modificationDate=1676529062817&api=v2)|RU: 17.02.23<br>TU: 17.02.23<br>PU: 21..02.23|
|eRp FD 1.8.1-0|1\.8.1-0|<p>Release eRp FD 1.8.1-0 enthält ausschließlich die Deaktivierung der Funktion "E-Rezept mit eGK in der Apotheke ohne PIN" und umfasst weiterhin die Änderungen mit den Produktversionen 1.8.0-0 - 1.8.0-2.</p><p>Funktionale Änderungen:</p><p>- Kodierung fullURL (A\_22920)</p><p>- Verallgemeinerung Anforderungen (http-Returncode)</p><p>- Zuordnung A\_22383</p><p>- Prüfverfahren A\_22103 - Fehlerdetails in OperationOutcome</p><p>- FHIR Version E-Rezept Workflow (A\_22483)</p><p>- Vorbereitung E-Rezept FHIR Validator </p><p>Fehlerbehebungen:</p><p>- Update libxml2, Feature Toggle und Behebung Schwachstelle bei Abruf in der Apotheke</p><p>- fehlerhafte Referenzen in task.input (task accept response)</p><p>- Handling Maintenance Mode</p><p>- Reconnect Subscription Server</p>|<p>eRp FD 1.8.1-0<br>[Release Note](file:///C:/download/attachments/444109897/ERP-E-Rezept_Fachdienst_Produktversion_1.8.1-ReleaseNote1.1.pdf?version=1&modificationDate=1671007357207&api=v2)</p><p>eRp FD 1.8.0-2<br>[Release Note](file:///C:/download/attachments/444109897/ERP-E-Rezept_Fachdienst_Produktversion_1.8.0-2-ReleaseNote1.0.pdf?version=1&modificationDate=1667308205152&api=v2)</p><p>eRp FD 1.8.0-1<br>[Release Note](file:///C:/download/attachments/444109897/ERP-E-Rezept_Fachdienst_Produktversion_1.8.0-1-ReleaseNote1.0.pdf?version=1&modificationDate=1666184522610&api=v2)</p><p>eRp FD 1.8.0-0<br>[Release Note](file:///C:/download/attachments/444109897/ERP-E-Rezept_Fachdienst_Produktversion_1.8.0-ReleaseNote1.2.pdf?version=1&modificationDate=1666184542191&api=v2)</p>|RU-DEV: 05.11.22<br>RU: 30.11.22<br>TU: 28.11..22<br>PU: 06.12.22|
|eRp FD 1.7.0-2|1\.7.0-2|- Fehlerbehebungen (u.a. HTTP 500 Fehler, Signal Termination in RU) |[Release Note](file:///C:/download/attachments/444109897/ERP-E-Rezept_Fachdienst_Produktversion_1.7.0-2-ReleaseNote1.0.pdf?version=1&modificationDate=1663047437776&api=v2)|RU-DEV: 09.09.22<br>RU: 15.09.22<br>TU: 16.09.22<br>PU: 04.10.22|
|eRp FD 1.7.0-1|1\.7.0-1|<p>Änderungen werden mit eRp FD 1.7.0-2 ausgerollt:</p><p>- Fehlerbehebungen (u.a. MVO Statuscode 500, Management Zertifikate und Refresh Jobs) </p>|[Release Note](file:///C:/download/attachments/444109897/ERP-E-Rezept_Fachdienst_Produktversion_1.7.0-1-ReleaseNote1.0.pdf?version=1&modificationDate=1661513040453&api=v2)|RU-DEV: 29.08.22<br>RU: 06.09.22<br>TU: -<br>PU: -|
|eRp FD 1.7.0-0|1\.7.0-0|<p>Änderungen werden mit eRp FD 1.7.0-2 ausgerollt:</p><p>- E-Rezept FHIR Validator (Basis-Validator)</p><p>- Feature Mehrfachverordnungen (MVO)</p><p>- MVO: zulässige Workflows 169 und 209</p><p>- Nachträgliche Einbettung OCSP-Response in QES</p><p>- Übergangsregelung unbekannte Extension</p><p>- Rohdaten Erweiterung: Lieferung LEI-Pseudonym</p>|[Release Note](file:///C:/download/attachments/444109897/ERP-E-Rezept_Fachdienst_Produktversion_1.7.0-ReleaseNote1.0-280722-1528-516.pdf?version=1&modificationDate=1659083995306&api=v2)|<p>RU-DEV: 29.07.22<br>RU: 05.08.22<br>TU: -<br>PU: -</p><p>--------------------------</p>|
|eRp FD 1.6.0-2|1\.6.0-2|<p>- Security Patch</p><p>- Verbesserung Management Maintenance Mode</p>|[Release Note](file:///C:/download/attachments/444109897/ERP-E-Rezept_Fachdienst_Produktversion_1.5.0-2-ReleaseNote1.0.pdf?version=1&modificationDate=1657032197192&api=v2)|RU-DEV: i.A.<br>RU: 15.07.22<br>TU: 15.07.22<br>PU: 26.07.22|
|eRp FD 1.6.0-1|1\.6.0-1|<p>Änderungen werden mit eRp FD 1.6.0-2 ausgerollt:</p><p>- Konfigurationsoption VAU-Proxy bzgl. DOS Prüfung</p><p>- Fehlerbehebung ERP-10359 (Prüfung an Datumsgrenze)</p>|[Release Note](file:///C:/download/attachments/444109897/ERP-E-Rezept_Fachdienst_Produktversion_1.6.0-1-ReleaseNote1.0.pdf?version=1&modificationDate=1656517232831&api=v2)|RU-DEV: 01.07.22<br>RU: 01.07.22<br>TU: 05.07.22<br>PU: -|
|eRp FD 1.6.0-0|1\.6.0-0|<p>Änderungen werden mit eRp FD 1.6.0-2 ausgerollt:</p><p>- Prüfregel - authoredOn = Signaturdatum</p><p>- Prüfregel Längenprüfung PZN</p><p>- Fehlerbehebungen: </p><p>&emsp;- Signaturprüfung mit eHBA V1.0</p>|[Release Note](file:///C:/download/attachments/444109897/ERP-E-Rezept_Fachdienst_Produktversion_1.6.0-ReleaseNote1.0.pdf?version=1&modificationDate=1655979412451&api=v2)|RU-DEV: 14.06.22<br>RU: 24.06.22<br>TU: -<br>PU: -|
|eRp FD 1.5.0-2|1\.5.0-2|<p>- Konfiguration VAU-Proxy bzgl. DOS Prüfung</p><p>- Fehlerbehebung</p><p>- Security Patches</p>|[Release Note](file:///C:/download/attachments/444109897/ERP-E-Rezept_Fachdienst_Produktversion_1.5.0-2-ReleaseNote1.0.pdf?version=1&modificationDate=1657032197192&api=v2)|RU-DEV: -<br>RU: -<br>TU: -<br>PU: 12.07.22|
|eRp FD 1.5.0-1|1\.5.0-1|- BDE Upload Fix (perf\_logger) Fix |[Release Note](file:///C:/download/attachments/444109897/ERP-E-Rezept_Fachdienst_Produktversion_1.5.0-1-ReleaseNote1.0.pdf?version=1&modificationDate=1655979526775&api=v2)|RU-DEV: -<br>RU: 26.05.22<br>TU: 31.05.22<br>PU: 09.06.22|
### <a name="erezept@ru-identityprovider(idp)"></a>**Identity Provider (IdP)**

|**Label......................**|**Produkt<br>Version**|**Inhalt/Umfang**|**Zusatz-informationen**|**Deployment.....**|
| :-: | :-: | :-: | :-: | :-: |
|eRp IDP 3.0.4-6|3\.0.4-6|- Aktualisierung betrieblicher Komponenten (AccessKeeper, PairingDienst, AccessProxy, KMS, CertificateService und TLS Service).||RU: 15.03.23<br>TU: 30.03.23<br>PU: 27.04.23|
|eRp IDP 3.0.4-3|3\.0.4-3|- Update Komponenten: AccessKeeper, PairingDienst, KMS, CertificateService und TLS Service ||RU: 25.10.22<br>TU: 02.11.22<br>PU: 15.11.22|
|eRp IDP 3.0.4-2|3\.0.4-2|- Patch Komponenten: AccessKeeper, KMS und Pairing Dienst||RU: 10.10.22<br>TU: 10.10.22<br>PU: 13.10.22|
|eRp IDP 3.0.4-1|3\.0.4-1|- Upgrade Reporting-Services||RU: 27.09.22<br>TU: 04.10.22<br>PU: 11.10.22|
|eRp IDP 3.0.4-0|3\.0.4-0|<p>- Performance Erweiterungen</p><p>- Anpassung IDP Rest API</p><p>- Längenbeschränkung kk\_app\_redirect\_uri</p><p>- Library Upgrades</p><p>- Encoder Upgrades</p><p>- Upgrade TLS-Service</p><p>- Neuer Parameter für EKU optionale Prüfung</p>||RU: 23.05.22<br>TU: 07.06.22<br>PU: 30.06.22|
### <a name="erezept@ru-front-enddesversicherten(fdv)-ios"></a>**Front-End des Versicherten (FdV) - iOS**

|**Label......................**|**Produkt<br>Version**|**Inhalt/Umfang**|**Zusatz-informationen**|**Deployment.....<br>(Store)**|
| :-: | :-: | :-: | :-: | :-: |
|eRp FdV iOS 1.9.0|1\.9.0-0|<p>- Funktionale Erweiterungen (u.a. Feature Einlösen ohne Anmeldung am E-Rezept-Fachdienst, Parsen von Kostenbelegen, Änderungen in Cardwall wg. Gleichstellung Fasttrack)</p><p>- Verbesserung und Erweiterung Benutzerführung (u.a. Pflege Mobil Analytics, Aktualisierung Profilauswahl, Rezept Detailansicht, Update der Sprachen)</p><p>- Sonstiges (u.a. Verbesserung Testautomatisierung, Veränderungen im Datenmodell, Umbau Lademanagement für Discovery Dokument vom IDP)</p><p>- Fehlerbehebung (u.a. Parsen von Kostenbelegen, Senden von Fehlermeldungen durch Nutzer, UI Fehler)</p>||23\.05.23 (geplant)|
|eRp FdV iOS 1.8.0|1\.8.0-0|<p>- Verbesserung der Benutzerführung (u.a. Unterstützung für Sehbehinderte, Anzeigen bei Profilwechsel)</p><p>- Funktionale Erweiterungen (u.a. Kostenbelege PKV (aktiv erst ab 01.07.23), Anzeige Komm.-informationen bei Bestellungen in Apotheken)</p><p>- Weitere Maßnahmen im Rahmen Framework- und DB-Update / Refactoring</p><p>- Fehlerbehebung (u.a. fehlende Hinweisinformationen, Sortierung der Antworten von Apotheken, Fehler im Dark- und Demo-Modus, Stabilisierung Session-Handling)</p>||10\.05.23|
|eRp FdV iOS 1.7.0|1\.7.0-0|<p>- Verbesserung der Benutzerführung (u.a. Umstellung des Anzeigeverhaltens von Rezepten und Einnahmehinweisen, Aktualisierung der Übersetzungen, Editierung Profilnamen, Tooltips bei Erstinstallation)</p><p>- Funktionale Erweiterungen (u.a. Aktivierung Mobile Analytics, Erweiterung Medikationstypen)</p><p>- Umfangreichere Maßnahmen im Rahmen Framework Update / Refactoring</p><p>- Fehlerbehebung (u.a. Statusanzeige, Scannen von Rezepten, Behandlung eingelöster Rezepte, Benutzerführung für Sehbehinderte, Demo-Modus, Dark-Mode, Onboarding)</p>||21\.02.23|
|eRp FdV iOS 1.6.0|1\.6.0-0|<p>- Verbesserung der Benutzerführung (u.a. Nutzerleitung durch Hinweistexte; Aktualisierung von Texten)</p><p>- Hinzufügung von Medicationtypes (Rezepturen)</p><p>- Fehlerbehebung (u.a. User Interface, App-Sicherung, Demo-Modus)</p>||02\.02.23|
|eRp FdV iOS 1.5.0|1\.5.0-0|<p>- Verbesserung der Benutzerführung (u.a. Überarbeitung Kassen- und Apothekensuche, Überarbeitung UI Mainscreen)</p><p>- Fehlerbehebung (u.a. Fasttrack)</p>||11\.01.23|
|eRp FdV iOS 1.4.9|1\.4.9-0|<p>- Verbesserung der Benutzerführung (u.a. Navigation zu den Hilfeprozessen, Darstellung von Fehlermeldungen)</p><p>- Fehlerbehebung (u.a. Anzeige Rezepttyp, NFC-Fehlermeldung, VoiceOver Funktion, Anlegen Profile, Bestellung eGK, Kennwort-Eingabe)</p>||21\.11.22|
|eRp FdV iOS 1.4.8|1\.4.8-0|<p>- Funktionale Erweiterungen (u.a. Mehrfachverordnung)</p><p>- Verbesserung der Benutzerführung (u.a. Handling Apothekensuche und -favoriten)</p><p>- Fehlerbehebung (u.a. Tastatur-Fehler unter iOS16, Kennwortfunktion)</p>||14\.11.22|
|eRp FdV iOS 1.4.7|1\.4.7-0|<p>- Verbesserung der Benutzerführung und funktionale Erweiterung (u.a. Überarbeitung Apothekensuchseite, Handling Cardwall, PIN Wiederherstelfunktion)</p><p>- Fehlerbehebung (u.a. Demo-Modus (Biometrie))</p>||02\.11.22|
|eRp FdV iOS 1.4.6|1\.4.6-0|<p>- Verbesserung der Benutzerführung und funktionale Erweiterung (u.a. Suchfunktion für die eGK/PIN Bestellung, Update der KV-Kontaktliste, Handling Rufnummern)</p><p>- Fehlerbehebung (u.a. Verifikation PIN, iOS 16 Fehler)</p>||19\.11.22|
|eRp FdV iOS 1.4.5|1\.4.5-0|<p>- Verbesserung der Benutzerführung (u.a. neuer Status "In Übermittlung", Bestell-UI, Vermeidung zu langer PIN, Erweiterung Fehlermeldungen)</p><p>- Fehlerbehebung (u.a.  Vermeidung Mehrfacheingabe CAN, Refactoring der Cardwall)</p>||12\.10.22|
|eRp FdV iOS 1.4.4|1\.4.4-0|<p>- Funktionale Erweiterungen (u.a. neue Apotheken-Suchliste)</p><p>- Update der Versicherungsliste</p><p>- Fehlerbehebung (u.a.  CAN Eingabe in der Cardwall, Fehler bei Migrationen von Vorversionen, Link Youtube, Biometrie (Login und Bestätigung, Fehlermeldungen beim Löschen)</p>||21\.09.22|
|eRp FdV iOS 1.4.3|1\.4.3-0|<p>- Funktionale Erweiterungen (Direktzuweisung 169, Vorbereitung MVO, Teilung von Rezepten, Entsperrung eGK mit PUK)</p><p>- Verbesserung der Benutzerführung (u.a. Refactoring der Cardwall UI, Copyright Informationen, Vorbereitung Mitteilungen zu Bestellen-Screen)</p><p>- Fehlerbehebung (u.a. Demo-Mode, Cardwall-Navigation (CanViews, CardWallPinView und CardWallLoginOptionView), CAN Voiceover)</p>||13\.09.22|
|eRp FdV iOS 1.4.2|1\.4.2-0|<p>- Erweiterung Sprachen (Ukrainisch, Arabisch, Polnisch und Russisch)</p><p>- Verbesserung der Benutzerführung (u.a. Kameralicht, Hilfen für NFC)</p>||22\.08.22|
|eRp FdV iOS 1.4.0|1\.4.0-0|<p>- Funktionale Erweiterungen (Familienfunktion (zusätzliche Profile für Angehörige), Handling der Authentifizierung, CAN Scanner in der Cardwall, Ausbau Testautomatisierung)</p><p>- Alternative Zuweisung (nur RU)</p><p>- Fehlerbehebung (u.a. GUI, Kontaktliste für eGK/PIN Bestellungen)</p>||27\.07.22|
|eRp FdV iOS 1.3.3|1\.3.3-0|<p>- Verbesserung der Benutzerführung (u.a. Handling CAN in Cardwall, Hinterlegung, individuelle BIlder, Anzeige gelöschter Zugriffstoken, Positionierung NFC-Karte, keine Einlöse-Button ohne Rezept)</p><p>- DevOps-Aspekte (techn. Dokumentation, Umbau CI-Pipeline, Handling Lieferung der Desktop-App, Handling Releases)</p><p>- Fehlerbehebung (u.a. bei Rezept-Download, Cache-Hanling, Formate und Farben) </p>||15\.07.22|
|eRp FdV iOS 1.3.2|1\.3.2-0|<p>- Überarbeitung der Benutzerführung (u.a. Onboarding, Info bei NFC- und Biometrie-Fehler)</p><p>- Behebung von Fehlern (u.a. Zertifikatspinning, Aktualisierung Status Rezept, Filterung/Anzeige von Apotheken, Anzeige von eGK, Verhalten der Cardwall nach Abbruch Kartenkommunikation, Fehler aus Regressionstest)</p>|[github](https://gematik.github.io/E-Rezept-App-iOS/errors/error_graph.html "https://gematik.github.io/e-rezept-app-ios/errors/error_graph.html")|27\.06.22|
|eRp FdV iOS 1.3.1|1\.3.1-0|<p>- Alternative Zuweisung</p><p>- Erweiterung Debug-Version</p><p>- Update Kontaktliste für Kassen</p><p>- Behebung von Fehlern (Pageination von Protokolleinträgen, Auswahl Textfeld, Management von Profilen)</p>||06\.06.22|
|eRp FdV iOS 1.3.0|1\.3.0-0|<p>- Anmelden am Fachdienst via Kassen-App (Fasttrack-Verfahren)</p><p>- Erweiterung Nutzerkommunikation (Response an gematik bei NFC-Fehler; Kennwort-Handling)</p><p>- Codepflege (Parser)</p><p>- Behebung von Fehlern (Nutzung durch sehbehinderte Personen, Anzeige von Buttons, Korrektur URL Apotheke, Löschung von Rezepten, GUI)</p>||31\.05.22|
|eRp FdV iOS 1.2.7|1\.2.7-0|<p>- Erweiterte Lieferinformationen (alternative Lieferadresse, Kontaktadresse)</p><p>- Verbesserung Transparenz und Robustheit</p><p>- Behebung von Fehlern (u.a. Anzeigetexte, Handling eGK im Demo-Modus))</p>||03\.05.22|
### <a name="erezept@ru-front-enddesversicherten(fdv)-androidundharmony"></a>**Front-End des Versicherten (FdV) - Android und Harmony**

|**Label......................**|**Produkt<br>Version**|**Inhalt/Umfang**|**Zusatz-informationen**|**Deployment.....<br>(Store)**|
| :-: | :-: | :-: | :-: | :-: |
|eRp FdV Android und Harmony 1.11.0|1\.11.0-0|<p>- Funktionale Erweiterungen (u.a. Feature Einlösen ohne Anmeldung am E-Rezept-Fachdienst, Update NFC-Positionierung)</p><p>- Verbesserung und Erweiterung Benutzerführung (u.a. Pflege Mobil Analytics, Anpassung Wunsch-PIN)</p><p>- Sonstiges (u.a. Update für Testautomatisierung)</p><p>- Fehlerbehebung (u.a. keine Verwendung API Key für Zuweisung, Anzeige von verfügbaren Services, Reihenfolge von Rezepten, Anzeige von Rezepturen und Wirkstoffen, Sichtbarkeit Anmelde-Button, FAQ Link, Fehlermeldung bei Refresh)</p>||24\.05.23 (geplant)|
|eRp FdV Android und Harmony 1.10.0|1\.10.0-0|<p>- Funktionale Erweiterungen (u.a. Feature PKV (nicht in PU erreichbar), Parser für Zertifikate, Vorbereitung für Zuweisen ohne Anmeldung am Fachdienst)</p><p>- Verbesserung und Erweiterung Benutzerführung (u.a. Änderung der eGK Bestellfunktion und Kontaktdaten der Kasse, Anzeige Kostenbelege PKV (nicht in PU erreichbar))</p><p>- Sonstiges (u.a. Umbenennung Krankenkasse, Refactoring ViewModel Authentifizierung)</p><p>- Fehlerbehebung (u.a. Testkonstellationen, FHIR Parser, PIN Änderung)</p>||06\.04.23|
|eRp FdV Android und Harmony 1.8.0|1\.8.0-0|<p>- Verbesserung und Erweiterung Benutzerführung (u.a. Apothekensuche, Onboarding, Bestellprozess, Aktivierung Mobile Analytics, Optimierung Mehrsprachigkeit, Tooltips für Sehbehinderte, neue Datenschutzerklärung)</p><p>- Fehlerbehebung (u.a. Bezeichnung Rezeptur, Handling Stammdaten, Stornierung Rezept)</p>||03\.03.23|
|eRp FdV Android und Harmony 1.7.0|1\.7.0-0|<p>- Verbesserung und Erweiterung Benutzerführung (u.a. eGK Bestellung, UI Onboarding Screen)</p><p>- Fehlerbehebung (u.a. UI, Rezeptliste, Einlöseprozess, Medication Dispense)</p>||24\.01.23|
|eRp FdV Android und Harmony 1.6.1|1\.6.1-0|<p>- Verbesserung und Erweiterung Benutzerführung (u.a. Rezeptdetails mit Anzeige Notdienst, App-Sperre nach 10 sec (alt: 30 sec))</p><p>- Fehlerbehebung (u.a. Anzeige von Keyboards)</p>||22\.12.22|
|eRp FdV Android und Harmony 1.5.0|1\.5.0-0|<p>- Verbesserung und Erweiterung Benutzerführung (u.a. Tooltipps, Aktualisierung Krankenkassenliste)</p><p>- Fehlerbehebung (u.a. Berechnung Gültigkeiten, Darstellung der Notdienstgebühr)</p>||09\.12.22|
|eRp FdV Android und Harmony 1.4.9|1\.4.9-0|<p>- Verbesserung und Erweiterung Benutzerführung (u.a. Einbindung von Übersetzungen, Kartenansicht für Apotheken, Aktualisierung GUI Startbildschirm, Anpassung bei Kontaktdaten der KV)</p><p>- Fehlerbehebung (u.a. Datum in den Rezeptdetails, Positionierung Hintergrundbild, GUI Fehler in Cardwall)</p>||26\.11.22|
|eRp FdV Android und Harmony 1.4.7|1\.4.7-0|<p>- Verbesserung und Erweiterung Benutzerführung (u.a. Informationen über die NFC-Verfügbarkeit, Handling Internetverbindung, URL Umfrage)</p><p>- Funktionale Erweiterungen (u.a. obligatorisches Update)</p><p>- Fehlerbehebung (u.a. Darstellung von Freitext/Wirkstoff, Sortierung Rezepte, Sichtbarkeit Tastatur)</p>||07\.11.22|
|eRp FdV Android und Harmony 1.4.6|1\.4.6-0|<p>- Verbesserung und Erweiterung Benutzerführung (u.a. Warnung bei Ablaufen eines Rezeptes, Schnellauswahlliste für Apotheken, Umbau der Apothekensuchseite, Kennworthinweise, Optimierungen UI und Geräteidentitätserstellung der Cardwall, Umbau Wunsch-PIN Funktion, eigener FHIR Parser, Erweiterung der Mini-Cardwall)</p><p>- Fehlerbehebung (u.a. Hinweis auf Zuzahlung, Anzeige Rezept-Status, UI-Fehler u.a. Cardwall, PIN Eingabe, Scanning bei Direktzuweisung und Rezepten, PIN Eingabe, Fehlermeldungen, Fehlertolleranz im FHIR Parser)</p>||14\.10.22|
|eRp FdV Android und Harmony 1.4.4|1\.4.4-0|<p>- Funktionale Erweiterungen (u.a. Unterstützung Rezepttyp 169 Direktzuweisung, Unterstützung Mehrfachverordnungen, Deaktivierung Teilen von Rezepten, Parsen von Nachrichten aus der Apotheke)</p><p>- Verbesserung und Erweiterung Benutzerführung (u.a. UI-Optimierungen Menüs, Bewertung/Feedback, UI Refactoring Rezept-Detailseiten, Anhaltehilfe für NFC Karte)</p><p>- Betrieblich (u.a. Update API-Keys)</p><p>- Fehlerbehebung (u.a. Screensizes CAN, Eingabeschrift bei Namensänderungen im Profil, hinzufügen von Rezepten via Kamera, UI Darstellungsfehler in der Cardwall)</p>||05\.10.22|
|eRp FdV Android und Harmony 1.4.3|1\.4.3-0|<p>- Funktionale Erweiterungen (u.a. Teilung von Rezepten)</p><p>- Verbesserung Benutzerführung (u.a. Handling von Mitteilungen)</p><p>- Codepflege</p>||14\.09.22|
|eRp FdV Android und Harmony 1.4.1|1\.4.1-0|<p>- Verbesserung und Erweiterung Benutzerführung (u.a. Sichtbarkeit von Buttons, Anzeige der Apotheken, Bestellübersicht, Profilseite und Kontaktinformationen)</p><p>- Behebung von Fehlern (u.a. Institutionsname)</p>||24\.08.22|
|eRp FdV Android und Harmony 1.4.0|1\.4.0-0|<p>- Familienfunktion inkl. Steuerung</p><p>- Wartungsarbeiten (u.a. CI, Codepflege</p><p>- Behebung von Fehlern (u.a. UI, Entsperren eGK, Handling Access-Token))</p>||22\.07.22|
|eRp FdV Android und Harmony 1.3.0|1\.3.0-0|<p>- Verbesserung und Update der Sicherheitsfunktionen (Handling eGK Sperre, PIN und NFC; neue API-Keys und User-Agents)</p><p>- Anmelden am Fachdienst via Kassen-App (Fasttrack-Verfahren)</p><p>- Überarbeitung und Pflege Benutzerführung für (u.a. Cardwall (u.a. PIN-, CAN-Screen), Fehlerhandling, Lese-Modus, Dokumentation, Gültigkeitsangabe von Rezepten)</p><p>- Refactoring Parser (FHIR, UX), Code und Fehler-Handling</p><p>- Erweiterung Konny-App um RU-DEV</p><p>- Umstellung App-Signing auf Plugin + Cert</p><p>- Behebung von Fehlern (u.a. Handling SSO-Token, Profil-Management, User-Interface (Anzeigen, Texte und Fehler-Infos), App-Abstürze bei Nutzungsbedingungen und bestimmten Endgeräten, Dark Mode, Cardwall-Refresh)</p>||01\.06.22|
### <a name="erezept@ru-anwendungdesversicherten(adv)"></a>**Anwendung des Versicherten (AdV)**

|**Label......................**|**Produkt<br>Version**|**Inhalt/Umfang**|**Zusatz-informationen**|**Deployment.....<br>(Store)**|
| :-: | :-: | :-: | :-: | :-: |
|eRp AdV Windows 1.2.4|1\.2.4-0|- ...||17\.03.23|
|eRp AdV Windows 1.0.1|1\.2.1-0|<p>- Behoben werden zwei Fehler bei der Anzeige von Protokollierungen</p><p>- API-Interface</p>||04\.02.22|
### <a name="erezept@ru-apotheken-verzeichnisdienst(apovzd)"></a>**Apotheken-Verzeichnisdienst (APOVZD)**

|**Label......................**|**Produkt<br>Version**|**Inhalt/Umfang**|**Zusatz-informationen**|**Deployment.....**|
| :-: | :-: | :-: | :-: | :-: |
|eRp APOVZD 1.3.0-1|1\.3.0-1|<p>Änderungen:</p><p>- Betrieblich (Verbesserung URL Sync, um Hinzufügen/Entfernen des Botendienstes über das Apothekenportal zu gewährleisten; Verbesserung Hinzufügen/Entfernen von URLs für die drei verschiedenen Belieferungsoptionen über die Apothekenverwaltungssysteme)</p>|[Release Notes](file:///C:/download/attachments/444109897/ReleaseNotes%20ApoVZD%201-3-0-1.pdf?version=1&modificationDate=1684744535132&api=v2)|RU: 04.05.23<br>PU: 26.05.23|
|eRp APOVZD 1.3.0-0|1\.3.0-0|<p>Änderungen:</p><p>- Stufe #A Erweiterung Schnittstelle ApoVZ zu FdV</p><p>- Stufe #B Einpflegbarkeit von Testdaten (über Austausch Json-Daten)</p><p>- Stufe #C Erweiterung der Pflegeschnittstellen</p><p>- Stufe #D Synchronisation Verschlüsselungszertifikate VZD</p>|[Release Notes](file:///C:/download/attachments/444109897/ReleaseNotes%20ApoVZD%201-3-0.pdf?version=2&modificationDate=1684744577277&api=v2)|RU: 06.04.23 <br>PU: -|
### <a name="erezept@ru-nutzungsplan-test"></a>**Nutzungsplan - Test**
TEST! Keine realen Daten!


Team Calendars Team-Kalender
