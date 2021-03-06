import json

from django.core.urlresolvers import reverse

from pulseapi.tests import PulseTestCase


class TestEntryView(PulseTestCase):
    def test_get_single_entry_data(self):
        """
        Check if we can get a single entry by its `id`
        """

        id = self.entries[0].id
        response = self.client.get(reverse('entry', kwargs={'pk': id}))
        self.assertEqual(response.status_code, 200)

    def test_post_minimum_entry(self):
        """
        Test posting an entry with minimum amount of content
        """
        payload = self.generatePostPayload(data={'title':'title test_post_minimum_entry'})
        postresponse = self.client.post('/entries/', payload)

        self.assertEqual(postresponse.status_code, 200)

    def test_post_duplicate_title(self):
        """Make sure multiple entries can have the same title"""

        payload = {
            'title': 'title setUp1',
        }
        postresponse = self.client.post('/entries/', data=self.generatePostPayload(data=payload))
        entriesJson = json.loads(str(self.client.get('/entries/').content, 'utf-8'))
        self.assertEqual(postresponse.status_code, 200)
        self.assertEqual(len(entriesJson), 4)

    def test_post_empty_title(self):
        """Make sure entries require a title"""

        payload = {
            'title':''
        }
        postresponse = self.client.post('/entries/', data=self.generatePostPayload(data=payload))
        self.assertEqual(postresponse.status_code, 400)

    def test_post_empty_description(self):
        """Make sure entries require a description"""

        payload = {
            'title': 'title empty description',
            'description': '',
        }
        postresponse = self.client.post('/entries/', data=self.generatePostPayload(data=payload))
        self.assertEqual(postresponse.status_code, 400)

    def test_post_full_entry(self):
        """Entry with all content"""
        payload = {
            'title': 'test full entry',
            'description': 'description full entry',
            'tags': ['tag1', 'tag2'],
            'interest': 'interest field',
            'get_involved': 'get involved text field',
            'get_involved_url': 'http://example.com/getinvolved',
            'thumbnail_url': 'http://example.com/',
            'content_url': 'http://example.com/',
            'internal_notes': 'Some internal notes',
            'featured': True,
            'issues': 'Decentralization',
            'creators': ['Pomax', 'Alan']
        }
        postresponse = self.client.post('/entries/', data=self.generatePostPayload(data=payload))
        self.assertEqual(postresponse.status_code, 200)

    def test_post_entry_with_mixed_tags(self):
        """
        Post entries with some existing tags, some new tags
        See if tags endpoint has proper results afterwards
        """
        payload = {
            'title': 'title test_post_entry_with_mixed_tags2',
            'description': 'description test_post_entry_with_mixed_tags',
            'tags': ['tag2', 'tag3'],
        }
        values = json.loads(str(self.client.get('/nonce/').content, 'utf-8'))
        postresponse = self.client.post('/entries/', data=self.generatePostPayload(data=payload))
        tagList = json.loads(str(self.client.get('/tags/').content, 'utf-8'))
        self.assertEqual(tagList, ['tag1','tag2','tag3'])


    def test_post_entry_with_mixed_creators(self):
        """
        Post entry with some existing creators, some new creators
        See if creators endpoint has proper results afterwards
        """
        payload = {
            'title': 'title test_post_entry_with_mixed_tags2',
            'description': 'description test_post_entry_with_mixed_tags',
            'creators': ['Pomax','Alan'],
        }
        values = json.loads(str(self.client.get('/nonce/').content, 'utf-8'))
        postresponse = self.client.post('/entries/', data=self.generatePostPayload(data=payload))
        creatorList = json.loads(str(self.client.get('/creators/').content, 'utf-8'))
        self.assertEqual(creatorList, ['Pomax','Alan'])

    def test_get_entries_list(self):
        """Get /entries endpoint"""
        entryList = self.client.get('/entries/')
        self.assertEqual(entryList.status_code, 200)

    def test_entries_search(self):
        """Make sure filtering searches works"""
        searchList = self.client.get('/entries/?search=setup')
        entriesJson = json.loads(str(searchList.content, 'utf-8'))
        self.assertEqual(len(entriesJson), 1)

    def test_entries_search(self):
        """Make sure filtering searches by tag works"""
        searchList = self.client.get('/entries/?tag=tag1')
        entriesJson = json.loads(str(searchList.content, 'utf-8'))
        self.assertEqual(len(entriesJson), 1)


    def test_entries_issue(self):
        """test filtering entires by issue"""
        payload = {
            'title': 'title test_entries_issue',
            'description': 'description test_entries_issue',
            'issues': 'Decentralization',
        }
        values = json.loads(str(self.client.get('/nonce/').content, 'utf-8'))
        postresponse = self.client.post('/entries/', data=self.generatePostPayload(data=payload))
        searchList = self.client.get('/entries/?issue=Decentralization')
        entriesJson = json.loads(str(searchList.content, 'utf-8'))
        self.assertEqual(len(entriesJson), 1)

    def test_post_entry_new_issue(self):
        """posting an entry with a new Issue should result in an error. Permission denied?"""
        payload = {
            'title': 'title test_entries_issue',
            'description': 'description test_entries_issue',
            'issues': 'Privacy',
        }
        postresponse = self.client.post('/entries/', data=self.generatePostPayload(data=payload))
        self.assertEqual(postresponse.status_code, 400)

    def test_post_authentication_requirement(self):
        """Make sure you can't post without using the nonce"""
        postresponse = self.client.post('/entries/', data={
            'title': 'title this test should fail',
            'description': 'description this test should fail',
            'tags': ['tag2', 'tag3'],
            'interest': 'interest field',
            'get_involved': 'get involved text field',
            'get_involved_url': 'http://example.com/getinvolved',
            'thumbnail_url': 'http://example.com/',
            'content_url': 'http://example.com/',
            'internal_notes': 'Some internal notes'
        })
        self.assertEqual(postresponse.status_code, 400)
