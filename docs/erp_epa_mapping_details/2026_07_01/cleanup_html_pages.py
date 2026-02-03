#!/usr/bin/env python3
"""
Bereinigt HTML-Dateien aus einem FHIR Implementation Guide,
um sie als eigenständige Dokumentationsseiten zu verwenden.

Entfernt Navigation, Header, Breadcrumbs und andere IG-spezifische Elemente.
"""

import os
import sys
import re
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup

VERSION = "0.9.0"


def cleanup_html(html_content, file_path):
    """
    Bereinigt den HTML-Content von IG-spezifischen Elementen.
    
    Args:
        html_content: Der ursprüngliche HTML-Content
        file_path: Pfad zur Datei (für Logging)
    
    Returns:
        Bereinigter HTML-Content
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 1. Entferne Navigation (segment-navbar)
    navbar = soup.find(id='segment-navbar')
    if navbar:
        navbar.decompose()
        print(f"  ✓ Navigation entfernt")
    
    # 2. Entferne Header mit Logo (segment-header)
    header = soup.find(id='segment-header')
    if header:
        header.decompose()
        print(f"  ✓ Header entfernt")
    
    # 3. Entferne Breadcrumbs (segment-breadcrumb)
    breadcrumb = soup.find(id='segment-breadcrumb')
    if breadcrumb:
        breadcrumb.decompose()
        print(f"  ✓ Breadcrumbs entfernt")
    
    # 4. Entferne IG-Headline-Banner
    headline_container = soup.find(class_='gem-ig-headline-container')
    if headline_container:
        headline_container.decompose()
        print(f"  ✓ IG-Banner entfernt")
    
    # 5. Vereinfache Footer
    footer = soup.find(id='segment-footer')
    if footer:
        # Ersetze durch einfachen Footer
        new_footer = soup.new_tag('div', id='segment-footer', **{'class': 'segment'})
        footer_container = soup.new_tag('div', **{'class': 'container'})
        footer_inner = soup.new_tag('div', **{'class': 'inner-wrapper'})
        footer_text = soup.new_tag('p')
        footer_text.string = 'Mapping-Dokumentation extrahiert aus dem E-Rezept Implementation Guide'
        footer_inner.append(footer_text)
        footer_container.append(footer_inner)
        new_footer.append(footer_container)
        footer.replace_with(new_footer)
        print(f"  ✓ Footer vereinfacht")
    
    # 6. Entferne überflüssige Menü-Skripte im Head
    for script in soup.find_all('script'):
        src = script.get('src', '')
        if 'menu' in src.lower():
            script.decompose()
    
    # 7. Bereinige externe Links zu IG-Seiten (optional: in Text umwandeln)
    for link in soup.find_all('a'):
        href = link.get('href', '')
        # Links zu IG-internen Seiten, die nicht existieren
        if href and (href.startswith('menu-') or href in ['index.html', 'toc.html', 'artifacts.html']):
            # Konvertiere zu normalem Text
            link.name = 'span'
            del link['href']
    
    # 8. Füge einfachen Titel hinzu, wenn keiner existiert
    content_div = soup.find(id='segment-content')
    if content_div:
        h2 = content_div.find('h2')
        if h2:
            title_text = h2.get_text(strip=True)
            # Bereinige Nummerierung aus dem Titel
            title_text = re.sub(r'^\d+(\.\d+)*\s*', '', title_text)
            
            # Aktualisiere den Seitentitel
            title_tag = soup.find('title')
            if title_tag:
                title_tag.string = title_text
    
    return str(soup)


def create_index_page(directory, html_files, run_date, version):
    """
    Erstellt eine Übersichtsseite mit Links zu allen Mapping-Dokumenten.
    
    Args:
        directory: Pfad zum Verzeichnis
        html_files: Liste der HTML-Dateien
    """
    # Filtere nur mapping-*.html Dateien und sortiere sie
    mapping_files = sorted([f for f in html_files if f.name.startswith('mapping-')])
    
    if not mapping_files:
        print("⚠️  Keine Mapping-Dateien für Index gefunden")
        return
    
    # Erstelle Links mit lesbaren Titeln
    links_html = []
    for html_file in mapping_files:
        # Extrahiere Titel aus der Datei
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
                soup = BeautifulSoup(content, 'html.parser')
                h2 = soup.find('h2')
                if h2:
                    title = h2.get_text(strip=True)
                    # Bereinige Nummerierung
                    title = re.sub(r'^\d+(\.\d+)*\s*', '', title)
                else:
                    title = html_file.stem.replace('mapping-', '').replace('-', ' ').title()
        except:
            title = html_file.stem.replace('mapping-', '').replace('-', ' ').title()
        
        links_html.append(f'        <li><a href="{html_file.name}">{title}</a></li>')
    
    index_html = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE HTML>
<html lang="de" xml:lang="de" xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta content="text/html;charset=utf-8" http-equiv="Content-Type"/>
    <title>FHIR Mapping-Dokumentation - E-Rezept-Fachdienst ab 01.07.2026</title>
    <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
    <link href="fhir.css" rel="stylesheet"/>
    <link href="assets/css/bootstrap-fhir.css" rel="stylesheet"/>
    <link href="assets/css/project.css" rel="stylesheet"/>
    <link href="assets/css/ig.gematik.css" rel="stylesheet"/>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        h1 {{
            color: #2a6496;
            border-bottom: 3px solid #2a6496;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }}
        h2 {{
            color: #2a6496;
            margin-top: 30px;
        }}
        .info-box {{
            background-color: #e7f3ff;
            border-left: 4px solid #2a6496;
            padding: 15px;
            margin: 20px 0;
        }}
        .mapping-list {{
            list-style-type: none;
            padding: 0;
        }}
        .mapping-list li {{
            margin: 10px 0;
            padding: 10px;
            background-color: #f8f9fa;
            border-radius: 4px;
        }}
        .mapping-list a {{
            color: #2a6496;
            text-decoration: none;
            font-weight: 500;
        }}
        .mapping-list a:hover {{
            text-decoration: underline;
        }}
        footer {{
            margin-top: 50px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            color: #666;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <h1>FHIR Mapping-Dokumentation</h1>
    <p><strong>Datum:</strong> {run_date} &nbsp;|&nbsp; <strong>Version:</strong> {version}</p>

    <div class="info-box">
        <strong>Gültig ab:</strong> 01.07.2026<br/>
        <strong>Beschreibung:</strong> Diese Dokumentation beschreibt das FHIR-Mapping, welches der E-Rezept-Fachdienst
        ab dem 01.07.2026 für die Transformation von Verordnungsdaten ausführen wird.
    </div>

    <h2>Übersicht der Mapping-Dokumentationen</h2>

    <p>
        Die folgenden Dokumente beschreiben detailliert, wie die FHIR-Ressourcen vom KBV-Format 
        in das EPA-Format transformiert werden. Dabei muss
    </p>

    <ul class="mapping-list">
{chr(10).join(links_html)}
    </ul>

    <h2>Hintergrund</h2>

    <p>
        Diese Mappings sind Teil der Integration des E-Rezept-Fachdienstes mit der
        elektronischen Patientenakte (ePA). Sie definieren die Transformation von
        Verordnungsdaten gemäß den KBV-Profilen (Kassenärztliche Bundesvereinigung)
        in die EPA-Medication-Profile.
    </p>

    <footer>
        <p>
            Mapping-Dokumentation extrahiert aus dem
            <a href="https://simplifier.net/eRezept" target="_blank" rel="noopener noreferrer">
                E-Rezept Implementation Guide
            </a>
        </p>
        <p>© gematik GmbH</p>
    </footer>
</body>
</html>"""
    
    index_path = directory / 'index.html'
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_html)
    
    print(f"📝 Übersichtsseite erstellt: {index_path.name}")


def process_directory(directory):
    """
    Verarbeitet alle HTML-Dateien in einem Verzeichnis und dessen Unterverzeichnissen.
    
    Args:
        directory: Pfad zum Verzeichnis
    """
    directory = Path(directory)
    
    if not directory.exists():
        print(f"❌ Verzeichnis nicht gefunden: {directory}")
        return
    
    html_files = list(directory.rglob('*.html'))
    
    if not html_files:
        print(f"⚠️  Keine HTML-Dateien gefunden in {directory}")
        return
    
    print(f"\n🔍 {len(html_files)} HTML-Datei(en) gefunden in {directory}\n")
    
    for html_file in html_files:
        # Überspringe die index.html, falls sie bereits existiert
        if html_file.name == 'index.html':
            continue
            
        print(f"📄 Verarbeite: {html_file.name}")
        
        try:
            # Lese Datei
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Bereinige Content
            cleaned_content = cleanup_html(content, html_file)
            
            # Speichere Datei
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)
            
            print(f"  ✅ Erfolgreich bereinigt\n")
            
        except Exception as e:
            print(f"  ❌ Fehler: {e}\n")
    
    # Erstelle Übersichtsseite
    print("\n📋 Erstelle Übersichtsseite...\n")
    run_date = datetime.now().strftime('%d.%m.%Y')
    create_index_page(
        directory,
        [f for f in html_files if f.name != 'index.html'],
        run_date,
        VERSION,
    )


def main():
    """Hauptfunktion"""
    if len(sys.argv) < 2:
        print("Usage: python cleanup_html_pages.py <directory>")
        print("\nBeispiel:")
        print("  python cleanup_html_pages.py docs/erp_epa_mapping_details")
        sys.exit(1)
    
    directory = sys.argv[1]
    
    print("=" * 60)
    print("HTML-Bereinigung für GitHub Pages")
    print("=" * 60)
    
    process_directory(directory)
    
    print("=" * 60)
    print("✅ Bereinigung abgeschlossen!")
    print("=" * 60)


if __name__ == '__main__':
    main()
