import sys
from crawler import fetch_robots, fetch_sitemap
from parser import extract_forms
from reporter import print_report


def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py https://example.com")
        sys.exit(1)

    target = sys.argv[1]

    print(f"[+] Target: {target}")

    robots_data = fetch_robots(target)
    sitemap_links = fetch_sitemap(target)
    forms = extract_forms(target)

    print_report(robots_data, sitemap_links, forms)


if __name__ == "__main__":
    main()
