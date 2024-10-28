from bs4 import BeautifulSoup
import seaborn as sns
import matplotlib.pyplot as plt
import requests
import pandas as pd
import random

def map_to_int(num_string: str):
    num_string = num_string.lower()
    mapper = {
        "one":1,
        "two":2,
        "three":3,
        "four":4,
        "five":5,
    }
    return mapper[num_string]



base_url = "https://books.toscrape.com/"
site = requests.get(base_url)
soup = BeautifulSoup(site.text, "html.parser")

all_category = soup.find(class_="nav nav-list").find("ul").find_all("li")


limit = 5
data_scale = 3
offset_scale = 1
offset_limit = 0.3
ratings_data = {"category":[],
                "ratings":[],
                "mean":[],
                }


for category in all_category[:limit]:
    category_link = str(base_url + category.find("a").get("href"))
    category_name = str(category.find("a").text).strip()
    category_page = requests.get(category_link)
    category_mean : float = ...
    cat = BeautifulSoup(category_page.text, "html.parser")
    all_ratings_per_category = cat.find_all("p")[::3]
    n = len(all_ratings_per_category)

    total_ratings = 0
    for rating in all_ratings_per_category:
        rate = map_to_int(rating.get("class")[1])
        total_ratings += rate

        for i in range(data_scale):
            offset = random.randint(-offset_scale * 1000, offset_scale * 1000) * (1/1000) * offset_limit
            ratings_data["category"].append(category_name)
            ratings_data["ratings"].append(rate + offset)
    
    category_mean = total_ratings / n
    for i in range(n * data_scale):
        ratings_data["mean"].append(category_mean)
        
sns.set_theme(style="ticks")
sns.set_palette('rocket_r')
sns.catplot(data=ratings_data,
             x="category",
             y="ratings",
             hue="ratings",
             kind="swarm",
             )

plt.show()