import os
import requests

from celery import shared_task
from .models import Team, News
import json

@shared_task(name="get_news")
def get_news():
    teams = Team.objects.all()
    for team in teams:
        search_url = f"https://site.web.api.espn.com/apis/search/v2?region=us&lang=en&limit=50&page=1&type=article&iapPackages=ESPN_PLUS_PFL_112423%2CESPN_PLUS%2CESPN_PLUS_MLB&dtciVideoSearch=true&query={team.name}"
        
        # Google 검색 결과 페이지를 가져옵니다.
        response = requests.get(search_url)
        
        if response.status_code == 200:
            data = json.loads(response.content)
            articles=data["results"][0]["contents"]
            count=0
            for article in articles:
                if count==12:
                    break
                title = article["displayName"]
                link = article["link"]["web"]
                if "images" in article:
                    thumbnail = article["images"][0]["url"]
                else:
                    thumbnail=""
                published_date = article["date"]
                author = article["byline"]
                team = team
                news = News(
                    team=team,
                    title=title,
                    thumbnail=thumbnail,
                    url=link,
                    author=author,
                    published_date=published_date,
                )
                news.save()
                count+=1  
    return "News crawling completed."

