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
from bs4 import BeautifulSoup


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
