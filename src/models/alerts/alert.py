import uuid

import requests
import src.models.alerts.constants as AlertConstants


class Alert(object):

    def __init__(self, user, price_limit, item, _id=None):
        self.user = user
        self.price_limit = price_limit
        self.item = item
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Alert for {} on item{} with price {}".format(self.user.email, self.item.name, self.price_limit)

    def send(self):
        return requests.post(
            AlertConstants.URL,
            auth=("api", AlertConstants.API_KEY),
            data={
                "from": AlertConstants.FROM,
                "to": self.user.email,
                "subject": "Price limit reached for {}".format(self.item.name),
                "text": "We've found a deal! (link here)"
            }
        )