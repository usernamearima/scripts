from colorama import Fore, Style


def print_report(robots, sitemap, forms):
    print("\n" + "="*50)
    print(Fore.CYAN + "[ROBOTS.TXT]" + Style.RESET_ALL)

    if robots:
        for line in robots:
            print("  ", line)
    else:
        print("  Not found.")

    print("\n" + "="*50)
    print(Fore.CYAN + "[SITEMAP LINKS]" + Style.RESET_ALL)

    if sitemap:
        for link in sitemap:
            print("  ", link)
    else:
        print("  Not found.")

    print("\n" + "="*50)
    print(Fore.CYAN + "[FORMS FOUND]" + Style.RESET_ALL)

    if forms:
        for i, form in enumerate(forms, 1):
            print(f"\n  Form #{i}")
            print("   Action:", form["action"])
            print("   Method:", form["method"])
            print("   Inputs:")
            for inp in form["inputs"]:
                print("    -", inp)
    else:
        print("  No forms detected.")

    print("\n" + "="*50)
