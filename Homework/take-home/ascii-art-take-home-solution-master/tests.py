from io import StringIO
from itertools import chain
import unittest
from unittest.mock import patch
from asciiart import Canvas, Rectangle


class TestCanvas(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(width=10, height=10)

    def test_canvas_width_height(self):
        """Test that canvas is initialized with correct width & height."""

        self.assertEqual(self.canvas.width, 10)
        self.assertEqual(self.canvas.height, 10)

    def test_add_shape(self):
        """Test that a shape can be added to the canvas."""

        r = Rectangle(0, 0, 1, 1, '+')
        self.canvas.add(r)

        self.assertIn(r, self.canvas.elements)

    @patch('sys.stdout', new_callable=StringIO)
    def test_render_empty_canvas(self, output):
        """Test that empty canvas is properly rendered."""

        self.canvas.render()

        # print('a')
        # -> 'a\n'
        rows = output.getvalue().rstrip('\n').split('\n')
        # rows = ['          ', '          ', etc]

        self.assertEqual(len(rows), 10)
        self.assertEqual(len(rows[0]), 10)
        self.assertTrue(all(
            [ch == ' ' for ch in chain.from_iterable(rows)]
        ))

    @patch('sys.stdout', new_callable=StringIO)
    def test_render_canvas_one(self, output):
        """Test that canvas with one rectangle is properly rendered."""

        r = Rectangle(0, 0, 1, 1, '+')
        self.canvas.add(r)
        self.canvas.render()

        rows = output.getvalue().rstrip('\n').split('\n')

        self.assertEqual(rows[0], '++        ')
        self.assertEqual(rows[1], '++        ')
        self.assertTrue(all(
            [ch == ' ' for ch in chain.from_iterable(rows[2:])]
        ))

    @patch('sys.stdout', new_callable=StringIO)
    def test_render_canvas_overlap(self, output):
        """Test that canvas renders rectangles that overlap."""

        r1 = Rectangle(0, 0, 1, 1, '+')
        r2 = Rectangle(0, 1, 2, 2, '=')
        self.canvas.add(r1)
        self.canvas.add(r2)
        self.canvas.render()

        rows = output.getvalue().rstrip('\n').split('\n')

        self.assertEqual(rows[0], '++        ')
        self.assertEqual(rows[1], '===       ')
        self.assertEqual(rows[2], '===       ')
        self.assertTrue(all(
            [ch == ' ' for ch in chain.from_iterable(rows[3:])]
        ))

    @patch('sys.stdout', new_callable=StringIO)
    def test_render_canvas_update(self, output):
        """Test that canvas renders properly after updating a shape."""

        r1 = Rectangle(0, 0, 1, 1, '+')
        self.canvas.add(r1)
        r1.translate('x', 1)
        self.canvas.render()

        rows = output.getvalue().rstrip('\n').split('\n')

        self.assertEqual(rows[0], ' ++       ')
        self.assertEqual(rows[1], ' ++       ')
        self.assertTrue(all(
            [ch == ' ' for ch in chain.from_iterable(rows[2:])]
        ))


if __name__ == '__main__':
    unittest.main(verbosity=2)
