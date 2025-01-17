'''
Created on 21 Oct 2013

@author: michael
'''
from django.db import models

from preferences.models import Preferences

from tunobase.poll import models as poll_models

from app.research_tool import models as research_tool_models
from app.discussions import models as discussion_models


class SitePreferences(Preferences):
    __module__ = 'preferences.models'

    active_poll = models.ForeignKey(
        poll_models.PollQuestion,
        related_name='active_polls',
        blank=True,
        null=True
    )
    active_discussion = models.ForeignKey(
        discussion_models.Discussion,
        related_name='active_discussions',
        blank=True,
        null=True
    )
    research_tool = models.ForeignKey(
        research_tool_models.ResearchTool,
        blank=True,
        null=True
    )

    total_users_metric_api_key = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    unique_users_metric_api_key = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    page_views_metric_api_key = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    newsfeed_page_views_metric_api_key = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    registations_metric_api_key = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    comments_metric_api_key = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    likes_metric_api_key = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    research_tool_polls_metric_api_key = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    top_5_articles_page_views_metric_api_key = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    top_5_articles_comments_metric_api_key = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
