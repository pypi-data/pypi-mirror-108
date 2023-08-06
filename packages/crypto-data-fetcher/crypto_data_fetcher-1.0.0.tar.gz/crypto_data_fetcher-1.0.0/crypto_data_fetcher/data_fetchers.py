from .bases import BaseFetcher
from .formatters import DefaultFormatter

__all__ = ["DefaultFetcher", "SocialFetcher"]


class DefaultFetcher(BaseFetcher):
    """
    Data fetcher for default Coin Detective Page
    """
    data = DefaultFormatter()
    column_map = [
        "Market Cap Now",
        "Price Now",
        "Price 1h",
        "Price 1d",
        "Price 7d",
        "Price 30d",
        "Price 90d",
        "Price Graph 4h",
        "Price Graph 1d",
        "Price Graph 7d",
        "Price Graph 30d",
        "Price Graph 90d",
        "Volume 24h Now",
        "Volume 24h Graph 1h",
        "Volume 24h Graph 1d",
        "Volume 24h Graph 7d",
        "Available Supply Now",
        "Available Supply 1d",
        "Available Supply 7d",
        "Market Cap Rank 7d",
        "Market Cap Rank 30d",
        "Market Cap Rank Graph 90d",
        "Vol / Mcap Now",
        "Vol / Mcap Graph 7d",
    ]


class SocialFetcher(DefaultFetcher):
    """
    Data fetcher for Coin Social Stats
    """
    key = "Social"
    column_map = [
        "Market Cap Now",
        "Reddit Subscribers Now",
        "Reddit Subscribers 1d",
        "Reddit Subscribers 7d",
        "Reddit Subscribers Graph 30d",
        "Reddit Accounts Active Now",
        "Reddit Accounts Active 1d",
        "Reddit Accounts Active 7d",
        "Reddit Accounts Active Graph 30d",
        "Reddit Comments Now",
        "Reddit Comments 1d",
        "Reddit Comments 7d",
        "Reddit Score Now",
        "Reddit Score 1d",
        "Reddit Score 7d",
        "Twitter Followers Now",
        "Twitter Followers 1d",
        "Twitter Followers 7d",
        "Twitter Followers Graph 30d",
        "Twitter Tweets Now",
        "Twitter Tweets 1d",
        "Twitter Tweets 7d",
    ]
