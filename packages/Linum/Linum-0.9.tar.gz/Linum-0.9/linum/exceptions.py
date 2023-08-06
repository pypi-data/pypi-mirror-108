class IntersectionException(Exception):

    def __init__(self, layer: 'Layer', task_part: 'TaskPart'):
        """
        Исключение, вызываемое при попытке добавить на слой пересекающиеся задачи.

        :param layer:
        :param task_part:
        """
        self.task_part = task_part
        self.layer = layer

    def __str__(self):
        return 'SectionIntersectionException: {} in layer {}'.format(self.task_part, self.layer)
