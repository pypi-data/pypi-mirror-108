from unittest import TestCase

from linum.txt_renderer.base.border import Border


class TestBorder(TestCase):

    def test__add__(self):
        # Сложение с самим собой
        b = Border()
        self.assertEqual(b, b + b)
        b.left = True
        self.assertEqual(b, b + b)
        b.right = True
        self.assertEqual(b, b + b)
        b.top = True
        self.assertEqual(b, b + b)
        b.bottom = True
        self.assertEqual(b, b + b)

        # Сложение разных границ
        lb = Border(l=True)
        rb = Border(r=True)
        lrb = lb + rb
        self.assertEqual(Border(l=True, r=True), lrb)
        tb = Border(t=True)
        bb = Border(b=True)
        tbb = tb + bb
        self.assertEqual(Border(t=True, b=True), tbb)
        self.assertEqual(Border(l=True, r=True, t=True, b=True), lrb + tbb)

    def test__sub__(self):
        # Вычитание с самим собой
        b = Border()
        self.assertEqual(Border(), b - b)
        b.left = True
        self.assertEqual(Border(), b - b)
        b.right = True
        self.assertEqual(Border(), b - b)
        b.top = True
        self.assertEqual(Border(), b - b)
        b.bottom = True
        self.assertEqual(Border(), b - b)

        # Вычитание разных границ
        lb = Border(l=True)
        rb = Border(r=True)
        lrb = lb + rb
        self.assertEqual(lb, lrb - rb)
        self.assertEqual(rb, lrb - lb)
        tb = Border(t=True)
        bb = Border(b=True)
        tbb = tb + bb
        self.assertEqual(tb, tbb - bb)
        self.assertEqual(bb, tbb - tb)
