from .bases import BaseFormatter

__all__ = ["IterFormatter", "DefaultFormatter"]


class IterFormatter(BaseFormatter):
    def _format_(self):
        for i in self.data_.data:
            mapper_ = self.column_map if self.column_map else range(len(i.colValues))
            row_ = dict(zip(mapper_, i.colValues))
            row_["name"] = i.coinName
            yield row_

    def __get__(self, instance, owner):
        yield from self._format_()


class DefaultFormatter(IterFormatter):
    def __get__(self, instance, owner):
        """
        Formatter for data from Coin Detective API
        :param instance:
        :param owner:
        :return:
        """
        response = {
            self.key: []
        }
        for i in self._format_():
            response[self.key].append(i)
        return response
