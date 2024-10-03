import os
from scrapy import Request, Spider
from scrapy.http import Response
from typing import Iterable
from scrapy.crawler import CrawlerProcess


class T2Educacao(Spider):
    name = "t2-educacao"

    headers = {
        "access-token": "lBmxWZcI49Zx9JXeGqCrrw",
        "client": "E3Ccb-4LvdWUcjrziIm4QQ",
        "uid": "juviitor@outlook.com",
    }

    def start_requests(self) -> Iterable[Request]:

        try:
            courseID = int(input("Course ID: "))
            yield Request(
                url=f"https://cursos.t2.com.br/api/v1/courses/{courseID}/lessons",
                callback=self.extractVideos,
                headers=self.headers,
            )
        except Exception as e:
            print("\nDigite um numero valido")

    def extractVideos(self, response: Response):
        videosData = response.json()["data"]

        for video in videosData:
            urlCode: str = video["videoUrl"].split("/")[-1]
            finalVideoUrl = f"https://player.vimeo.com/video/{urlCode}"
            os.system("ls")
            yield {"title": video["name"], "url": finalVideoUrl}


process = CrawlerProcess(
    settings={
        "FEEDS": {
            "t2educacao-matFinanceiraComHP-12C.json": {
                "format": "json",
                "encoding": "utf8",
            },
        },
    }
)

process.crawl(T2Educacao)
process.start()
