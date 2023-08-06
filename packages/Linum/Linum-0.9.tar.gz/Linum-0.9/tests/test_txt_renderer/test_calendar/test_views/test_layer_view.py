from datetime import date
from unittest import TestCase

from linum.task import Task
from linum.txt_renderer.calendar.views.layer_view import LayerView
from linum.layer import Layer
from linum.task_part import TaskPart


class TestLayerView(TestCase):

    def setUp(self) -> None:
        t = Task('Task 1', date(2020, 1, 30), 4)
        self.tp = TaskPart(t)
        self.tp_before = TaskPart(t, length=2)
        self.tp_after = TaskPart(t, date(2020, 2, 1))

    def test_render_middle_segment(self):
        # Рендер пустого слоя
        layer = Layer()
        self.assertEqual('', LayerView(layer).render_middle_segment())

        # Пустой слой с левой границей
        layer = Layer()
        lw = LayerView(layer)
        lw.left_border = True
        self.assertEqual('│', lw.render_middle_segment())

        # Пустой слой с правой границей
        layer = Layer()
        lw = LayerView(layer)
        lw.right_border = True
        self.assertEqual('│', lw.render_middle_segment())

        # Пустой слой с левой и правой границами
        layer = Layer()
        lw = LayerView(layer)
        lw.right_border = True
        lw.left_border = True
        self.assertEqual('││', lw.render_middle_segment())

        # Пустой слой с внутренними границами
        layer = Layer()
        lw = LayerView(layer)
        lw.inner_borders = True
        self.assertEqual('', lw.render_middle_segment())

        # Слой с задачей до конца месяца
        layer = Layer([self.tp_before])
        lw = LayerView(layer, date(2020, 1, 29), 3)
        self.assertEqual('    │Task 1│', lw.render_middle_segment())

        # Слой с задачей до конца месяца и левой границей
        layer = Layer([self.tp_before])
        lw = LayerView(layer, date(2020, 1, 29), 3)
        lw.left_border = True
        self.assertEqual('│    │Task 1│', lw.render_middle_segment())

        # Слой с задачей до конца месяца и правой границей
        layer = Layer([self.tp_before])
        lw = LayerView(layer, date(2020, 1, 29), 3)
        lw.right_border = True
        self.assertEqual('    │Task 1││', lw.render_middle_segment())

        # Слой с задачей до конца месяца с левой и правой границами
        layer = Layer([self.tp_before])
        lw = LayerView(layer, date(2020, 1, 29), 3)
        lw.right_border = True
        lw.left_border = True
        self.assertEqual('│    │Task 1││', lw.render_middle_segment())

        # Слой с задачей до конца месяца и внутренними границами
        layer = Layer([self.tp_before])
        lw = LayerView(layer, date(2020, 1, 29), 3)
        lw.inner_borders = True
        self.assertEqual('    │Task 1   ', lw.render_middle_segment())

        # Слой с задачей до конца месяца с внутренними границами и левой границей
        layer = Layer([self.tp_before])
        lw = LayerView(layer, date(2020, 1, 29), 3)
        lw.inner_borders = True
        lw.left_border = True
        self.assertEqual('│    │Task 1   ', lw.render_middle_segment())

        # Слой с задачей до конца месяца с внутренними границами и правой границей
        layer = Layer([self.tp_before])
        lw = LayerView(layer, date(2020, 1, 29), 3)
        lw.inner_borders = True
        lw.right_border = True
        self.assertEqual('    │Task 1   │', lw.render_middle_segment())

        # Слой с задачей до конца месяца с внутренними и внешними границами
        layer = Layer([self.tp_before])
        lw = LayerView(layer, date(2020, 1, 29), 3)
        lw.inner_borders = True
        lw.right_border = True
        lw.left_border = True
        self.assertEqual('│    │Task 1   │', lw.render_middle_segment())

