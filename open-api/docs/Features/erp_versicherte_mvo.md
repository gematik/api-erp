Hier dokumentiert die gematik die Nutzung der Schnittstellen rund um das
E-Rezept aus Sicht der Versicherten, die ihre E-Rezepte verwalten und
einlösen möchten.

Mehrfachverordnungen sollen die Versorgung mit Arzneimittel für
chronisch Kranke erleichtern. Für Versicherte, die eine kontinuierliche
Versorgung mit einem bestimmten Arzneimittel benötigen, können
Vertragsärzte Verordnungen ausstellen, nach denen eine nach der
Erstabgabe bis zu dreimal sich wiederholende Abgabe erlaubt ist.

Aus der Mehrfachverordnung ergeben sich Vorteile für Patienten und die
Abläufe in Arztpraxen, da die Rezepte für Dauermedikationen im Voraus
ausgestellt werden können und somit Wege zur Arztpraxis zum Rezepte
abholen entfallen.

# Fachliches Konzept

Eine Mehrfachverordnung besteht aus mindestens 2 bis maximal 4
Teilverordnungen. Jede Teilverordnung einer Mehrfachverordnung ist ein
vollständiges E-Rezept mit eigenem E-Rezept-Token. Das bedeutet, dass
jede der Teilverordnungen durch den eigenen E-Rezept-Token auch einzeln
durch den Versicherten, ggf. in verschiedenen Apotheken, eingelöst
werden kann.

Der Arzt/Zahnarzt kann das Ende der Gültigkeitszeitraumes einer
Teilverordnung festlegen. Falls das Ende nicht festgelegt wird, dann
gilt die Teilverordnung bis 365 Tage nach dem Ausstellungsdatum der
Mehrfachverordnung. Die folgende Abbildung zeigt eine mögliche Variante
für die Gültigkeitszeiträume zweier Teilverordnungen einer
Mehrfachverordnung.

![width=100%](../images/api_mvo_gueltigkeit.png)

# Datenmodell der Mehrfachverordnung

Eine Mehrfachverordnung besteht aus 2 bis max. 4 unabhängigen
Teilverordnungen. Jede Teilverordnung ist ein (zahn)ärztlich signiertes
E-Rezept gemäß der [KBV-Festlegungen^](https://simplifier.net/erezept)
für einen Verordnungsdatensatz.

Beispieldatensätze finden sich im Unterverzeichnis
[samples/MVO\_KBV\_1.0.2\_.zip](../samples/MVO_KBV_1.0.2_.zip)

Die folgenden Felder sind dabei charakteristisch für die
Teilverordnungen einer Mehrfachverordnung

## Kennzeichen einer Verordnung als Teilverordnung einer Mehrfachverordnung

Wenn im Verordnungsdatensatz das Flag
MedicationRequest.extension:Mehrfachverordnung.extension:Kennzeichen =
true gesetzt ist, dann ist dieses E-Rezept eine Teilverordnung einer
Mehrfachverordnung.

    MedicationRequest.extension:Mehrfachverordnung.extension:Kennzeichen = true

## Nummer des Rezepts der Mehrfachverordnung ("Zähler")

    MedicationRequest.extension:Mehrfachverordnung.extension:Nummerierung.value[x]:valueRatio.numerator

## Gesamtzahl der Teilverordnungen in der Mehrfachverordnung ("Nenner")

    MedicationRequest.extension:Mehrfachverordnung.extension:Nummerierung.value[x]:valueRatio.denominator

## Start der Gültigkeit

Die Teilverordnungen von Mehrfachverordnungen haben einen
Gültigkeitszeitraum. Der Beginn des Gültigkeitszeitraumes ist in
MedicationRequest.extension:Mehrfachverordnung.extension:Zeitraum.value\[x\]:valuePeriod.start
angegeben.

    MedicationRequest.extension:Mehrfachverordnung.extension:Zeitraum.value[x]:valuePeriod.start

## Ende der Gültigkeit

Der Verordnende kann im Verordnungsdatensatz ein Ende des
Gültigkeitszeitraumes angeben
(MedicationRequest.extension:Mehrfachverordnung.extension:Zeitraum.value\[x\]:valuePeriod.end).
Wenn kein explizites Ende des Gültigkeitszeitraumes angegeben ist, dann
endet der Gültigkeitszeitraum 365 Tage nach Ausstellen der
Teilverordnung. Der E-Rezept-Fachdienst berechnet den Wert für
Task.extension:expiryDate entsprechend.

Wird der Gültigkeitszeitraum überschritten darf das E-Rezept nicht mehr
eingelöst werden.

    MedicationRequest.extension:Mehrfachverordnung.extension:Zeitraum.value[x]:valuePeriod.end

Eine Teilverordnung kann zu Lastern der GKV abgerechnet werden, wenn es
innerhalb des Gültigkeitszeitraums eingelöst wird. D.h. ein Einlösen als
Selbstzahler entfällt bzw, gibt es bei Teilverordnungen einer MVO nicht.

Eine Reihenfolge der Abgabe der einzelnen Teilverordnungen einer MVO ist
bei Abgabe nicht zu beachten.

Patienten haben zu jeder Zeit die Möglichkeit, alle Teilverordnungen
einer Mehrfachverordnung über die E-Rezept-App einzusehen und die
Einlöseinformationen als Datamatrix oder Zuweisung an Apotheken zu
teilen (und bei Bedarf zu löschen).

Apotheken sind VOR dem Gültigkeitsbeginn `valuePeriod.start` nicht
berechtigt, eine Teilverordnung herunterzuladen.

Durch einen Bug im Fachdienst wird derzeit das Ende der Gültigkeitsdauer
bei $accept nicht überprüft. Dadurch kann es sein, dass eine MVO vom
Fachdienst zurückgegeben wird, die nicht mehr gültig ist. Dies muss im
AVS geprüft werden.

Die Angabe der Gültigkeit muss im Format "yyyy-mm-dd" angegeben werden.
