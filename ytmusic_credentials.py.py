#!/usr/bin/env python3

import http.client
import browser_cookie3  # Install with `pip install browser-cookie3`
import ytmusicapi
import os


def fetch_ytmusic_headers():
    """
    Fetch raw headers from an authenticated YouTube Music session.
    Returns the raw HTTP request as a string.
    """
    print("Fetching YouTube Music headers...")

    # Extract cookies from the browser
    cookies = browser_cookie3.firefox(domain_name="music.youtube.com")

    # Define the target host and endpoint
    host = "music.youtube.com"
    path = "/youtubei/v1/browse"

    headers = {
        "Host": host,
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:134.0) Gecko/20100101 Firefox/134.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.7,he;q=0.3",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Content-Type": "application/json",
        "Referer": f"https://{host}/library",
        "Connection": "keep-alive",
    }

    # Add cookies to headers
    cookies_header = "; ".join([f"{cookie.name}={cookie.value}" for cookie in cookies])
    headers["Cookie"] = cookies_header

    # Simulate additional required headers for the YouTube Music API
    headers.update({
        "X-Goog-Visitor-Id": "Cgs2NS0zVmZzaWpkTSiLjv-7BjIKCgJJTBIEGgAgVQ%3D%3D",
        "X-Youtube-Bootstrap-Logged-In": "true",
        "X-Youtube-Client-Name": "67",
        "X-Youtube-Client-Version": "1.20241218.01.00",
        "X-Goog-AuthUser": "0",
        "X-Origin": f"https://{host}",
        "DNT": "1",
        "Sec-GPC": "1",
    })

    # Construct the raw HTTP request
    raw_request = f"POST {path} HTTP/3\n"
    raw_request += "\n".join([f"{key}: {value}" for key, value in headers.items()])
    raw_request += "\n\n{...JSON body payload here...}"

    return raw_request


def generate_credentials(raw_headers, credentials_file="oauth.json"):
    """
    Generate YouTube Music credentials using raw headers.

    Parameters:
        raw_headers (str): Raw headers string extracted from fetch_ytmusic_headers().
        credentials_file (str): Path to save the configuration headers (credentials).
    """
    print("Generating YouTube Music credentials file...")
    try:
        # Use ytmusicapi.setup to process headers and save the credentials
        config_headers = ytmusicapi.setup(filepath=credentials_file, headers_raw=raw_headers)
        print(f"Configuration headers saved to {credentials_file}")
        return config_headers
    except Exception as e:
        raise RuntimeError(f"Failed to generate credentials: {e}")


def main():
    """
    Main function to handle the complete YouTube Music credential generation process.
    """
    try:
        # Fetch raw headers
        raw_headers = fetch_ytmusic_headers()
        if not raw_headers:
            print("Failed to fetch raw headers. Exiting.")
            return

        # Save raw headers to a file (optional step for debugging purposes)
        raw_headers_file = "raw_headers.txt"
        with open(raw_headers_file, "w", encoding="utf-8") as file:
            file.write(raw_headers)
        print(f"Raw headers saved to {raw_headers_file}")

        # Generate YouTube Music credentials
        credentials_file = "oauth.json"
        generate_credentials(raw_headers, credentials_file=credentials_file)
        print("YouTube Music credentials generated successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
