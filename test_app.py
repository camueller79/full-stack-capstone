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

        self.test_band = {
            'name': 'testname',
            'city': 'testcity',
            'state': 'MO'
        }

        self.test_album = {
            'title': 'testalbum',
            'band_id': 1
        }

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        pass

    def test_get_bands_success(self):
        test_band = Band(
            name=self.test_band['name'],
            city=self.test_band['city'],
            state=self.test_band['state'])
        test_band.insert()
        res = self.client().get('/bands', headers={
            "Authorization": "Bearer {}".format(self.manager)
        })
        self.assertEqual(res.status_code, 200)
        test_band.delete()

    # test get band failure no permissions
    def test_get_bands_wrong_permissions(self):
        res = self.client().get('/bands')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    # test get albums success
    def test_get_albums_success(self):
        test_album = Album(
            title=self.test_album['title'],
            band_id=self.test_album['band_id'])
        test_album.insert()
        res = self.client().get('/albums', headers={
            "Authorization": "Bearer {}".format(self.manager)
        })
        self.assertEqual(res.status_code, 200)
        test_album.delete()

    # test get albums failure

    def test_get_albums_wrong_permissions(self):
        res = self.client().get('/albums')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    # test post band success
    def test_post_new_band_success(self):
        res = self.client().post('/bands', json=self.test_band, headers={
            "Authorization": "Bearer {}".format(self.manager)
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        Band.query.filter(Band.name == self.test_band['name']).delete()

    # test post band failure (no authorization)
    def test_post_new_band_failure(self):
        res = self.client().post('/bands', json=self.test_band)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    # test post album success
    def test_post_new_album_success(self):
        res = self.client().post('/albums', json=self.test_album, headers={
            "Authorization": "Bearer {}".format(self.manager)
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        Album.query.filter(Album.title == self.test_album['title']).delete()

    # test post album failure
    def test_post_new_album_failure(self):
        res = self.client().post('/albums', json=self.test_album)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    # test patch album success
    def test_patch_album_success(self):
        new_album = Album(
            title=self.test_album['title'],
            band_id=self.test_album['band_id'])
        new_album.insert()

        res = self.client().patch('/albums/{}'.format(new_album.id), json=self.test_album,
                                  headers={"Authorization": "Bearer {}" .format(self.manager)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        new_album.delete()

    # test patch album failure
    def test_patch_album_failure(self):
        res = self.client().patch('/albums/1', json=self.test_album)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    # test patch band success
    def test_patch_band_success(self):
        new_band = Band(
            name=self.test_band['name'],
            city=self.test_band['city'],
            state=self.test_band['state'])
        new_band.insert()

        res = self.client().patch('/bands/{}'.format(new_band.id), json=self.test_band,
                                  headers={"Authorization": "Bearer {}".format(self.manager)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        new_band.delete()

    # test patch band failure
    def test_patch_band_failure(self):
        res = self.client().patch('/bands/1', json=self.test_band)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    # test delete band success
    def test_delete_band_success(self):
        new_band = Band(
            name=self.test_band['name'],
            city=self.test_band['city'],
            state=self.test_band['state'])
        new_band.insert()

        res = self.client().delete('/bands/{}'.format(new_band.id), headers={
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
        new_album = Album(
            title=self.test_album['title'],
            band_id=self.test_album['band_id'])
        new_album.insert()

        res = self.client().delete('/albums/{}'.format(new_album.id), headers={
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
