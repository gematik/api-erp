# Methodik

Um Änderungen der FHIR Ressourcen nach Versionsübergängen zu ermitteln
und zu visualisieren, bietet der HAPI Validator eine hilfreiche
Funktionalität. [Der Hapi Validator kann Profile miteinander
vergleichen](https://confluence.hl7.org/pages/viewpage.action?pageId=35718580#UsingtheFHIRValidator-ComparingProfiles).

Bis zur Version 5.6.88 ist die Vergleichsfunktion
[fehlerhaft](https://github.com/hapifhir/org.hl7.fhir.core/issues/1040).
Ab Version 5.6.89 kann diese wie folgt benutzt werden:

    java -jar validator_cli.jar -compare -dest compare_results -version 4.0.1 \
    -ig de.gematik.erezept-workflow.r4#1.2.1 \
    -ig de.gematik.erezept-workflow.r4#1.1.1 \
    -left https://gematik.de/fhir/StructureDefinition/ErxTask|1.1.1 \
    -right https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_PR_Task|1.2.1

Das Ergebnis eines solchen Abgleichs ist ein Ordner mit vielen
(Bild-)dateien und einer index.html die als Einstiegspunkt für den
erfolgten Vergleiche dient. Darüber hinaus enthalten die Verzeichnisse
die *union*- und *intersection*-FHIR Strukturen die für eine
vereinfachte Integration verwendet werden können.

Die CompareFunktion kann nur für Definitionen von Profilen und
Extensions aufgerufen werden. *OperationDefinition*,
*CodeSystem*,*NamingSystem* und *ValueSet’werden nicht direkt
miteinander verglichen. Wenn Profile oder Extensions
'OperationDefinition*, *CodeSystem*,*NamingSystem* oder *ValueSet*
beinhalten, werden diese aber indirekt verglichen.

Da durch Änderung der Canonicals die Profilnamen (wie im obigen
Beispiel) nicht immer identisch geblieben sind, ist ein automatisierter
Aufruf der Vergleichsfunktionalität nicht ohne weiteres möglich. Um das
problem zu lösen können "Transitionfiles" verwendet werden.

# Transitionfiles

Um die Umbenennung von Profilen oder deren Umlagerung in neue Profile
festzuhalten wurden "Transitionfiles" erstellt, diese geben Auskunft
über

-   Abhängigkeiten die für den Vergleich der Profile notwendig sind

-   Neue Profile seit dem Versionsübergang

-   Ausgeschiedene Profile mit dem Versionsübergang

-   Profiländerungen mit den Versionsübergang

## Download Transitionfiles

-   [transitionfile\_kbv.ita.erp\_v1.0.2\_to\_v1.1.1.json](#./resources/transitionfiles/transitionfile_kbv.ita.erp_v1.0.2_to_v1.1.1.json)

-   [transitionfile\_de.gematik.erezept-workflow.r4\_v1.1.1\_to\_v1.2.1.json](#./resources/transitionfiles/transitionfile_de.gematik.erezept-workflow.r4_v1.1.1_to_v1.2.1.json)

-   [transitionfile\_de.abda.eRezeptAbgabedatenBasis\_v1.2.1\_to\_v1.3.0.json](#./resources/transitionfiles/transitionfile_de.abda.eRezeptAbgabedatenBasis_v1.2.1_to_v1.3.0.json)

-   [transitionfile\_de.gkvsv.eRezeptAbrechnungsdaten\_v1.2.0\_to\_v1.3.0.json](#./resources/transitionfiles/transitionfile_de.gkvsv.eRezeptAbrechnungsdaten_v1.2.0_to_v1.3.0.json)

# Generierte Vergleichs Ergebnisse

Die Artefakte der jeweils abhängigen Pakete wurden nicht erzeugt und
werden hier nicht zur Verfügung gestellt. Diese Abhängigkeiten können
auf Simplifier unter dem Tab "Dependencies" eingesehen werden. Zum
Beispiel können Sie die Abhängigkeiten des E-Rezept-Workflows Paketes
unter <https://simplifier.net/erezept-workflow/~dependencies> einsehen.
Für Änderungen innerhalb der Abhängigkeiten empfehlen wir Ihnen, die
Releasenotes der Pakete zu analysieren. Beispielsweise finden Sie eine
Liste der Releasenotes für das Paket "de.basisprofil.r4" in Version
1.3.2 unter <https://simplifier.net/packages/de.basisprofil.r4/1.3.2>.

Die Ergebnisse des Abgleichs der betroffenen Pakete (ohne deren direkte
und indirekte Abhängigkeiten) können hier eingesehen werden:

-   [de.abda.eRezeptAbgabedaten](https://htmlpreview.github.io/?https://github.com/gematik/api-erp/blob/master/docs/resources/compare_results/de.abda.eRezeptAbgabedaten/index.html)

-   [de.abda.eRezeptAbgabedatenBasis](https://htmlpreview.github.io/?https://github.com/gematik/api-erp/blob/master/docs/resources/compare_results/de.abda.eRezeptAbgabedatenBasis/index.html)

-   [de.basisprofil.r4](https://htmlpreview.github.io/?https://github.com/gematik/api-erp/blob/master/docs/resources/compare_results/de.basisprofil.r4/index.html)

-   [de.gematik.erezept-patientenrechnung.r4](https://htmlpreview.github.io/?https://github.com/gematik/api-erp/blob/master/docs/resources/compare_results/de.gematik.erezept-patientenrechnung.r4/index.html)

-   [de.gematik.erezept-workflow.r4](https://htmlpreview.github.io/?https://github.com/gematik/api-erp/blob/master/docs/resources/compare_results/de.gematik.erezept-workflow.r4/index.html)

-   [de.gkvsv.erezeptabrechnungsdaten](https://htmlpreview.github.io/?https://github.com/gematik/api-erp/blob/master/docs/resources/compare_results/de.gkvsv.erezeptabrechnungsdaten/index.html)

-   [kbv.ita.erp](https://htmlpreview.github.io/?https://github.com/gematik/api-erp/blob/feature/update_compress-results/docs/resources/compare_results/kbv.ita.erp/index.html)

-   [kbv.ita.for](https://htmlpreview.github.io/?https://github.com/gematik/api-erp/blob/master/docs/resources/compare_results/kbv.ita.for/index.html)

Die html-Dateien können auch als [komprimiertes Verzeichnis
heruntergeladen](#./resources/compare_results.zip) werden und lokal im
Browser betrachtet werden.
