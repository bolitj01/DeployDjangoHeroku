from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Todo
import json

# Tests directly on the Todo model
class TodoModelTests(TestCase):
    
    # This method will run before every test
    def setUp(self):
        # Sample todo data and user
        self.test_title = 'Test Todo'
        self.test_description = 'Test Description'
        self.test_completed = False
        self.test_user = User.objects.create_user(username='testuser', password='12345')

    def test_create_todo(self):
        # Create a Todo item for testing
        Todo.objects.create(
            title=self.test_title,
            description=self.test_description,
            completed=self.test_completed,
            user=self.test_user
        )
        
        # Get the Todo item from the database
        todo = Todo.objects.get(title=self.test_title)
        
        """Test the Todo model can create a todo item."""
        self.assertEqual(todo.title, self.test_title)
        self.assertEqual(todo.description, self.test_description)
        self.assertEqual(todo.completed, self.test_completed)
        self.assertEqual(todo.user, self.test_user)

    def test_todo_string(self):
        """Test the string representation of the Todo model."""
        # Create a Todo item
        todo = self.todo = Todo.objects.create(
            title=self.test_title,
            description=self.test_description,
            completed=self.test_completed,
            user=self.test_user
        )
        self.assertEqual(str(todo), 'Test Todo')

    def test_todo_unique_title(self):
        """Test that the Todo title must be unique."""
        with self.assertRaises(Exception):
            # First todo
            Todo.objects.create(
                title=self.test_title,
                description=self.test_description,
                completed=self.test_completed,
                user=self.test_user
            )
            # Second todo with the same title
            Todo.objects.create(
                title=self.test_title,
                description=self.test_description,
                completed=self.test_completed,
                user=self.test_user
            )

    def test_delete_user_deletes_todo(self):
        """Test that deleting a user deletes their todos."""
        Todo.objects.create(
            title=self.test_title,
            description=self.test_description,
            completed=self.test_completed,
            user=self.test_user
        )
        self.assertEqual(Todo.objects.count(), 1)
        self.test_user.delete()
        self.assertEqual(Todo.objects.count(), 0)
        
# Tests on the Todo views
class TodoViewTests(TestCase):
    
    def setUp(self):
        # Sample todo data and user
        self.test_title = 'Test Todo'
        self.test_description = 'Test Description'
        self.test_completed = False
        self.test_user = User.objects.create_user(
            username='testuser', password='12345')
        self.client.post(reverse('login'), 
            {'username': 'testuser', 'password': '12345'})
        
    def tearDown(self):
        self.client.post(reverse('logout'))
        
    def test_create_todo(self):
        # Test creating a new todo
        response = self.client.post(reverse('create_todo'), {
            'title': self.test_title,
            'description': self.test_description,
            'completed': self.test_completed,
        })
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Todo.objects.filter(
            title=self.test_title).exists())
        
    def test_todos_mv_list(self):
        # Create a Todo - todo-list POST
        response = self.client.post(reverse('todo-list'), {
            'title': self.test_title,
            'description': self.test_description,
            'completed': self.test_completed,
        })
        self.assertEqual(response.status_code, 201)
        # Create another Todo
        response = self.client.post(reverse('todo-list'), {
            'title': 'Another Todo',
            'description': 'Another Description',
            'completed': True,
        })
        self.assertEqual(response.status_code, 201)
        # Get the list of todos - todo-list GET
        response = self.client.get(reverse('todo-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Todo.objects.count(), 2)
        
        
    def test_todo_mv_detail(self):
        # Create a Todo
        Todo.objects.create(
            title=self.test_title,
            description=self.test_description,
            completed=self.test_completed,
            user=self.test_user
        )
         # Prepare the data as a JSON string
        data = json.dumps({
            'title': self.test_title,
            'description': 'Updated Description',
            'completed': True,
            'user': self.test_user.id
        })

        # Update a Todo - make sure to set content_type='application/json'
        response = self.client.put(reverse('todo-detail', 
                    args=[self.test_title]), data, content_type='application/json')
        self.assertEqual(response.status_code, 200)

        # Get the updated Todo - todo-detail GET
        response = self.client.get(reverse('todo-detail', args=[self.test_title]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['description'], 'Updated Description')

        # Delete a Todo - todo-detail DELETE
        response = self.client.delete(reverse('todo-detail', args=[self.test_title]))
        self.assertEqual(response.status_code, 204)
        self.assertCountEqual(Todo.objects.all(), [])
        
    def test_toggle_completed(self):
        # Create a Todo
        Todo.objects.create(
            title=self.test_title,
            description=self.test_description,
            completed=self.test_completed,
            user=self.test_user
        )
        # Toggle the completed status of a Todo
        data = json.dumps({'title': self.test_title})
        response = self.client.put(reverse('toggle_complete'), data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Todo.objects.get(title=self.test_title).completed)