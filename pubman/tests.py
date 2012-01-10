"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from pubman import settings

import datetime

from models import Article

class PubmanTest(TestCase):

    fixtures = ['flatpages', 'sites', 'treemenus',]
    
    def setUp(self):
        self.a = Article.objects.create(title="Test a", date_published=datetime.datetime.now()+datetime.timedelta(1,0), publication_stage='P', slug='a-slug')
        self.b = Article.objects.create(title="Test b", date_published=datetime.datetime.now(), publication_stage='P', slug='b')    
        
    def testArticle(self):
        self.assertEquals(self.a.is_published(),False)
        self.assertEquals(self.b.is_published(),True)    
        articles = Article.objects.filter(Article.permission_to_view_Q())
        # Published articles include self.b and the two in the fixtures
        self.assertEquals(articles.count(),1)
        self.assertEquals(articles[0].title,"Test b")

    def testViews(self):
        c = Client()
        response = c.get('/about/')
        self.assertEquals(response.status_code, 200)
        response = c.get('/license/')
        self.assertEquals(response.status_code, 200)        
        response = c.get('/admin/')
        self.assertEquals(response.status_code, 200)
        response = c.get('/story/')
        self.assertEquals(response.status_code, 200)
        response = c.get('/article/b/', follow=True)
        self.assertEquals(response.status_code, 200)        
        response = c.get('/article/1/', follow=True)
        self.assertEquals(response.status_code, 404)
        response = c.get('/article/2/', follow=True)
        self.assertEquals(response.status_code, 200)
        
    
    def testLogin(self):
        User.objects.create(username="joebloggs", email="joebloggs@example.com", password="abcde")
        c = Client()      
        response = c.post('/accounts/login/', {'username': 'joebloggs@example.com', 'password': 'abcde'})
        self.assertEquals(response.status_code, 200)
        response = c.post('/accounts/login/', {'username': 'joebloggs', 'password': 'abcde'})
        self.assertEquals(response.status_code, 200)
        
