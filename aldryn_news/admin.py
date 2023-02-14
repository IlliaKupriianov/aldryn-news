# -*- coding: utf-8 -*-
from distutils.version import LooseVersion

import cms
from aldryn_apphooks_config.admin import ModelAppHookConfig, BaseAppHookConfig

from cms.admin.placeholderadmin import FrontendEditableAdminMixin, PlaceholderAdminMixin
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from hvad.admin import TranslatableAdmin

from aldryn_news.cms_appconfig import NewsConfig
from aldryn_news.forms import CategoryForm, NewsForm
from aldryn_news.models import Category, News, Tag, TaggedItem


class NewsAdmin(TranslatableAdmin, FrontendEditableAdminMixin, PlaceholderAdminMixin, admin.ModelAdmin):
    list_display = ['__str__', 'publication_start', 'publication_end', 'all_translations']
    form = NewsForm
    frontend_editable_fields = ('title', 'lead_in')

    def get_fieldsets(self, request, obj=None):
        fieldsets = [
            (None, {'fields': ['title', 'slug', 'category', 'publication_start', 'publication_end']}),
            (None, {'fields': ['key_visual', 'lead_in', 'tags', 'canonical_tag']})
        ]

        # show placeholder field if not CMS 3.0
        if LooseVersion(cms.__version__) < LooseVersion('3.0'):
            fieldsets.append(
                ('Content', {
                    'classes': ['plugin-holder', 'plugin-holder-nopage'],
                    'fields': ['content']}))

        return fieldsets


class CategoryAdmin(TranslatableAdmin):
    form = CategoryForm
    list_display = ['__str__', 'all_translations', 'ordering']
    list_editable = ['ordering']

    def get_fieldsets(self, request, obj=None):
        fieldsets = [
            (None, {'fields': ['name', 'slug']}),
        ]
        return fieldsets


class TaggedItemInline(admin.StackedInline):
    model = TaggedItem


class TagAdmin(TranslatableAdmin):
    list_display = ['__str__', 'all_translations', 'ordering']
    inlines = [TaggedItemInline]
    list_editable = ['ordering']

    def get_fieldsets(self, request, obj=None):
        fieldsets = [
            (None, {'fields': ['name', 'slug']}),
        ]
        return fieldsets


class NewsConfigAdmin(BaseAppHookConfig, admin.ModelAdmin):

    def get_config_fields(self):
        return (
            'paginate_by',
        )

    def get_fieldsets(self, request, obj):
        return [
            (_('Config'), {'fields': self.get_config_fields()})
        ]

admin.site.register(NewsConfig, NewsConfigAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
