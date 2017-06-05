import feedparser

# class LatestEntriesFeed(Feed, user_url, user_title):
#     title = str(user_title)
#     link = str(user_url)
#     #description = "Updates on changes and additions to police beat central."

#     def items(self):
#         return NewsItem.objects.order_by('-pub_date')[:5]

#     def item_title(self, item):
#         return item.title

#     #def item_description(self, item):
#     #    return item.description

#     # item_link is only needed if NewsItem has no get_absolute_url method.
#     def item_link(self, item):
#         return reverse('news-item', args=[item.pk])


class DashboardFeed(object):

    def __init__(self, url):
        self.url = url

    # feeds =  feedparser.parse(url)

    def fetcher(self):
        feeds = feedparser.parse(self.url)
        self = feeds
        return self
