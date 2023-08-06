#!/usr/bin/env python
# -*- coding: utf-8 -*-


from . import orm_exceptions
from .filter import Filter


__author__ = 'James Iter'
__date__ = '2021/4/16'
__contact__ = 'james.iter.cn@gmail.com'
__copyright__ = '(c) 2021 by James Iter.'


class ORM(object):

    _table_name = None
    _primary_key = None
    _db = None

    def __init__(self):
        pass

    @classmethod
    def init_db_adaptor(cls, db=None):
        cls._db = db

    @property
    def fields(self):
        return vars(self).keys()

    @classmethod
    def check_field(cls, field=None):
        fields = list()

        if isinstance(field, (str, bytes)):
            assert field in cls.fields
            fields.append(field)

        if isinstance(field, (tuple, list)):
            for item in field:
                assert item in cls.fields
                fields.append(field)

        return fields

    @classmethod
    def get_mapped_columns(cls, fields=None, except_fields=None):
        if fields is None:
            fields = cls.fields

        fields = cls.check_field(field=fields)

        if except_fields is not None:
            except_fields = cls.check_field(field=except_fields)
            fields = [item for item in fields if item not in except_fields]

        return ', '.join(fields)

    def create(self):
        sql_stmt = ("INSERT INTO " + self._table_name + " (" +
                    ', '.join(filter(lambda _key: _key != self._primary_key, self.fields)) +
                    ") VALUES (" +
                    ', '.join(['%({0})s'.format(key)
                               for key in filter(lambda _key: _key != self._primary_key, self.fields)]) + ")")

        cnx = self._db.cnxpool.get_connection()
        cursor = cnx.cursor(dictionary=True, buffered=True)

        try:
            cursor.execute(sql_stmt, self.__dict__)
            self.__setattr__(self._primary_key, cursor.lastrowid)
            cnx.commit()

        finally:
            cursor.close()
            cnx.close()

    def update(self):
        if not self.exist():
            raise orm_exceptions.NotExist

        sql_stmt = ("UPDATE " + self._table_name + " SET " +
                    ', '.join(['{0} = %({0})s'.format(key)
                               for key in filter(lambda _key: _key != self._primary_key, self.fields)]) +
                    " WHERE " + '{0} = %({0})s'.format(self._primary_key))

        cnx = self._db.cnxpool.get_connection()
        cursor = cnx.cursor(dictionary=True, buffered=True)
        try:
            cursor.execute(sql_stmt, self.__dict__)
            cnx.commit()

        finally:
            cursor.close()
            cnx.close()

    def delete(self):
        if not self.exist():
            raise orm_exceptions.NotExist

        sql_stmt = ("DELETE FROM " + self._table_name + " WHERE " + '{0} = %({0})s'.format(self._primary_key))

        cnx = self._db.cnxpool.get_connection()
        cursor = cnx.cursor(dictionary=True, buffered=True)

        try:
            cursor.execute(sql_stmt, self.__dict__)
            cnx.commit()

        finally:
            cursor.close()
            cnx.close()

    def get(self, fields=None, except_fields=None):
        mapped_columns = self.get_mapped_columns(fields=fields, except_fields=except_fields)

        sql_stmt = ("SELECT " + mapped_columns + " FROM " + self._table_name +
                    " WHERE " + '{0} = %({0})s'.format(self._primary_key) +
                    " LIMIT 1")

        cnx = self._db.cnxpool.get_connection()
        cursor = cnx.cursor(dictionary=True, buffered=True)

        try:
            cursor.execute(sql_stmt, self.__dict__)
            row = cursor.fetchone()

        finally:
            cursor.close()
            cnx.close()

        if isinstance(row, dict):
            self.__dict__ = row
        else:
            raise orm_exceptions.NotExist

    def exist(self):
        sql_stmt = ("SELECT " + self._primary_key + " FROM " + self._table_name +
                    " WHERE " + '{0} = %({0})s'.format(self._primary_key) + " LIMIT 1")

        cnx = self._db.cnxpool.get_connection()
        cursor = cnx.cursor(dictionary=True, buffered=True)

        try:
            cursor.execute(sql_stmt, self.__dict__)
            row = cursor.fetchone()

        finally:
            cursor.close()
            cnx.close()

        if isinstance(row, dict):
            return True

        return False

    def get_by(self, field, fields=None, except_fields=None):
        sql_field = ''

        if isinstance(field, (str, bytes)):
            assert field in self.fields
            sql_field = field + ' = %(' + field + ')s'

        if isinstance(field, (tuple, list)):
            fields = list()

            for item in field:
                assert item in self.fields
                fields.append(item + ' = %(' + item + ')s')

            sql_field = ' AND '.join(fields)

        mapped_columns = self.get_mapped_columns(fields=fields, except_fields=except_fields)
        sql_stmt = ("SELECT " + mapped_columns + " FROM " + self._table_name + " WHERE " + sql_field + " LIMIT 1")

        cnx = self._db.cnxpool.get_connection()
        cursor = cnx.cursor(dictionary=True, buffered=True)

        try:
            cursor.execute(sql_stmt, self.__dict__)
            row = cursor.fetchone()

        finally:
            cursor.close()
            cnx.close()

        if isinstance(row, dict):
            self.__dict__ = row
        else:
            raise orm_exceptions.NotExist

    def exist_by(self, field):
        sql_field = ''

        if isinstance(field, (str, bytes)):
            assert field in self.fields
            sql_field = field + ' = %(' + field + ')s'

        if isinstance(field, (tuple, list)):
            fields = list()

            for item in field:
                assert item in self.fields
                fields.append(item + ' = %(' + item + ')s')

            sql_field = ' AND '.join(fields)

        sql_stmt = ("SELECT " + self._primary_key + " FROM " + self._table_name + " WHERE " + sql_field + " LIMIT 1")

        cnx = self._db.cnxpool.get_connection()
        cursor = cnx.cursor(dictionary=True, buffered=True)

        try:
            cursor.execute(sql_stmt, self.__dict__)
            row = cursor.fetchone()

        finally:
            cursor.close()
            cnx.close()

        if isinstance(row, dict):
            return True

        return False

    @staticmethod
    def get_filter_keywords():
        # 指定参与过滤的关键字及其数据库对应字段类型
        """
        使用示例
        return {
            'name': FilterFieldType.STR.value,
            'remark': FilterFieldType.STR.value,
            'age': FilterFieldType.INT.value
        }
        """
        raise NotImplementedError()

    @classmethod
    def get_by_filter(cls, offset=0, limit=1000, order_by=None, order='asc', filter_str='', fields=None,
                      except_fields=None):
        if order_by is None:
            order_by = cls._primary_key

        assert isinstance(offset, int)
        assert isinstance(limit, int)
        assert order_by in cls.fields
        assert order in ['asc', 'desc']

        mapped_columns = cls.get_mapped_columns(fields=fields, except_fields=except_fields)

        sql_stmt = ("SELECT " + mapped_columns + " FROM " + cls._table_name + " ORDER BY " + order_by + " " + order +
                    " LIMIT %(offset)s, %(limit)s")
        sql_stmt_count = ("SELECT count(" + cls._primary_key + ") FROM " + cls._table_name)

        where_str = Filter.filter_str_to_sql(allow_keywords=cls.get_filter_keywords(), filter_str=filter_str)
        if where_str != '':
            sql_stmt = ("SELECT " + mapped_columns + " FROM " + cls._table_name + " WHERE " + where_str +
                        " ORDER BY " + order_by + " " + order + " LIMIT %(offset)s, %(limit)s")
            sql_stmt_count = ("SELECT count(" + cls._primary_key + ") FROM " + cls._table_name + " WHERE " + where_str)

        cnx = cls._db.cnxpool.get_connection()
        cursor = cnx.cursor(dictionary=True, buffered=True)

        try:
            cursor.execute(sql_stmt, {'offset': offset, 'limit': limit})
            rows = cursor.fetchall()
            cursor.execute(sql_stmt_count)
            count = cursor.fetchone()
            return rows, count["count(" + cls._primary_key + ")"]

        finally:
            cursor.close()
            cnx.close()

    @classmethod
    def get_mapping_by_filter(cls, key=None, **kwargs):
        if key is None:
            key = cls._primary_key

        assert key in cls.fields

        rows, _ = cls.get_by_filter(**kwargs)

        mapping = dict()

        for row in rows:
            value_of_key = row[key]

            if value_of_key not in mapping:
                mapping[value_of_key] = row

            elif isinstance(mapping[value_of_key], dict):
                mapping[value_of_key] = [mapping[value_of_key]]
                mapping[value_of_key].append(row)

            elif isinstance(mapping[value_of_key], list):
                mapping[value_of_key].append(row)

        return mapping

    @staticmethod
    def get_allow_update_keywords():
        # 指定允许批量更新的字段
        """
        使用示例
        return ['remark', 'age']
        """
        raise NotImplementedError()

    @classmethod
    def update_by_filter(cls, kv, filter_str=''):
        # 过滤掉不予支持批量更新的字段
        _kv = {}
        for k, v in kv.iteritems():
            if k in cls.get_allow_update_keywords():
                _kv[k] = v

        if _kv.__len__() < 1:
            return

        # set_str = ', '.join(map(lambda x: x + ' = %(' + x + ')s', _kv.keys()))
        # 上面为通过map实现的方式
        set_str = ', '.join(['{0} = %({0})s'.format(key) for key in _kv.keys()])
        where_str = Filter.filter_str_to_sql(allow_keywords=cls.get_filter_keywords(), filter_str=filter_str)

        if where_str.__len__() == 0:
            raise orm_exceptions.LimitNone

        sql_stmt = ("UPDATE " + cls._table_name + " SET " + set_str + " WHERE " + where_str)

        cnx = cls._db.cnxpool.get_connection()
        cursor = cnx.cursor(dictionary=True, buffered=True)

        try:
            cursor.execute(sql_stmt, _kv)
            cnx.commit()

        finally:
            cursor.close()
            cnx.close()

    @classmethod
    def delete_by_filter(cls, filter_str=''):
        where_str = Filter.filter_str_to_sql(allow_keywords=cls.get_filter_keywords(), filter_str=filter_str)

        if where_str.__len__() == 0:
            raise orm_exceptions.LimitNone

        sql_stmt = ("DELETE FROM " + cls._table_name + " WHERE " + where_str)

        cnx = cls._db.cnxpool.get_connection()
        cursor = cnx.cursor(dictionary=True, buffered=True)

        try:
            cursor.execute(sql_stmt)
            cnx.commit()

        finally:
            cursor.close()
            cnx.close()

    @staticmethod
    def get_allow_content_search_keywords():
        # 指定允许全文检索的字段
        """
        使用示例
        return ['name', 'remark']
        """
        raise NotImplementedError()

    @classmethod
    def content_search(cls, offset=0, limit=1000, order_by=None, order='asc', filter_str='', keyword='', fields=None,
                       except_fields=None):
        if order_by is None:
            order_by = cls._primary_key

        assert isinstance(offset, int)
        assert isinstance(limit, int)
        assert order_by in cls.fields
        assert order in ['asc', 'desc']

        mapped_columns = cls.get_mapped_columns(fields=fields, except_fields=except_fields)

        _kv = dict()
        _kv = _kv.fromkeys(cls.get_allow_content_search_keywords(), '%{0}%'.format(keyword))

        where_str = ' OR '.join([k + ' LIKE %(' + k + ')s' for k in _kv.keys()])

        filter_str = Filter.filter_str_to_sql(allow_keywords=cls.get_filter_keywords(), filter_str=filter_str)

        if filter_str != '':
            where_str = filter_str + ' AND (' + where_str + ')'

        sql_stmt = ("SELECT " + mapped_columns + " FROM " + cls._table_name + " WHERE " + where_str +
                    " ORDER BY " + order_by + " " + order + " LIMIT %(offset)s, %(limit)s")
        sql_stmt_count = ("SELECT count(" + cls._primary_key + ") FROM " + cls._table_name + " WHERE " + where_str)

        _kv.update(**{'offset': offset, 'limit': limit})
        cnx = cls._db.cnxpool.get_connection()
        cursor = cnx.cursor(dictionary=True, buffered=True)

        try:
            cursor.execute(sql_stmt, _kv)
            rows = cursor.fetchall()
            cursor.execute(sql_stmt_count, _kv)
            count = cursor.fetchone()
            return rows, count["count(" + cls._primary_key + ")"]

        finally:
            cursor.close()
            cnx.close()

    @classmethod
    def get_all(cls, order_by=None, order='asc', fields=None, except_fields=None):
        if order_by is None:
            order_by = cls._primary_key

        assert order_by in cls.fields
        assert order in ['asc', 'desc']

        mapped_columns = cls.get_mapped_columns(fields=fields, except_fields=except_fields)
        sql_stmt = ("SELECT " + mapped_columns + " FROM " + cls._table_name + " ORDER BY " + order_by + " " + order)
        sql_stmt_count = ("SELECT count(" + cls._primary_key + ") FROM " + cls._table_name)

        cnx = cls._db.cnxpool.get_connection()
        cursor = cnx.cursor(dictionary=True, buffered=True)

        try:
            cursor.execute(sql_stmt)
            rows = cursor.fetchall()
            cursor.execute(sql_stmt_count)
            count = cursor.fetchone()
            return rows, count["count(" + cls._primary_key + ")"]

        finally:
            cursor.close()
            cnx.close()

    @classmethod
    def distinct_by(cls, fields=None, order_by=None, order='asc'):
        if order_by is None:
            order_by = cls._primary_key

        assert isinstance(fields, list)
        assert order_by in cls.fields
        assert order in ['asc', 'desc']

        for field in fields:
            assert field in cls.fields

        sql_stmt = ("SELECT DISTINCT " + ', '.join(fields) + " FROM " + cls._table_name +
                    " ORDER BY " + order_by + " " + order)

        cnx = cls._db.cnxpool.get_connection()
        cursor = cnx.cursor(dictionary=True, buffered=True)

        try:
            cursor.execute(sql_stmt)
            rows = cursor.fetchall()
            return rows, rows.__len__()

        finally:
            cursor.close()
            cnx.close()

