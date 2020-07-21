import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from models import Band, Album, setup_db, db
from app import create_app
import datetime

class BandAlbumRepoTest(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.manager = os.environ.get('MANAGER_KEY')
        self.readonly = os.environ.get('READONLY_KEY')
        setup_db(self.app)
        db.create_all()

        self.new_band = {
            'name': 'Beth Bombara',
            'city': 'St Louis',
            'state': 'MO'
        }

        self.new_album = {
            'title': 'My great album',
            'band_id': 1
        }

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        pass

    def test_get_bands_success(self):
        res = self.client().get('/bands', headers={
            "Authorization": "Bearer {}".format(self.manager)
        })
        self.assertEqual(res.status_code, 200)
    
    # test get band failure no permissions
    def test_get_bands_wrong_permissions(self):
        res = self.client().get('/bands')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    # test get albums success
    def test_get_albums_success(self):
        res = self.client().get('/albums', headers={
            "Authorization": "Bearer {}".format(self.manager)
        })
        self.assertEqual(res.status_code, 200)

    # test get albums failure

    def test_get_albums_wrong_permissions(self):
        res = self.client().get('/albums')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    # test post band success
    def test_post_new_band_success(self):
        res = self.client().post('/bands/add', json = self.new_band, headers = {
            "Authorization": "Bearer {}".format(self.manager)
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    # test post band failure (no authorization)
    def test_post_new_band_failure(self):
        res = self.client().post('/bands/add', json = self.new_band)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    # test post album success
    def test_post_new_album_success(self):
        res = self.client().post('/albums/add', json = self.new_album, headers = {
            "Authorization": "Bearer {}".format(self.manager)
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    # test post album failure
    def test_post_new_album_failure(self):
        res = self.client().post('/albums/add', json = self.new_album)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    # test patch album success
    def test_patch_album_success(self):
        res = self.client().patch('/albums/1', json = self.new_album, headers = {
            "Authorization": "Bearer {}".format(self.manager)
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    # test patch album failure
    def test_patch_album_failure(self):
        res = self.client().patch('/albums/1', json = self.new_album)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    # test patch band success
    def test_patch_band_success(self):
        res = self.client().patch('/bands/1', json = self.new_band, headers = {
            "Authorization": "Bearer {}".format(self.manager)
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    # test patch band failure
    def test_patch_band_failure(self):
        res = self.client().patch('/bands/1', json = self.new_band)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    # test delete band success
    def test_delete_band_success(self):
        res = self.client().delete('/bands/1', headers = {
            "Authorization": "Bearer {}".format(self.manager)
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    # test delete band failure
    def test_delete_band_failure(self):
        res = self.client().delete('/bands/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    # test delete album success
    def test_delete_album_success(self):
        res = self.client().delete('/albums/1', headers = {
            "Authorization": "Bearer {}".format(self.manager)
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    # test delete album failure
    def test_delete_album_failure(self):
        res = self.client().delete('/albums/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

if __name__ == "__main__":
    unittest.main()