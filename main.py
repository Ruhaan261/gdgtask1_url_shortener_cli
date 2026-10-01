import argparse
from datetime import datetime
import json
import os
import random
import string
from urllib.parse import urlparse
import webbrowser

DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        backup = DATA_FILE + ".corrupt"
        os.replace(DATA_FILE, backup)
        print(f"Warning: {DATA_FILE} was corrupted. "
              f"Saved a copy as {backup} and started fresh.")
        return {}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def generate_code(length=6):
    characters = string.ascii_letters + string.digits
    return "".join(random.choices(characters, k=length))

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def shorten(url, alias=None):
    if not is_valid_url(url):
        print(f'Error: "{url}" is not a valid URL.')
        return
    
    data = load_data()

    if alias:
        code = alias
        if code in data:
            answer = input(f"Alias '{code}' already exists and maps to {data[code]['url']}. Overwrite? (yes/no): ")
            if answer.lower() != 'yes':
                print('Operation Cancelled.')
                return
    else:
        code = generate_code()
        while code in data:
            code = generate_code()

    data[code] = {
        "url":url,
        "clicks": 0,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    save_data(data)
    print(f"Short code created: {code}")

def resolve(code):
    data = load_data()

    if code not in data:
        print(f"Error: short code '{code}' not found.")
        return

    data[code]["clicks"] += 1
    save_data(data)

    url = data[code]["url"]
    print(f"Resolved to: {url}")
    webbrowser.open(url)

def list_urls():
    data = load_data()

    if not data:
        print('No URLs have been shortened yet.')
        return

    for code, info in data.items():
        print(f"{code}-> {info['url']}| clicks:{info['clicks']}| created:{info['created_at']}")

def main():
    parser = argparse.ArgumentParser(description="A simple CLI URL shortener.")
    subparsers = parser.add_subparsers(dest="command")

    shorten_parser = subparsers.add_parser("shorten", help="Shorten a URL")
    shorten_parser.add_argument("url", help="The URL to shorten")
    shorten_parser.add_argument("--alias", help="Custom alias for the short code", default = None)

    resolve_parser = subparsers.add_parser("resolve", help="Resolve a short code to its URL")
    resolve_parser.add_argument("code", help="The short code to resolve")

    subparsers.add_parser("list", help="List of all shortened URLs")

    args = parser.parse_args()

    if args.command == "shorten":
        shorten(args.url, args.alias)
    elif args.command == "resolve":
        resolve(args.code)
    elif args.command == "list":
        list_urls()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()