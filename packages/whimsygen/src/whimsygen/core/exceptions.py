"""Custom exceptions for whimsygen."""


class WhimsyGenError(Exception):
    """Base exception for whimsygen."""

    pass


class CrawlerError(WhimsyGenError):
    """Error during Wikipedia crawling."""

    pass


class ExtractionError(WhimsyGenError):
    """Error during strategy extraction."""

    pass


class SamplerError(WhimsyGenError):
    """Error during strategy sampling."""

    pass
