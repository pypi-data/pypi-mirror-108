from requests_html import HTMLSession


class Trans:
    def __init__(self, word):
        self.word = word
        self._url = ""
        self.pronounce = ""
        self.trans = []
        self.examples = []

    def translation(self):
        pass

    @property
    def session(self):
        return HTMLSession()


class YoudaoTrans(Trans):
    def __init__(self, word):
        super().__init__(word)
        self._url = f"http://dict.youdao.com/w/eng/{word}/"
        self.r = self.session.get(self._url)

    def translation(self):
        trans = self.r.html.xpath("(//div[@class='trans-container'])[1]/ul/li/text()")
        self.trans = [{t.split(".")[0]: t.split(".")[1]} for t in trans]

        self.pronounce = self.r.html.xpath("(//span[@class='phonetic'])[1]//text()")[0]
        temp_examples = self.r.html.xpath("//div[@id='bilingual']/ul/li")
        self.examples = [
            {
                "origin": "".join(example.xpath("(//p)[1]//text()")).strip("\n"),
                "trans": "".join(example.xpath("(//p)[2]//text()")).strip("\n"),
            }
            for example in temp_examples
        ]
        return {
            "origin": self.word,
            "pronounce": self.pronounce,
            "trans": self.trans,
            "examples": self.examples,
        }


class BaiduTrans(Trans):
    pass


class BingTrans(Trans):
    def __init__(self, word):
        super(BingTrans, self).__init__(word)
        self._url = f"https://www.bing.com/dict/search?q={word}"
        self.r = self.session.get(self._url)

    def translation(self):
        self.pronounce = self.r.html.xpath()


def trans(word, engine: str = "youdao"):
    """trans word
    default engine is youdao
    """
    result = ""

    if engine == "youdao":
        result = YoudaoTrans(word).translation()
    elif engine == "bing":
        result = BingTrans(word).translation()

    return result


if __name__ == "__main__":

    result = trans("human", engine="youdao")
    print(result)
