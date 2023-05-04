import pytest
import pdb

from demo.models import Person, Country, Recipe, Library, Author, Book, BenchmarkResults
from mixer.backend.django import mixer

from decimal import Decimal

ITERATION_COUNT = 1


@pytest.mark.django_db
def test_simple_model_explicit():
    names = [
        "John Connor",
        "Adam 🕵️‍♀️ Savage 👌",
        "P⋶†⋴⅊ ℙ⋀ℛ₭⟃®"
    ]

    for name in names:
        Person.objects.create(name=name)

    results = Person.objects.all()

    # Do we have as many objects as we should?
    assert results.count() == len(names)

    # Are the fields preserved as they should be?
    for result in results:
        assert result.name in names


@pytest.mark.django_db
def test_simple_model_fuzzy():
    mixer.cycle(ITERATION_COUNT).blend(Person)
    assert Person.objects.all().count() == ITERATION_COUNT


@pytest.mark.django_db
def test_small_autofield():
    codes = [
        "USA",
        "GER",
        "JP"
    ]

    for code in codes:
        Country.objects.create(country_code=code)

    results = Country.objects.all()

    # Do we have as many objects as we should?
    assert results.count() == len(codes)


@pytest.mark.django_db
def test_advanced_model_explicit():
    Recipe.objects.create(
        archived=False,
        name="Chitatap",
        author="foobar@foo.bar",

        ingredients_cost=(Decimal(99) / Decimal(7)),
        ingredients_weight=float(16.3333),
        ingredients_count=1,
        instructions="Take a fish and chop it."
    )

    assert Recipe.objects.all().count() == 1


@pytest.mark.django_db
def test_advanced_model_fuzzy():
    mixer.cycle(ITERATION_COUNT).blend(Recipe)

    assert Recipe.objects.all().count() == ITERATION_COUNT


@pytest.mark.django_db
def test_foreign_relations():
    mixer.cycle(ITERATION_COUNT).blend(Author)
    mixer.cycle(ITERATION_COUNT).blend(Library)
    mixer.cycle(ITERATION_COUNT).blend(Book, libraries=None, author=mixer.SELECT)

    libraries = Library.objects.all()

    for book in Book.objects.all():
        book.libraries.set(libraries)

    assert Book.objects.all().count() == ITERATION_COUNT
    assert Book.author in Author.objects.all()
    assert Book.libraries.objects.first() in Library.objects.all()


@pytest.mark.django_db
def test_niche_fields():
    mixer.cycle(ITERATION_COUNT).blend(BenchmarkResults)

    assert BenchmarkResults.objects.all().count() == ITERATION_COUNT
