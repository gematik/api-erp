import unicodedata
import re

class CheckResult(object):
    def __init__(self,

        success: bool,
        reason: str,
        details: str
                ):

            self.success = success
            self.reason= reason
            self.details = details

    def __str__(self):
        result_string = "❌ Names NOT compareable"
        if self.success:
            result_string = "✅ Names are compareable"

        return "{0}, Reason: {1} {4}Details:{2}{3}".format(result_string, self.reason, self.details, draw_line(2), draw_line(1))

class Name(object):
    def __init__(self,
        given: str,
        family: str):
            self.original_given = given
            self.original_family = family
            self.given = given
            self.family = family

    def __str__(self):
        return "\r\n  Vorname:  '{0}'\r\n  Nachname: '{1}'".format(self.given, self.family)

    def original(self):
        return "\r\n  Vorname:  '{0}'\r\n  Nachname: '{1}'".format(self.original_given, self.original_family)

def draw_line(mode: int):
    if mode == 1:
        return "\r\n---------------------------------------------------------------------------------------------\r\n";
    else:
        return "\r\n=============================================================================================\r\n";

def standardize_name(name: Name) -> Name:
    name.given = normalize_text_and_to_lower(name.given,'NFD')
    name.family = normalize_text_and_to_lower(name.family,'NFD')
    name.given = removeSpacesAroundHyphen(name.given)

    return name

def normalize_text_and_to_lower(text:str, normalform: str) -> str:
    normalized_string = ''.join(c for c in unicodedata.normalize(normalform, text)
                  if unicodedata.category(c) != 'Mn')
    to_lower_and_normalized = normalized_string.lower()
    return to_lower_and_normalized

def removeSpacesAroundHyphen(text:str):
    replaced = re.sub(r'\s*-\s*', '-', text)
    return replaced

def slice_string(text:str, char_number: int) -> str:
    return text[0:char_number]

def check_equal(name_in: str, name_out:str):
    if name_in == name_out:
        return True
    return False

def check_exist_single_out_given_name_in_given_names(qes_name: str, verschreibender_name: str) -> bool:
    qes_names = qes_name.split(' ')
    verschreibender_names = verschreibender_name.split(' ')
    for verschreibender_name in verschreibender_names:
        if verschreibender_name in qes_names:
            return True

    return False

def make_abbreviation(name: str):
    hyphen_chars = ["-","‐","‑","–","—"]
    if any(c in hyphen_chars for c in name):
        names = re.split(r'[' + ''.join(hyphen_chars) + ']+', name)
        abbr = []
        for n in names:
            abbr.append(slice_string(n, 1) + ".")
        return '-'.join(abbr)
    else:
        return slice_string(name, 1) + "."

def get_name_origin(verschreibender_name:str , qes_names_left) -> str:
    if verschreibender_name in qes_names_left:
        return verschreibender_name

    for qes_name in qes_names_left:
        if make_abbreviation(qes_name) == verschreibender_name:
            return qes_name


def every_given_name_has_valid_origin(qes_name: str, verschreibender_name: str) -> bool:
    qes_names_left = qes_name.split(' ')
    verschreibender_names = verschreibender_name.split(' ')
    for out_given_name in verschreibender_names:
        name_origin = get_name_origin(out_given_name, qes_names_left)
        if name_origin:
            qes_names_left.remove(name_origin)
        else:
            return False

    return True

def test_name(test_number: int, test_case: str, qes_name: Name, verschreibender_name: Name, test_assertion: bool):
    check_results = check_name(qes_name, verschreibender_name)
    test_result = "failed ❌"
    namensvergleich_result = "gescheitert"

    if len(check_results) != 0:
        if  check_results[0].success == test_assertion:
            test_result = "was successfull ✅"
        if check_results[0].success == True:
            namensvergleich_result = "erfolgreich"

        print("{0}. Test '{1}' {2}{3}Ergebnis: Namensvergleich {6}{3}Tested:\r\n QES: {4}\r\n FHIR: {5}{3}".format(test_number, test_case, test_result,draw_line(1),qes_name.original(), verschreibender_name.original(),namensvergleich_result))
        if check_results[0].success == True:
            print(check_results[0].reason)
        else:
            print("Warning(s)\Error(s):")
            for check_result in check_results:
                print("{0} Details: {1}".format(check_result.reason, check_result.details))
        print(draw_line(0))
    else:
        print("ERROR: found {0} issues".format(len(check_results)))




def check_name(qes_name: Name, verschreibender_name: Name):
    #standardize names
    qes_name_simple = standardize_name(qes_name)
    verschreibender_name_simple = standardize_name(verschreibender_name)

    #check family names
    qes_name.family = slice_string(qes_name.family, 45)
    check_results = []

    if not check_equal(qes_name_simple.family, verschreibender_name_simple.family):
        check_results.append(CheckResult(False, "Namensungleichheit bei den Nachnamen festgestellt.", "\r\n {0} != {1}".format(qes_name_simple.family, verschreibender_name_simple.family)))

    #check given name
    if not check_exist_single_out_given_name_in_given_names(qes_name_simple.given, verschreibender_name_simple.given):
        check_results.append(CheckResult(False, "Fehlen eines ungekürzten Zertifikats-Vornamens in den Practitioner Vornamen festgestellt.", "\r\n {0} != {1}".format(qes_name_simple.given, verschreibender_name_simple.given)))

    if not every_given_name_has_valid_origin(qes_name_simple.given, verschreibender_name_simple.given):
        check_results.append(CheckResult(False, "Ein zusätzliches Element ohne erkennbaren Ursprung wurde in den Verschreibender-Vornamen festgestellt.", "\r\n {0} != {1}".format(qes_name_simple.given, verschreibender_name_simple.given)))

    if len(check_results) == 0:
        check_results.append(CheckResult(True, "Namen sind nach den Vorgaben vergleichbar.", "\r\n QES: {0} \r\n FHIR: {1}".format(qes_name, verschreibender_name)))

    return check_results

if __name__ == '__main__':
    test_name(1, 'Equal Strings', Name('Hans-Georg Michael Sebastian von','von Holz auf der Heide'), Name('Hans-Georg Michael Sebastian von','von Holz auf der Heide'), True)
    test_name(2, 'Different family names', Name('Hans-Georg Michael Sebastian','von Holz auf der Heide'), Name('Hans-Georg Michael Sebastian','Holz auf der Heide'), False)
    test_name(3, 'Lowercase and Uppercase', Name('GEORG','HOTZ'), Name('Georg','Hotz'), True)
    test_name(4, 'Special Characters', Name('Jeßica','Weißhäschen'), Name('Jeßica','Weißhäschen'), True)
    test_name(41, 'Special Characters', Name('Jeßica','Weißhäschen'), Name('Jessica','Weisshaeschen'), False)
    test_name(5, 'Special Characters', Name('Marušić','Kovač'), Name('Marusic','Kovac'), True)
    test_name(6, 'Different special characters', Name('Marušić','Kovač'), Name('Marusic','Kovać'), True)
    test_name(7, 'Given not present', Name('Michael','Jackson'), Name('','Jackson'), False)
    test_name(8, 'Multiple given names used', Name('Michael','Jackson'), Name('Michael Michael','Jackson'), False)
    test_name(9, 'Multiple given abbreviation and names used', Name('Michael','Jackson'), Name('Michael M.','Jackson'), False)
    test_name(10, 'additional given names used', Name('Michael','Jackson'), Name('Michael Peter','Jackson'), False)
    test_name(11, 'only abbreviation used', Name('Michael','Jackson'), Name('M.','Jackson'), False)
    test_name(12, 'Correct abbreviation', Name('Michael Peter','Jackson'), Name('M. Peter','Jackson'), True)
    test_name(13, 'Correct abbreviation 2', Name('Michael Peter','Jackson'), Name('Michael P.','Jackson'), True)
    test_name(14, 'abbreviation in QES', Name('Michael P.','Jackson'), Name('P.','Jackson'), True)
    test_name(15, 'overlong familyname shortend', Name('Franz Anselm Hamann Philipp','Graf von Ingelheim genannt Echter von und zu Mespelbrunn'), Name('Franz Anselm Hamann Philipp','Graf von Ingelheim genannt Echter von und zu '), True)
    test_name(16, 'overlong familyname not shortend', Name('Sebastian','von OttovordemgentschenfeldeOttovordemgentschenfelde-Memmingen'), Name('Sebastian','von OttovordemgentschenfeldeOttovordemgentschenfelde-Memmingen'), False)
    test_name(17, 'abbreviation of given names with -', Name('Hans-Georg Martin','Schleicher'), Name('H.-G. Martin','Schleicher'), True)
    test_name(18, 'wrong abbreviation of given names with -', Name('Hans-Georg Martin','Schleicher'), Name('H. Martin','Schleicher'), False)
    test_name(19, 'new ordering of given names', Name('Alexa Friederike Barbara','Baronesse von Schmargen gen. Karst'), Name('Barbara Friederike Alexa','Baronesse von Schmargen gen. Karst'), True)
    test_name(20, 'control character fail', Name('Anna/', 'Högström-Schurig-Freif. v. Schrenck v. Notzing'), Name('Anna', 'Högström-Schurig-Freif. v. Schrenck v. Notzin'), False)
    test_name(21, 'control character success', Name('Anna/', 'Högström-Schurig-Freif. v. Schrenck v. Notzing'), Name('Anna/', 'Högström-Schurig-Freif. v. Schrenck v. Notzin'), True)
    test_name(22, 'Special hyphen usage', Name('Anna-Luise‐Susie‑Stella–Rosie—Bella', 'Meier'), Name('Anna-Luise‐Susie‑Stella–Rosie—Bella', 'Meier'), True)
    test_name(23, 'Abbreviation with special hyphen usage', Name('Sophie Anna-Luise‐Susie‑Stella–Rosie—Bella', 'Meier'), Name('Sophie A.-L.-S.-S.-R.-B.', 'Meier'), True)
    test_name(24, 'Abbreviation rebuilding with wrong hyphen', Name('Sophie Anna-Luise‐Susie‑Stella–Rosie—Bella', 'Meier'), Name('Sophie A.‐L.‐S.‐S.‐R.‐B.', 'Meier'), False)
    test_name(25, 'Multiple Errors', Name('Sophie Anna-Luise‐Susie‑Stella–Rosie—Bella', 'Meier'), Name('Reiner', 'Müller'), False)
    test_name(26, 'less FHIR given names', Name('Hans-Georg Martin','Schleicher'), Name('Martin','Schleicher'), True)
    test_name(27, 'less FHIR given names 2', Name('Georg Martin','Schleicher'), Name('Martin','Schleicher'), True)
    test_name(28, 'wrong abbreviation of given names with -', Name('Hans-Georg Martin','Schleicher'), Name('Hans-G. Martin','Schleicher'), False)
    test_name(29, 'wrong abbreviation of given names with - 2', Name('Hans-Georg Martin','Schleicher'), Name('H.-Georg Martin','Schleicher'), False)
    test_name(30, 'leading Space before hyphen', Name('Hans -Georg Martin','Schleicher'), Name('Hans-Georg','Schleicher'), True)
    test_name(31, 'tailing Space after hyphen', Name('Hans- Georg Martin','Schleicher'), Name('Hans-Georg','Schleicher'), True)
    test_name(32, 'tailing Space around hyphen', Name('Hans - Georg Martin','Schleicher'), Name('Hans-Georg','Schleicher'), True)
    test_name(33, 'leading Space before hyphen', Name('Hans -Georg Martin','Schleicher'), Name('Hans -Georg','Schleicher'), True)
    test_name(34, 'tailing Space after hyphen', Name('Hans- Georg Martin','Schleicher'), Name('Hans- Georg','Schleicher'), True)
    test_name(35, 'tailing Space around hyphen', Name('Hans - Georg Martin','Schleicher'), Name('Hans - Georg','Schleicher'), True)