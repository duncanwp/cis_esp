from django.test import TestCase


class SubsetDatasetTest(TestCase):

    fixtures = ['/datasets/tests/fixtures.json', ]

    def setUp(self):
        initial_data.load()
        for user in User.objects.all():
            profile = Profile.objects.create(user=user)
            profile.save()
        settings.RESTRICT_PACKAGE_EDITORS = False
        settings.RESTRICT_GRID_EDITORS = True

    def test_add_package_view(self):
        url = reverse('add_package')
        response = self.client.get(url)

        # The response should be a redirect, since the user is not logged in.
        self.assertEqual(response.status_code, 302)

        # Once we log in the user, we should get back the appropriate response.
        self.assertTrue(self.client.login(username='user', password='user'))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'package/package_form.html')
        for c in Category.objects.all():
            self.assertContains(response, c.title)
        count = Package.objects.count()
        response = self.client.post(url, {
            'category': Category.objects.all()[0].pk,
            'repo_url': 'http://github.com/django/django',
            'slug': 'test-slug',
            'title': 'TEST TITLE',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Package.objects.count(), count + 1)
