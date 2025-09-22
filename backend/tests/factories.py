"""Factory helpers for tests."""
from __future__ import annotations

import factory
from django.utils import timezone

from accounts.models import User
from blog.models import Comment, Post, Tag


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        skip_postgeneration_save = True

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    display_name = factory.Faker("name")
    bio = factory.Faker("sentence")

    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        pwd = extracted or "s3cretpass"
        self.set_password(pwd)
        if create:
            self.save()


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tag
        skip_postgeneration_save = True

    name = factory.Faker("word")


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post
        skip_postgeneration_save = True

    author = factory.SubFactory(UserFactory)
    title = factory.Faker("sentence", nb_words=6)
    summary = factory.Faker("paragraph")
    content = factory.Faker("paragraph", nb_sentences=5)
    status = Post.PUBLISHED
    published_at = factory.LazyFunction(timezone.now)

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for tag in extracted:
                self.tags.add(tag)
        else:
            self.tags.add(TagFactory())


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment
        skip_postgeneration_save = True

    post = factory.SubFactory(PostFactory)
    author = factory.SubFactory(UserFactory)
    body = factory.Faker("sentence")
    is_public = True
