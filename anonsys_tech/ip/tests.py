from django.test import TestCase

# Create your tests here.
class ViewTest(TestCase):

    # Test page status
    def test_home(self):
        response = self.client.get('/')
        self.assertContains(response, 'Home Page', 2, 200)

    def test_ip(self):
        response = self.client.get('/ip/')
        print(response.content)
        self.assertContains(response, 'IP Lookup Page', 2, 200)


    def test_contact(self):
        response = self.client.get('/contact/')
        self.assertContains(response, 'Contact Page', 2, 200)
