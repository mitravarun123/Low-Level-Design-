from abc import ABC, abstractmethod
from enum import Enum


class Url:
    def __init__(self, shortcode, longcode):
        self.shortcode = shortcode
        self.longcode = longcode

    def get_shortcode(self):
        return self.shortcode

    def get_longcode(self):
        return self.longcode


class EncoderStrategy(ABC):
    @abstractmethod
    def encode(self, num):
        pass


class Base62Encoder(EncoderStrategy):
    def __init__(self):
        self.base = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

    def encode(self, num):
        if num == 0:
            return self.base[0]

        res = ""
        while num > 0:
            res = self.base[num % 62] + res
            num //= 62
        return res


class Base64Encoder(EncoderStrategy):
    def __init__(self):
        self.base = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+/"

    def encode(self, num):
        if num == 0:
            return self.base[0]

        res = ""
        while num > 0:
            res = self.base[num % 64] + res
            num //= 64
        return res


class EncoderType(Enum):
    BASE62 = "BASE62"
    BASE64 = "BASE64"


class EncoderFactory:
    @staticmethod
    def get_encoder(encoder_type: EncoderType) -> EncoderStrategy:
        if encoder_type == EncoderType.BASE62:
            return Base62Encoder()
        elif encoder_type == EncoderType.BASE64:
            return Base64Encoder()
        else:
            raise ValueError("Unsupported Encoder Type")


class UrlRepository:
    def __init__(self):
        self.short_to_long = {}
        self.long_to_short = {}

    def save(self, url: Url):
        self.short_to_long[url.get_shortcode()] = url.get_longcode()
        self.long_to_short[url.get_longcode()] = url.get_shortcode()

    def get_long(self, short):
        return self.short_to_long.get(short)

    def get_short(self, long):
        return self.long_to_short.get(long)



class UrlShortenerService:
    def __init__(self, encoder: EncoderStrategy):
        self.encoder = encoder
        self.repo = UrlRepository()
        self.counter = 1

    def shorten_url(self, long_url):
        existing = self.repo.get_short(long_url)
        if existing:
            return existing

        short_code = self.encoder.encode(self.counter)
        self.counter += 1

        url = Url(short_code, long_url)
        self.repo.save(url)

        return short_code

    def expand_url(self, short_code):
        return self.repo.get_long(short_code)



if __name__ == "__main__":


    encoder = EncoderFactory.get_encoder(EncoderType.BASE62)
    service = UrlShortenerService(encoder)

    s1 = service.shorten_url("https://leetcode.com/problems/word-search")
    s2 = service.shorten_url("https://github.com/mitravarun123")

    print("BASE62:")
    print(s1, "->", service.expand_url(s1))
    print(s2, "->", service.expand_url(s2))


    encoder64 = EncoderFactory.get_encoder(EncoderType.BASE64)
    service64 = UrlShortenerService(encoder64)

    s3 = service64.shorten_url("https://systemdesignprimer.com")

    print("\nBASE64:")
    print(s3, "->", service64.expand_url(s3))
