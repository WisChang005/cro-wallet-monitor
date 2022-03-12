import os
import logging

from bs4 import BeautifulSoup
import requests


LINE_TOKEN = os.environ["PERSONAL_LINE_TOKEN"]


def main():
    line_notify(LINE_TOKEN, get_sending_message())


def get_sending_message() -> str:
    cro_wallet_counts = get_cro_wallet_counts()
    cro_prise = get_cro_price()
    message = f"\nCRO Prise ($USD): {cro_prise}\nCRO Wallet addresses: {cro_wallet_counts}"
    return message


def get_cro_wallet_counts() -> str:
    url = "https://cronos.org/explorer/"
    headers = {
        "User-Agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                       "(KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.62"),
        "Accept-Language": "en-US,en;q=0.9"
    }
    rsp = requests.get(url, headers=headers)
    bs4 = BeautifulSoup(rsp.text, "lxml")
    span_tag = bs4.find("span", {"data-selector": "address-count"})
    return span_tag.text.strip()


def line_notify(line_token: str, msg: str):
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {line_token}"}
    payload = {"message": msg}
    r = requests.post(url, headers=headers, params=payload)
    line_status = r.status_code
    logging.debug("Line notify status code [%s]", line_status)
    return line_status


def get_cro_price() -> str:
    url = "https://coinmarketcap.com/currencies/cronos/holders/"
    headers = {
        "User-Agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                       "(KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.62"),
        "Accept-Language": "en-US,en;q=0.9"
    }
    rsp = requests.get(url, headers=headers)
    bs4 = BeautifulSoup(rsp.text, "lxml")
    cro_prise = bs4.find("div", {"class": "priceValue"}).span.text
    return cro_prise


if __name__ == "__main__":
    main()
