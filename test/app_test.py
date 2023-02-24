import pytest
from pathlib import Path

from app import app
from database import Database


def test_home_page():
    """test home page exists"""
    tester = app.test_client()
    response = tester.get("/", content_type="html/text")

    assert response.status_code == 200


def test_all_page():
    """test all data page exists"""
    tester = app.test_client()
    response = tester.get("/all", content_type="html/text")

    assert response.status_code == 200


def test_search_page():
    """test search page exists"""
    tester = app.test_client()
    response = tester.get("/search", content_type="html/text")

    assert response.status_code == 200


def test_ranking_page():
    """test ranking page exists"""
    tester = app.test_client()
    response = tester.get("/ranking", content_type="html/text")

    assert response.status_code == 200


def test_magnitude_type_page():
    """test magnitude type page exists"""
    tester = app.test_client()
    response = tester.get("/magnitude_type", content_type="html/text")

    assert response.status_code == 200


def test_404_page():
    """test 404 page exists"""
    tester = app.test_client()
    response = tester.get("/hoge", content_type="html/text")

    assert response.status_code == 404


def test_database():
    """test the database exists"""
    tester = Path("./data/earthquake_data.db").is_file()
    assert tester


def test_cleansing_data_time():
    """test the database exists"""
    db = Database()
    test_data = {
        'time': '2023-02-01T10:20:30.000Z',
        'depth': 15.00,
        'mag': 5.00,
        'magType': 'md',
        'place': '3km NW of Aberdeen, UK',
        'name': 'University of Aberdeen'
    }
    check_data = {
        'time': '01/02/2023 10:20:30',
        'depth': '15.00',
        'mag': '5.00',
        'magType': 'md',
        'place': '3km NW of Aberdeen, UK',
        'name': 'University of Aberdeen'
    }

    assert db.cleansing_data(test_data) == check_data


def test_search_request():
    """test post request for search page """
    tester = app.test_client()
    response = tester.post("/search")

    assert response.status_code == 200


def test_cleansing_data_round_number():
    """test round number of depth and magnitude: round minority second"""
    db = Database()
    test_data = {
        'time': '2023-02-01T10:20:30.000Z',
        'depth': 15.12345,
        'mag': 5.67890,
        'magType': 'md',
        'place': '3km NW of Aberdeen, UK',
        'name': 'University of Aberdeen'
    }
    check_data = {
        'time': '01/02/2023 10:20:30',
        'depth': '15.12',
        'mag': '5.68',
        'magType': 'md',
        'place': '3km NW of Aberdeen, UK',
        'name': 'University of Aberdeen'
    }

    assert db.cleansing_data(test_data) == check_data


def test_cleansing_data_round_number2():
    """test round number of depth and magnitude: increase in digit"""
    db = Database()
    test_data = {
        'time': '2023-02-01T10:20:30.000Z',
        'depth': 15.999,
        'mag': 5.999,
        'magType': 'md',
        'place': '3km NW of Aberdeen, UK',
        'name': 'University of Aberdeen'
    }
    check_data = {
        'time': '01/02/2023 10:20:30',
        'depth': '16.00',
        'mag': '6.00',
        'magType': 'md',
        'place': '3km NW of Aberdeen, UK',
        'name': 'University of Aberdeen'
    }

    assert db.cleansing_data(test_data) == check_data
