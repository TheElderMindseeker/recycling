import pytest

from src import create_app
from src.config import TestConfig
from src.models import db


@pytest.fixture(scope='module')
def client():
    """Test client for Flask WSGI application"""
    app = create_app(TestConfig)
    with app.app_context():
        t_client = app.test_client()
        db.create_all()
        yield t_client
        db.drop_all()


def test_post_recycle(client):
    """Test recycle creation"""
    json_data = {
        'name': 'Recycle 1',
        'address': 'Recycling str, 12',
        'position': 'POINT(0 1)',
        'open_time': '10:00',
        'close_time': '19:00',
        'trash_types': 'plastic&organic&javascript',
        'bonus_program': False,
    }
    response = client.post('/recycles', json=json_data)
    assert response.status_code == 200
