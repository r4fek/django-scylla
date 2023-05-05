import pytest

from demo.models import Person, Country, Recipe, Address, Library, Author, Book, BenchmarkResults
from mixer.backend.django import mixer

from decimal import Decimal
from datetime import timedelta


ITERATION_COUNT = 3


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
def test_foreign_one_to_one():
    mixer.blend(Address)
    mixer.blend(Library, address=mixer.SELECT)

    # Do these models exist?
    assert Address.objects.all().count() == 1
    assert Library.objects.all().count() == 1

    # Grab author, books
    address = Address.objects.first()
    library = Library.objects.first()

    # Make sure that establishing this relation succeeded.
    assert library.address == address


@pytest.mark.django_db
def test_foreign_one_to_many():
    mixer.blend(Author)
    mixer.cycle(ITERATION_COUNT).blend(Book, libraries=None, author=mixer.SELECT)

    # Do these models exist?
    assert Book.objects.all().count() == ITERATION_COUNT
    assert Author.objects.all().count() == 1

    # Grab author, books
    author = Author.objects.first()
    books = Book.objects.all()

    # Make sure that establishing this relation succeeded.
    author_books = author.book_set.all()

    for book in books:
        assert book in author_books


@pytest.mark.django_db
def test_foreign_many_to_many():
    mixer.blend(Address)
    mixer.cycle(ITERATION_COUNT).blend(Author)
    mixer.cycle(ITERATION_COUNT).blend(Library, address=mixer.SELECT)
    mixer.cycle(ITERATION_COUNT).blend(Book, libraries=None, author=mixer.SELECT)

    # Do these models exist?
    assert Author.objects.all().count() == ITERATION_COUNT
    assert Book.objects.all().count() == ITERATION_COUNT
    assert Library.objects.all().count() == ITERATION_COUNT

    # Grab our libraries and books
    libraries = Library.objects.all()
    books = Book.objects.all()

    # Put every book into every library
    for book in books:
        book.libraries.set(libraries)

    # Ensure that the other side of this relationship has been created and is selectable
    for library in libraries:
        assert library.book_set is not None
        assert books.first() in library.book_set

    # Verify that the relationships have been created appropriately
    for book in books:
        for library in libraries:
            assert library in book.libraries


@pytest.mark.django_db
def test_niche_fields():
    duration_field = timedelta(days=1, seconds=25)
    json_field = '''
        {
            "foo": "bar",
            "baz": { "bleep": 2, "bloop": false }
        }
    '''

    mixer.cycle(ITERATION_COUNT).blend(
        BenchmarkResults,
        runtime=duration_field,
        configuration=json_field
    )

    assert BenchmarkResults.objects.all().count() == ITERATION_COUNT
