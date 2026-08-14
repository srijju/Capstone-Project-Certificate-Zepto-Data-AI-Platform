import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://books.toscrape.com/"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

books_data = []


def get_soup(url):
    """
    Sends GET request and returns BeautifulSoup object.
    Raises exception if request fails.
    """
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()
    return BeautifulSoup(response.text, "lxml")


def get_category_links():
    """
    Scrapes all available category links.
    Returns:
        List of tuples -> (category_name, category_url)
    """
    soup = get_soup(BASE_URL)

    category_section = soup.find("ul", class_="nav nav-list")

    categories = []

    for li in category_section.find_all("li")[1:]:   # Skip "Books"
        a = li.find("a")

        category_name = a.text.strip()

        category_url = urljoin(BASE_URL, a["href"])

        categories.append((category_name, category_url))

    return categories


def get_rating(star_tag):
    """
    Extract textual rating.
    Example:
        One
        Two
        Three
    """
    classes = star_tag["class"]

    for cls in classes:
        if cls != "star-rating":
            return cls

    return None


def scrape_category(category_name, category_url):
    """
    Scrapes every page inside one category.
    """

    next_page = category_url

    while next_page:

        soup = get_soup(next_page)

        books = soup.find_all("article", class_="product_pod")

        for book in books:

            title = book.h3.a["title"]

            price = book.find("p", class_="price_color").text.strip()

            availability = book.find(
                "p",
                class_="instock availability"
            ).text.strip()

            rating = get_rating(book.find("p", class_="star-rating"))

            books_data.append({
                "title": title,
                "price": price,
                "star_rating": rating,
                "availability": availability,
                "category": category_name
            })

        next_button = soup.find("li", class_="next")

        if next_button:

            href = next_button.a["href"]

            next_page = urljoin(next_page, href)

        else:

            next_page = None


def main():

    categories = get_category_links()

    print(f"Found {len(categories)} categories")

    # First 3 categories
    for category_name, category_url in categories[:3]:

        print(f"Scraping {category_name}")

        scrape_category(category_name, category_url)

    df = pd.DataFrame(books_data)

    print(df.head())

    print(f"\nTotal books scraped: {len(df)}")

    df.to_csv("data/raw_books.csv", index=False)

    print("Saved to data/raw_books.csv")


if __name__ == "__main__":
    main()