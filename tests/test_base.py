import unittest
import tutum
import mock
import json
from tutum.api.base import RESTModel


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.pk = RESTModel.pk
        RESTModel.pk = 'uuid'

    def tearDown(self):
        RESTModel.pk = self.pk

    def test_base_init(self):
        model = RESTModel(key1='value1', key2='value2')
        self.assertEqual('value1', model.key1)
        self.assertEqual('value2', model.key2)

    def test_base_setattr(self):
        model = RESTModel()

        setattr(model, 'key', 'value')
        self.assertEqual('value', model.key)
        self.assertEqual(['key'], model.__changedattrs__)

        setattr(model, 'key', 'other value')
        self.assertEqual('other value', model.key)
        self.assertEqual(['key'], model.__changedattrs__)

        setattr(model, 'another_key', 'another_value')
        self.assertEqual('another_value', model.another_key)
        self.assertEqual(['key', 'another_key'], model.__changedattrs__)

    def test_base_getchanges(self):
        model = RESTModel()
        self.assertEqual([], model.__getchanges__())

        model.__changedattrs__ = ['tutum']
        self.assertEqual(['tutum'], model.__getchanges__())

    def test_base_setchanges(self):
        model = RESTModel()
        model.__setchanges__('abc')
        self.assertEqual('abc', model.__changedattrs__)

        model.__setchanges__(None)
        self.assertIsNone(model.__changedattrs__)

    def test_base_loaddict(self):
        model = RESTModel()
        self.assertRaises(AssertionError, model._loaddict, {'key': 'value'})

        model.endpoint = 'fake'
        model._loaddict({'key': 'value'})
        self.assertEqual('value', model.key)
        self.assertEqual('fake/uuid', model._detail_uri)
        self.assertEqual([], model.__getchanges__())

    def test_base_pk(self):
        model = RESTModel()
        self.assertEqual(model.__class__._pk_key(), model.pk)

    def test_base_is_dirty(self):
        model = RESTModel()
        self.assertFalse(model.is_dirty)

        model.key = 'value'
        self.assertTrue(model.is_dirty)

    @mock.patch('tutum.api.base.send_request')
    def test_base_list(self, mock_send_request):
        self.assertRaises(AssertionError, RESTModel.list)
        try:
            kwargs = {'key': 'value'}
            ret_json = {"meta": {"limit": 25, "next": None, "offset": 0, "previous": None, "total_count": 1},
                        "objects": [{"key": "value1"}, {"key": "value2"}]}
            mock_send_request.return_value = ret_json
            RESTModel.endpoint = 'fake'
            models = RESTModel.list(**kwargs)
            mock_send_request.assert_called_with('GET', 'fake', params=kwargs)
            self.assertEqual(2, len(models))
            self.assertIsInstance(models[0], RESTModel)
            self.assertEqual('value1', models[0].key)
            self.assertIsInstance(models[1], RESTModel)
            self.assertEqual('value2', models[1].key)
        finally:
            if hasattr(RESTModel, 'endpoint'):
                delattr(RESTModel, 'endpoint')

    @mock.patch('tutum.api.base.send_request')
    def test_base_fetch(self, mock_send_request):
        self.assertRaises(AssertionError, RESTModel.fetch, 'uuid')

        try:
            ret_json = {"key": "value"}
            mock_send_request.return_value = ret_json
            RESTModel.endpoint = 'fake'
            model = RESTModel.fetch('uuid')
            mock_send_request.assert_called_with('GET', 'fake/uuid')
            self.assertIsInstance(model, RESTModel)
            self.assertEqual('value', model.key)
        finally:
            if hasattr(RESTModel, 'endpoint'):
                delattr(RESTModel, 'endpoint')

    @mock.patch('tutum.api.base.send_request')
    def test_base_save(self, mock_send_request):
        try:
            self.assertTrue(RESTModel().save())

            model = RESTModel()
            model.key = 'value'
            self.assertRaises(AssertionError, model.save)

            RESTModel.endpoint = 'fake'
            mock_send_request.return_value = None
            result = model.save()
            mock_send_request.assert_called_with('POST', 'fake', data=json.dumps({'key': 'value'}))
            self.assertFalse(result)

            mock_send_request.return_value = {'newkey': 'newvalue'}
            result = model.save()
            mock_send_request.assert_called_with('POST', 'fake', data=json.dumps({'key': 'value'}))
            self.assertTrue(result)
            self.assertEqual('newvalue', model.newkey)

            model.key = 'another value'
            mock_send_request.return_value = {'newkey2': 'newvalue2'}
            model._detail_uri = 'fake/uuid'
            result = model.save()
            mock_send_request.assert_called_with('PATCH', 'fake/uuid', data=json.dumps({'key': 'another value'}))
            self.assertTrue(result)
            self.assertEqual('another value', model.key)
            self.assertEqual('newvalue2', model.newkey2)
        finally:
            if hasattr(RESTModel, 'endpoint'):
                delattr(RESTModel, 'endpoint')

    @mock.patch('tutum.api.base.send_request')
    def test_base_refresh(self, mock_send_request):
        try:
            model = RESTModel()
            model.key = 'value'
            self.assertFalse(model.refresh(force=False))

            self.assertRaises(tutum.TutumApiError, model.refresh, force=True)

            RESTModel.endpoint = 'fake'
            model._detail_uri = 'fake/uuid'
            mock_send_request.side_effect = [{'newkey': 'newvalue'}, None]
            self.assertTrue(model.refresh(force=True))
            self.assertEqual('newvalue', model.newkey)
            mock_send_request.assert_called_with('GET', 'fake/uuid')

            self.assertFalse(model.refresh(force=True))
            mock_send_request.assert_called_with('GET', 'fake/uuid')
        finally:
            if hasattr(RESTModel, 'endpoint'):
                delattr(RESTModel, 'endpoint')


    @mock.patch('tutum.api.base.send_request')
    def test_base_delete(self, mock_send_request):
        try:
            model = RESTModel()
            self.assertRaises(tutum.TutumApiError, model.delete)

            RESTModel.endpoint = 'fake'
            model._detail_uri = 'fake/uuid'
            mock_send_request.side_effect = [{'key': 'value'}, None]
            self.assertTrue(model.delete())
            self.assertEqual('value', model.key)
            mock_send_request.assert_called_with('DELETE', 'fake/uuid')

            self.assertTrue(model.delete())
            self.assertIsNone(model._detail_uri)
            self.assertFalse(model.is_dirty)
        finally:
            if hasattr(RESTModel, 'endpoint'):
                delattr(RESTModel, 'endpoint')


    @mock.patch('tutum.api.base.send_request')
    def test_base_perform_action(self, mock_send_request):
        try:
            model = RESTModel()
            self.assertRaises(tutum.TutumApiError, model._perform_action, 'action')

            RESTModel.endpoint = 'fake'
            model._detail_uri = 'fake/uuid'
            mock_send_request.side_effect = [{'key': 'value'}, None]
            self.assertTrue(model._perform_action('action', {'key': 'value'}))
            self.assertEqual('value', model.key)
            mock_send_request.assert_called_with('POST', 'fake/uuid/action', data={'key': 'value'})

            self.assertFalse(model._perform_action('action', {'key': 'value'}))

        finally:
            if hasattr(RESTModel, 'endpoint'):
                delattr(RESTModel, 'endpoint')


    @mock.patch('tutum.api.base.send_request')
    def test_base_expand_attribute(self, mock_send_request):
        model = RESTModel()
        self.assertRaises(tutum.TutumApiError, model._expand_attribute, 'attribute')

        model._detail_uri = 'fake/uuid'
        mock_send_request.side_effect = [{'key': 'value'}, None]
        self.assertEqual('value', model._expand_attribute('key'))

        self.assertIsNone(model._expand_attribute('key'))


    def test_base_create(self):
        self.assertIsInstance(RESTModel.create(), RESTModel)

    def test_base_get_all_attributes(self):
        model = RESTModel()
        model.key = 'value'
        self.assertDictEqual({'key': 'value'}, model.get_all_attributes())