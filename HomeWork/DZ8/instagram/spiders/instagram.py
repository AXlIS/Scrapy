import scrapy
import re
import json
from scrapy.http import HtmlResponse
from urllib.parse import urlencode
from copy import deepcopy
from HomeWork.DZ8.instagram.items import SubscriberItem, SubscriptionItem


class InstagramSpider(scrapy.Spider):
    with open('inst.json') as f:
        log_data = json.load(f)
    login = log_data['login']
    password = log_data['password']
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['http://instagram.com/']
    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    parse_users = ['veraeremenk0', '_nadtsatyj_']
    graphql_url = 'https://www.instagram.com/graphql/query/?'
    subscriptions_hash = '3dec7e2c57367ef3da3d987d89f9dbc8'
    subscribers_hash = '5aefa9893005572d237da5068082d8d5'

    def parse(self, response: HtmlResponse):
        csrf_token = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(
            self.inst_login_link,
            method='POST',
            callback=self.user_parse,
            formdata={'username': self.login, 'enc_password': self.password},
            headers={'X-CSRFToken': csrf_token}
        )

    def user_parse(self, response: HtmlResponse):
        j_body = json.loads(response.text)
        if j_body['authenticated']:
            for user in self.parse_users:
                yield response.follow(
                    f'/{user}',
                    callback=self.user_data_parse,
                    cb_kwargs={'username': user}
                )

    def user_data_parse(self, response: HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)
        variables = {'id': user_id, 'first': 13, "include_reel": 'true', "fetch_mutual": 'false', }
        url_subscribers = f'{self.graphql_url}query_hash={self.subscribers_hash}&{urlencode(variables)}'
        url_subscriptions = f'{self.graphql_url}query_hash={self.subscriptions_hash}&{urlencode(variables)}'
        yield response.follow(
            url_subscribers,
            callback=self.user_subscribers_parse,
            cb_kwargs={
                'username': username,
                'user_id': user_id,
                'variables': deepcopy(variables)
            }
        )

        yield response.follow(
            url_subscriptions,
            callback=self.user_subscriptions_parse,
            cb_kwargs={
                'username': username,
                'user_id': user_id,
                'variables': deepcopy(variables)
            }
        )

    def user_subscribers_parse(self, response: HtmlResponse, username, user_id, variables):
        data = json.loads(response.text)
        subscribers_info = data.get("data").get("user").get("edge_followed_by").get("page_info")
        if subscribers_info.get("has_next_page"):
            variables["after"] = subscribers_info["end_cursor"]
            url_subscribers = f'{self.graphql_url}query_hash={self.subscribers_hash}&{urlencode(variables)}'
            yield response.follow(
                url_subscribers,
                callback=self.user_subscribers_parse,
                cb_kwargs={'username': username,
                           'user_id': user_id,
                           'variables': deepcopy(variables)
                           }
            )
        subscribers = data.get("data").get("user").get("edge_followed_by").get("edges")
        for subscriber in subscribers:
            yield SubscriberItem(
                status='subscriber',
                user_id=user_id,
                subscriber_id=subscriber.get("node").get("id"),
                subscriber_name=subscriber.get("node").get("username"),
                photo=subscriber.get("node").get("profile_pic_url")
            )

    def user_subscriptions_parse(self, response: HtmlResponse, username, user_id, variables):
        data = json.loads(response.text)
        subscriptions_info = data.get("data").get("user").get("edge_follow").get("page_info")
        if subscriptions_info.get("has_next_page"):
            variables["after"] = subscriptions_info["end_cursor"]
            url_subscriptions = f'{self.graphql_url}query_hash={self.subscriptions_hash}&{urlencode(variables)}'
            yield response.follow(
                url_subscriptions,
                callback=self.user_subscriptions_parse,
                cb_kwargs={'username': username,
                           'user_id': user_id,
                           'variables': deepcopy(variables)
                           }
            )
        subscriptions = data.get("data").get("user").get("edge_follow").get("edges")
        for subscription in subscriptions:
            yield SubscriptionItem(
                status='subscription',
                user_id=user_id,
                subscription_id=subscription.get("node").get("id"),
                subscription_name=subscription.get("node").get("username"),
                photo=subscription.get("node").get("profile_pic_url")
            )

    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')
