# import the necessary packages
from imutils import paths
import cv2
import os
import io
import re
import base64
from PIL import Image
import selenium
import requests
import time
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


# Scrape Amazon 
def get_amazon_data(query, no_of_pages):
    def get_data(query, no_of_pages):
        amazon_dict = {
            "featured": {
                "products_name": [],
                "prices": [],
                "ratings": [],
                "products_img": [],
                "products_url": [],
                "prime_delivery": []
            },
            "low_to_high": {
                "products_name": [],
                "prices": [],
                "ratings": [],
                "products_img": [],
                "products_url": [],
                "prime_delivery": []
            },
            "high_to_low": {
                "products_name": [],
                "prices": [],
                "ratings": [],
                "products_img": [],
                "products_url": [],
                "prime_delivery": []
            },
            "average_customer_review": {
                "products_name": [],
                "prices": [],
                "ratings": [],
                "products_img": [],
                "products_url": [],
                "prime_delivery": []
            },
            "newest_arrival": {
                "products_name": [],
                "prices": [],
                "ratings": [],
                "products_img": [],
                "products_url": [],
                "prime_delivery": []
            }
        }

        executable_path = {"executable_path": "chromedriver.exe"}
        browser = Browser("chrome", **executable_path, headless=True)
        for j in list(range(5)):
            for i in list(range(no_of_pages)):
                news_url = f"https://www.amazon.com/s?k={query}&page={i}"
                try:
                    browser.visit(news_url)
                    browser.find_by_xpath('//*[@id="a-autoid-0"]').click()
                    browser.find_by_xpath(
                        f'//*[@id="s-result-sort-select_{str(j)}"]').click()
                    html = browser.html
                    soup = bs(html, "html.parser")

                    for d in soup.findAll('div', attrs={'class': 'sg-col-4-of-24 sg-col-4-of-12 sg-col-4-of-36 s-result-item s-asin sg-col-4-of-28 sg-col-4-of-16 sg-col sg-col-4-of-20 sg-col-4-of-32'}):
                        name = d.find(
                            'span', attrs={'class': 'a-size-base-plus a-color-base a-text-normal'})
                        price = d.find('span', attrs={'class': 'a-offscreen'})
                        rating = d.find('span', attrs={'class': 'a-icon-alt'})
                        prime = d.find(
                            'i', attrs={'class': 'a-icon a-icon-prime a-icon-medium'})
                        img = d.find('img', attrs={'class': 's-image'})
                        url = d.find(
                            'a', attrs={'class': 'a-link-normal a-text-normal'})

                        if name is not None and price is not None:
                            amazon_dict[list(amazon_dict.keys())[
                                j]]["products_name"].append(name.text)
                            amazon_dict[list(amazon_dict.keys())[
                                j]]["prices"].append(price.text)

                            if rating is not None:
                                amazon_dict[list(amazon_dict.keys())[
                                    j]]["ratings"].append(rating.text)
                            else:
                                amazon_dict[list(amazon_dict.keys())[
                                    j]]["ratings"].append("Missing")

                            if img is not None:
                                amazon_dict[list(amazon_dict.keys())[
                                    j]]["products_img"].append(img["src"])
                            else:
                                amazon_dict[list(amazon_dict.keys())[
                                    j]]["products_img"].append(" ")

                            if url is not None:
                                amazon_dict[list(amazon_dict.keys())[j]]["products_url"].append(
                                    "https://amazon.com"+url["href"])
                            else:
                                amazon_dict[list(amazon_dict.keys())[
                                    j]]["products_url"].append(" ")

                            if prime is not None:
                                amazon_dict[list(amazon_dict.keys())[j]]["prime_delivery"].append(
                                    "Prime Delivery")
                            else:
                                amazon_dict[list(amazon_dict.keys())[j]]["prime_delivery"].append(
                                    "Not Prime Delivery")

                except Error as e:
                    print(e)
        browser.quit()
        return amazon_dict
    data = None
    str_error = None
    num_retries = 20
    for x in range(0, num_retries):
        try:
            data = get_data(query, no_of_pages)
        except Error as e:
            pass

        if data["high_to_low"] == None:
            continue
        else:
            break
    return data

# Scrape Walmart


def get_walmart_data(query, no_of_pages):
    def get_data(query, no_of_pages):
        drop_down = [
            "best_match--Best Match",
            "best_seller--Best Sellers",
            "price_low--Price: low to high",
            "price_high--Price: high to low",
            "rating_high--Highest Rating",
            "new--New"
        ]
        walmart_dict = {
            "best_match": {
                "products_name": [],
                "prices": [],
                "ratings": [],
                "no_of_reviews": [],
                "products_img": [],
                "products_url": [],
                "delivery_info": []
            },
            "best_sellers": {
                "products_name": [],
                "prices": [],
                "ratings": [],
                "no_of_reviews": [],
                "products_img": [],
                "products_url": [],
                "delivery_info": []
            },
            "high_to_low": {
                "products_name": [],
                "prices": [],
                "ratings": [],
                "no_of_reviews": [],
                "products_img": [],
                "products_url": [],
                "delivery_info": []
            },
            "low_to_high": {
                "products_name": [],
                "prices": [],
                "ratings": [],
                "no_of_reviews": [],
                "products_img": [],
                "products_url": [],
                "delivery_info": []
            },
            "highest_rating": {
                "products_name": [],
                "prices": [],
                "ratings": [],
                "no_of_reviews": [],
                "products_img": [],
                "products_url": [],
                "delivery_info": []
            },
            "newest_arrival": {
                "products_name": [],
                "prices": [],
                "ratings": [],
                "no_of_reviews": [],
                "products_img": [],
                "products_url": [],
                "delivery_info": []
            }
        }

        executable_path = {"executable_path": "chromedriver.exe"}
        browser = Browser("chrome", **executable_path, headless=True)
        for i in list(range(1, no_of_pages+1)):
            url = f"https://www.walmart.com/search/?page={i}&query={query}"
            browser.visit(url)
            for j in list(range(6)):
                browser.execute_script(
                    "window.scrollTo(0, -document.body.scrollHeight);")
                browser.find_by_xpath(
                    '//*[@id="SearchContainer"]/div/div[2]/div/div[2]/div/div[2]/div[1]/div/select').click()
                browser.find_by_value(drop_down[j]).click()
                html = browser.html
                soup = bs(html, "html.parser")

                for d in soup.findAll('li'):
                    try:
                        name = d.find(
                            'div', attrs={'class': 'search-result-product-title gridview'})
                        price = d.find('span', attrs={'class': 'price display-inline-block arrange-fit price price-main'})\
                            .find('span', attrs={'class': 'visuallyhidden'})
                        rating = d.find(
                            'span', attrs={'class': 'seo-avg-rating'})
                        review = d.find(
                            'span', attrs={'class': 'seo-review-count'})
                        delivery = d.find(
                            'div', attrs={'class': 'search-result-product-shipping-details gridview'})
                        img = d.find(
                            'div', attrs={'class': 'orientation-square'}).find("img")
                        url = d.find('a', attrs={
                                     'class': 'product-title-link line-clamp line-clamp-2 truncate-title'})

                        if name.find("a").find("span") is not None and price is not None:
                            walmart_dict[list(walmart_dict.keys())[j]]["products_name"].append(
                                name.find("a").find("span").text.replace('"', 'inch').replace("'", ""))
                            walmart_dict[list(walmart_dict.keys())[
                                j]]["prices"].append(price.text)

                            if rating is not None:
                                walmart_dict[list(walmart_dict.keys())[
                                    j]]["ratings"].append(rating.text)
                            else:
                                walmart_dict[list(walmart_dict.keys())[
                                    j]]["ratings"].append("Missing Ratings")

                            if review is not None:
                                walmart_dict[list(walmart_dict.keys())[
                                    j]]["no_of_reviews"].append(rating.text)
                            else:
                                walmart_dict[list(walmart_dict.keys())[
                                    j]]["no_of_reviews"].append("Missing Reviews")

                            if img is not None:
                                walmart_dict[list(walmart_dict.keys())[j]]["products_img"].append(
                                    img["data-image-src"])
                            else:
                                walmart_dict[list(walmart_dict.keys())[
                                    j]]["products_img"].append(" ")

                            if url is not None:
                                walmart_dict[list(walmart_dict.keys())[j]]["products_url"].append(
                                    "https://walmart.com"+url["href"])
                            else:
                                walmart_dict[list(walmart_dict.keys())[
                                    j]]["products_url"].append(" ")

                            if delivery is not None:
                                walmart_dict[list(walmart_dict.keys())[j]]["delivery_info"].append(
                                    delivery.text.replace("\xa0", " "))
                            else:
                                walmart_dict[list(walmart_dict.keys())[
                                    j]]["delivery_info"].append("Missing")

                    except:
                        pass
        browser.quit()
        return walmart_dict
    data = None
    str_error = None
    num_retries = 50
    for x in range(0, num_retries):
        try:
            data = get_data(query, no_of_pages)
        except ElementClickInterceptedException as e:
            pass

        if data["high_to_low"] == None:
            continue
        else:
            break
    return data
