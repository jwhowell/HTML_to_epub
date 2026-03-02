import requests
from bs4 import BeautifulSoup
from ebooklib import epub
from urllib.parse import urljoin
import re
from pathlib import Path

#BASE_URL = "https://www.typescriptlang.org/docs/handbook/"
#START_URL = BASE_URL + "intro.html"
OUTPUT_EPUB = "Output.epub"

def get_soup(url: str) -> BeautifulSoup:
    headers = {"User-Agent": "Mozilla/5.0 (compatible; HandbookScraper/1.0)"}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "lxml")

def clean_content(soup: BeautifulSoup) -> str:
    """Extract main content and clean junk"""
    main = soup.select_one("main") or soup.body
    if not main:
        return ""
    
    # Remove unwanted parts
    for sel in [
        "script", "style", "nav", "footer", ".header", ".edit-link",
        ".dark-mode-toggle", ".breadcrumbs", "iframe", ".ts-playground"
    ]:
        for el in main.select(sel):
            el.decompose()
       
    return str(main)

def main():
    print("Fetching table of contents...")
    chapters = [('Introduction', 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide#introduction'), ('Grammar and types', 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide#grammar_and_types'), ('Control flow and error handling', 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide#control_flow_and_error_handling'), ('Loops and iteration', 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide#loops_and_iteration'), ('Functions', 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide#functions'), ('Expressions and operators', 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide#expressions_and_operators'), ('Numbers and strings', 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide#numbers_and_strings'), ('Representing dates & times', 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide#representing_dates_times'), ('Regular expressions', 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide#regular_expressions'), ('Indexed collections', 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide#indexed_collections'), ('Keyed collections', 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide#keyed_collections'), ('Working with objects', 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide#working_with_objects'), ('Using classes', 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide#using_classes'), ('Promises', 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide#promises'), ('Typed arrays', 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide#typed_arrays'), ('Iterators and generators', 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide#iterators_and_generators'), ('Resource management', 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide#resource_management'), ('Internationalization', 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide#internationalization'), ('JavaScript modules', 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide#javascript_modules'), ('Advanced topics', 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide#advanced_topics')]
    print(f"Found {len(chapters)} chapters")
    
    identifier = str(input("Enter the book's Identifier: "))
    book_title = str(input("Enter the book's Title: "))
    author = str(input("Enter the book's author: "))

    OUTPUT_EPUB = str(input("Output file name (include .epub): "))

    book = epub.EpubBook()
    book.set_identifier(identifier)
    book.set_title(book_title)
    book.set_language("en")
    book.add_author(author)
    
    # Optional: add cover (download manually or skip)
    # cover = epub.EpubItem(uid="cover", file_name="cover.jpg", media_type="image/jpeg", content=...)
    # book.add_item(cover)
    # book.set_cover("cover.jpg", cover.content)
    
    toc_items = []
    spine = ["nav"]
    
    for i, (title, url) in enumerate(chapters, 1):
        print(f"Scraping {i}/{len(chapters)}: {title}")
        soup = get_soup(url)
        content_html = clean_content(soup)
        
        chapter = epub.EpubHtml(
            title=title,
            file_name=f"chap_{i:02d}.xhtml",
            lang="en"
        )
        chapter.content = f"<h1>{title}</h1>{content_html}".encode("utf-8")
        
        book.add_item(chapter)
        toc_items.append(chapter)
        spine.append(chapter)
    
    book.toc = toc_items
    book.spine = spine
    
    # Add basic nav (table of contents)
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    
    # Write it out
    epub.write_epub(OUTPUT_EPUB, book)
    print(f"EPUB saved to: {Path(OUTPUT_EPUB).resolve()}")

if __name__ == "__main__":
    main()