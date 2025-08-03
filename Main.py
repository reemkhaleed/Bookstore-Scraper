import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import sys
import subprocess

def scrape_books(url):
    print("Scraping data...")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    books = []
    for book in soup.select('.product_pod'):
        title = book.h3.a['title']
        price = book.select_one('.price_color').text
        books.append({'Title': title, 'Price': price})

    return books

def save_to_excel(data, file_name='books_data.xlsx'):
    df = pd.DataFrame(data)
    df.to_excel(file_name, index=False)
    return os.path.abspath(file_name)

def open_file(filepath):
    print("Attempting to open file...")
    try:
        if sys.platform.startswith('darwin'):  # macOS
            subprocess.call(('open', filepath))
        elif os.name == 'nt':  # Windows
            os.startfile(filepath)
        elif os.name == 'posix':  # Linux
            subprocess.call(('xdg-open', filepath))
    except Exception as e:
        print(f"Could not open file automatically: {e}")

def main():
    url = "http://books.toscrape.com"
    books = scrape_books(url)

    if not books:
        print("No data found.")
        return

    file_path = save_to_excel(books)
    print(f"Data saved to: {file_path}")
    open_file(file_path)

if __name__ == "__main__":
    main()
