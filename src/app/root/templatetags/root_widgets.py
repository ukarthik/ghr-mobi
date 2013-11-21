'''
Created on 31 Oct 2013

@author: michael
'''
from copy import copy

from django import template

from tunobase.core import models as core_models

from app.articles import models as article_models
from app.discussions import models as discussion_models

register = template.Library()

@register.inclusion_tag('root/inclusion_tags/home_page_discussion_widget.html', takes_context=True)
def home_page_discussion_widget(context):
    context = copy(context)
    context.update({
        'object_list': discussion_models.Discussion.objects.permitted()[:4],
    })
    return context

@register.inclusion_tag('root/inclusion_tags/home_page_updates_widget.html', takes_context=True)
def home_page_updates_widget(context):
    context = copy(context)
    articles = list(article_models.Article.objects.permitted()[:4])
    galleries = list(core_models.Gallery.objects.permitted()[:4])
    
    context.update({
        'object_list': articles + galleries,
    })
    return context