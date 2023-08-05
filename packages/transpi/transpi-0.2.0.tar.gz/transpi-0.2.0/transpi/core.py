from requests_html import HTMLSession


class Trans:
    def __init__(self, word):
        self.word = word
        self._url = ""
        self.pronounce = []
        self.trans = []
        self.examples = []

    @property
    def egg(self):
        return {
            "origin": self.word,
            "pronounce": self.pronounce,
            "trans": self.trans,
            "examples": self.examples,
        }

    def translation(self):
        pass

    @property
    def session(self):
        return HTMLSession()


class YoudaoTrans(Trans):
    def __init__(self, word):
        super(YoudaoTrans, self).__init__(word)
        self._url = f"http://dict.youdao.com/w/eng/{word}/"
        self.r = self.session.get(self._url)

    def translation(self):
        self.pronounce = [
            "".join(p.xpath("//span//text()")).replace("\n", "").replace(" ", "")
            for p in self.r.html.xpath("//span[@class='pronounce']")
        ]

        trans = self.r.html.xpath("(//div[@class='trans-container'])[1]/ul/li/text()")
        self.trans = [
            {"cixing": t.split(".")[0], "tran": t.split(".")[1]} for t in trans
        ]

        temp_examples = self.r.html.xpath("//div[@id='bilingual']/ul/li")
        self.examples = [
            {
                "en": "".join(example.xpath("(//p)[1]//text()")).strip("\n"),
                "cn": "".join(example.xpath("(//p)[2]//text()")).strip("\n"),
            }
            for example in temp_examples
        ]

        return self.egg


class BaiduTrans(Trans):
    pass


class BingTrans(Trans):
    def __init__(self, word):
        super(BingTrans, self).__init__(word)
        self._url = "https://cn.bing.com/dict/search"
        cookies = self.session.get(self._url).cookies
        self.r = self.session.get(self._url, params={"q": word}, cookies=cookies)

    def translation(self):
        # pronounce
        self.pronounce = [
            i.strip(" ")
            for i in self.r.html.xpath("(//div[@class='hd_p1_1']//div)//text()")
        ]

        # trans
        self.trans = [
            {
                "cixing": t.xpath("(//span)[1]//text()")[0],
                "tran": t.xpath("(//span)[2]//text()")[0],
            }
            for t in self.r.html.xpath("//div[@class='qdef']/ul//li")
        ]

        # example sentence
        self.examples = [
            {
                "en": "".join(e.xpath("//div[@class='sen_en b_regtxt']//text()")),
                "cn": "".join(e.xpath("//div[@class='sen_cn b_regtxt']//text()")),
            }
            for e in self.r.html.xpath("//div[@id='sentenceSeg']//div[@class='se_li1']")
        ]

        return self.egg


def trans(word, engine: str = "youdao"):
    """trans word
    default engine is youdao
    """
    egg = []

    if engine == "youdao":
        egg = YoudaoTrans(word).translation()
    elif engine == "bing":
        egg = BingTrans(word).translation()

    return egg


if __name__ == "__main__":

    result = trans("human", engine="youdao")
    print(result)
