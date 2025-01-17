'''
Created on 18 Dec 2013

@author: michael
'''
from datetime import datetime
from operator import attrgetter

from dateutil.relativedelta import *

from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site

from photon import Client

from tunobase.commenting import models as comment_models
from tunobase.social_media.tunosocial import models as tunosocial_models

from preferences import preferences

from app.root import models as root_models
from app.articles import models as article_models

client = Client(
    server="http://%s/" % Site.objects.get_current().domain,
)


def _push_total_week_month(api_key, total_val, week_val,
                           month_val, change_val):
    client.send(
       samples=(
           ("% Change", change_val),
           ("Past Month", month_val),
           ("Past Week", week_val),
           ("Total", total_val),
       ),
       api_key=api_key,
       timestamp=datetime.now(),
    )


def _push_top_5_articles(api_key, article_list):
    client.send(
       samples=article_list,
       api_key=api_key,
       timestamp=datetime.now(),
    )


def _push_total(api_key, queryset, date_field):
    week_kwargs = {
       '%s__gte' % date_field: timezone.now() + \
           relativedelta(weekday=SU(-1), weeks=-1)
    }
    month_kwargs = {
       '%s__gte' % date_field: timezone.now() + \
           relativedelta(day=1, months=-1),
       '%s__lt' % date_field: timezone.now() + \
           relativedelta(day=1)
    }
    previous_kwargs = {
       '%s__gte' % date_field: timezone.now() + \
           relativedelta(day=1, months=-2),
       '%s__lt' % date_field: timezone.now() + \
           relativedelta(day=1, months=-1)
    }
    total_objects = queryset
    total_objects_past_week = total_objects.filter(
        **week_kwargs
    )
    total_objects_past_month = total_objects.filter(
        **month_kwargs
    )
    total_objects_previous_month = total_objects.filter(
        **previous_kwargs
    )

    total_objects_count = total_objects.count()
    total_objects_past_week_count = total_objects_past_week.count()
    total_objects_past_month_count = total_objects_past_month.count()
    total_objects_previous_month_count = total_objects_previous_month.count()
    try:
        percent_change = ((total_objects_past_month_count - \
                           total_objects_previous_month_count) \
                          / float(total_objects_previous_month_count)) * 100
    except ZeroDivisionError:
        percent_change = 0.0

    _push_total_week_month(
        api_key,
        total_objects_count,
        total_objects_past_week_count,
        total_objects_past_month_count,
        percent_change
    )


def push_total_users():
    API_KEY = preferences.SitePreferences.total_users_metric_api_key

    _push_total(
        API_KEY,
        root_models.Visitor.objects.all(),
        'timestamp'
    )


def push_unique_users():
    API_KEY = preferences.SitePreferences.unique_users_metric_api_key

    _push_total(
        API_KEY,
        root_models.Visitor.objects.filter(unique=True),
        'timestamp'
    )


def push_page_views():
    API_KEY = preferences.SitePreferences.page_views_metric_api_key

    _push_total(
        API_KEY,
        root_models.PageImpression.objects.all(),
        'timestamp'
    )


def push_newsfeed_page_views():
    API_KEY = preferences.SitePreferences.newsfeed_page_views_metric_api_key

    _push_total(
        API_KEY,
        root_models.PageImpression.objects.filter(path__contains='newsfeed'),
        'timestamp'
    )


def push_registrations():
    API_KEY = preferences.SitePreferences.registations_metric_api_key

    _push_total(
        API_KEY,
        get_user_model().objects.all(),
        'date_joined'
    )


def push_comments():
    API_KEY = preferences.SitePreferences.comments_metric_api_key

    _push_total(
        API_KEY,
        comment_models.CommentModel.objects.all(),
        'publish_at'
    )


def push_likes():
    API_KEY = preferences.SitePreferences.likes_metric_api_key

    _push_total(
        API_KEY,
        tunosocial_models.Like.objects.all(),
        'created_at'
    )


def push_research_tool_polls():
    API_KEY = preferences.SitePreferences.research_tool_polls_metric_api_key

    _push_total(
        API_KEY,
        preferences.SitePreferences.research_tool.poll.answers.all(),
        'publish_at'
    )


def push_top_5_articles_page_views():
    API_KEY = preferences.SitePreferences.top_5_articles_page_views_metric_api_key

    article_list = list(article_models.Article.objects.permitted())
    top_5_articles = []
    content_type = ContentType.objects.get_for_model(article_models.Article)
    for article in article_list:
        num_page_impressions = root_models.PageImpression.objects.filter(
            content_type=content_type,
            object_pk=article.pk
        ).count()
        article.num_page_impressions = num_page_impressions

    for article in sorted(
        article_list,
        key=attrgetter('num_page_impressions'))[:5]:

        top_5_articles.append(
            (article.title, article.num_page_impressions)
        )

    _push_top_5_articles(
        API_KEY,
        top_5_articles
    )


def push_top_5_articles_comments():
    API_KEY = preferences.SitePreferences.top_5_articles_comments_metric_api_key

    article_list = list(article_models.Article.objects.permitted())
    top_5_articles = []
    content_type = ContentType.objects.get_for_model(article_models.Article)
    for article in article_list:
        num_comments = comment_models.CommentModel.objects.filter(
            content_type=content_type,
            object_pk=article.pk
        ).count()
        article.num_comments = num_comments

    for article in sorted(
        article_list,
        key=attrgetter('num_comments'))[:5]:

        top_5_articles.append(
            (article.title, article.num_comments)
        )

    _push_top_5_articles(
        API_KEY,
        top_5_articles
    )
