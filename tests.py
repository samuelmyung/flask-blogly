from models import DEFAULT_IMAGE_URL, User
from app import app, db
from unittest import TestCase
import os

os.environ["DATABASE_URL"] = "postgresql:///blogly_test"


# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.drop_all()
db.create_all()


class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        db.session.rollback()

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
        User.query.delete()

        test_user = User(
            first_name="test1_first",
            last_name="test1_last",
            image_url=None,
        )

        db.session.add(test_user)
        db.session.commit()

        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.
        self.user_id = test_user.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_users(self):
        """Testing show list users page"""

        with app.test_client() as c:
            resp = c.get("/users")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("test1_first", html)
            self.assertIn("test1_last", html)

    def test_add_user_form(self):
        """Testing showing the create user form"""

        with app.test_client() as c:
            resp = c.get("/users/new")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("This is add user page button for test", html)

    def test_root_redirect(self):
        """Testing root redirect to users page"""

        with app.test_client() as c:
            resp = c.get("/")
            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, '/users')

    def test_edit_users(self):
        """Testing editing a created user"""

        with app.test_client() as c:
            resp = c.post(f"/users/{self.user_id}/edit", data={
                'first_name': 'testing',
                'last_name': 'test1_last',
                'img_url': DEFAULT_IMAGE_URL,
            })
            self.assertEqual(resp.status_code, 302)         #Follow redirect and test html
            user = User.query.get(self.user_id)
            self.assertEqual(user.first_name, "testing")
            self.assertEqual(user.last_name, "test1_last")
            self.assertEqual(user.image_url, DEFAULT_IMAGE_URL)

    def test_add_users(self):
        """Testing creating a new user"""

        with app.test_client() as c:
            resp = c.post("/users/new", data={
                'first_name': 'test2_first',
                'last_name': 'test2_last',
                'img_url': '',
            })
            self.assertEqual(resp.status_code, 302)
            user = User.query.get(self.user_id + 1)
            self.assertEqual(user.first_name, "test2_first")
            self.assertEqual(user.last_name, "test2_last")
            self.assertEqual(user.image_url, DEFAULT_IMAGE_URL)
