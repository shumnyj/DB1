import psycopg2
# from psycopg2 import sql
from psycopg2.extras import RealDictCursor, DictCursor, NamedTupleCursor

tables = ('books', 'authors', 'publishers')

magic = 'SELECT title, pages, barcode, fname, sname, "exp", written, pub, address, publ, director ' \
        'from books inner join authors on fname=author_fname AND sname=author_sname ' \
        'inner join publishers on pub=pname'


def cast_values(values, types, fields):
    for j, val in enumerate(values):
        if val == '' or val == ' ' or val.lower() == 'null' or val.lower() == 'none':
            values[j] = None
        elif types[j] == 23:
            try:
                values[j] = int(values[j])
            except TypeError:
                print("invalid field value: {}".format(fields[j]))
                return None
                # alert = True
        elif types[j] == 16:
            try:
                values[j] = bool(values[j])
            except TypeError:
                print("invalid field value: {}".format(fields[j]))
                return None
                # alert = True
    return values


def table_choose():
    print('Avalible tables:')
    for i, val in enumerate(tables):
        print('{}: {};'.format(i, val) , end=' ')
    print(' ')
    i = None
    while i is None:
        try:
            i = int(input())
        except TypeError and ValueError:
            print('Please enter valid number')
            i = None
    if i > len(tables)-1 or i < 0:
        print('Wrong value, quitting')
        return None
    else:
        curs.execute('SELECT * FROM ' + tables[i] + ' LIMIT 1')
    return tables[i]


def get_header(info = True):
    ff = curs.description
    hfields = []
    htypes = []
    if ff is not None:
        for column in ff:
            hfields.append(column[0])
            htypes.append(column[1])
        if info is True:
            print('Fields:')
            print(hfields)
            print('Types:')
            print(htypes)
        return hfields, htypes
    else:
        print('Bad cursor')
        return None, None


def db_add():
    # alert = False
    act_table = table_choose()
    if act_table is None:
        return None
    # fields = dict.fromkeys(fields)
    fields, types = get_header()
    values = input('Please, enter values\n')
    values = values.split(',')

    values = cast_values(values, types, fields)
    # com ='INSERT INTO {!s} ({!s}) VALUES ({!r})'.format(tables[i], fields, values)
    if values is not None and len(values) == len(fields):
        com = 'INSERT INTO ' + act_table + ' ('
        for j, val in enumerate(fields):
            if val is not fields[-1]:
                if values[j] is not None:
                    com += '{!s},'.format(val)
            else:
                if values[j] is not None:
                    com += '{!s}) VALUES ('.format(val)
                else:
                    com[-1] = ')'
                    com += ' VALUES ('
        for val in values:
            if val is not values[-1]:
                if val is not None:
                    com += '{!r},'.format(val)
            else:
                if val is not None:
                    com += '{!r})'.format(val)
                else:
                    com[-1] = ')'
        try:
            # com = sql.SQL('INSERT INTO {} ({}) VALUES ({})'.format(sql.Identifier(tables[i]),sql.SQL(',').
            # join(map(sql.Identifier, fields)),sql.SQL(',').join(map(sql.Identifier, values))))
            curs.execute(com)
            connection.commit()
        except psycopg2.IntegrityError and psycopg2.ProgrammingError:
            connection.rollback()
            print('Bad values; Check constraints and try again')
    else:
        print('Incorrect values number')
        connection.rollback()


def db_update():
    act_table = table_choose()
    if act_table is None:
        return None
    fields, types = get_header()
    print('Choose fields to update')
    updating = input().split(',')
    for en in updating:
        en = en.strip()
        try:
            fields.index(en)
        except ValueError:
            print('One or more input fields are invalid')
            connection.rollback()
            return
    print('Enter new field values in the same order')
    values = input().split(',')
    if len(updating) == len(values):
        cond = input('Enter WHERE condition\n')
        com = 'UPDATE ' + act_table + ' SET '
        for i, val in enumerate(updating):
            if types[fields.index(val)] == 23:
                com += '{!s} = {!s},'.format(updating[i], values[i])
            else:
                com += '{!s} = {!r},'.format(updating[i], values[i])
        com = com.rstrip(',')
        com += ' WHERE ' + cond
        try:
            curs.execute(com)
            connection.commit()
        except psycopg2.IntegrityError and psycopg2.ProgrammingError:
            connection.rollback()
            print('Bad values; Check constraints and try again')
    else:
        print('Values count does not match required fields')


def db_remove():
    act_table = table_choose()
    if act_table is None:
        return None
    get_header()
    cond = input('Enter WHERE condition\n')
    com = 'DELETE FROM ' + act_table + ' WHERE ' + cond
    try:
        curs.execute(com)
        connection.commit()
    except psycopg2.IntegrityError and psycopg2.ProgrammingError:
        connection.rollback()
        print('Bad values; Check constraints and try again')


def db_search():
    search_head = 'SELECT title, fname, sname, pages, barcode, exp, written, pub' \
                  ' FROM books INNER JOIN authors' \
                  ' ON fname = author_fname AND sname = author_sname '
    curs.execute(search_head + 'LIMIT 1')
    fields, types = get_header()
    try:
        mode = int(input('Select search type: 1.Range; 2.Enum; 3.Text full; 4.Text exclude;\n'))
    except ValueError:
        print('Bad input')
        return

    if mode == 1:
        print('Enter search field')
        ff = input().strip()
        try:
            i = fields.index(ff)
            if types[i] != 23:
                print("Not numeric")
                connection.rollback()
                return
        except ValueError:
            print('Selected field does not exist')
            connection.rollback()
            return
        try:
            left = int(input('enter lower limit\n'))
            right = int(input('enter upper limit\n'))
        except ValueError:
            print('Not a number!')
            connection.rollback()
            return
        com = search_head + 'WHERE ' + ff + ' BETWEEN ' + str(left) + ' AND ' + str(right)
        curs.execute(com)
        for row in curs:
            print(row)
    elif mode == 2:
        print('Enter search field')
        ff = input().strip()
        try:
            i = fields.index(ff)
            if types[i] != 1043:
                print("Not string")
                connection.rollback()
                return
        except ValueError:
            print('Selected field does not exist')
            connection.rollback()
            return
        com = 'SELECT ' + ff + ' FROM books INNER JOIN authors ' \
              'ON fname = author_fname AND sname = author_sname ' \
              'GROUP BY ' + ff
        curs.execute(com)
        print('Avalible values:')
        for row in curs:
            print(row[0])
        fv = input('Enter value\n')
        com = search_head + 'WHERE ' + ff + ' = ' + '{!r}'.format(fv)
        curs.execute(com)
        for row in curs:
            print(row)
        connection.commit()
    elif mode == 3:
        fv = input('Enter text search values separated by space\n')
        fv = fv.split(' ')
        quer = ''
        for v in fv:
            quer += v + ' & '
        quer = quer[:-3]
        for t in tables:
            com = ''
            curs.execute('SELECT * FROM ' + t + ' LIMIT 1')
            fields, types = get_header(False)
            for i, val in enumerate(types):
                if val == 1043:
                    com += 'coalesce(' + fields[i] + ', \'\') || \' \' || '
            com = com[:-11]
            com = 'SELECT * FROM ' + t + ' WHERE to_tsvector(' \
                  + com + ') @@ to_tsquery(\'english\', \'' + quer + '\')'
            curs.execute(com)
            if curs.rowcount > 0:
                print('In table ' + t)
                for row in curs:
                    print(row)
        connection.commit()
    elif mode == 4:
        fv = input('Enter text search value that entries must not include\n')
        for t in tables:
            com = ''
            curs.execute('SELECT * FROM ' + t + ' LIMIT 1')
            fields, types = get_header(False)
            for i, val in enumerate(types):
                if val == 1043:
                    com += 'coalesce(' + fields[i] + ', \'\') || \' \' || '
            com = com[:-11]
            com = 'SELECT * FROM ' + t + ' WHERE NOT to_tsvector(' \
                  + com + ') @@ to_tsquery(\'english\', \'' + fv + '\')'
            curs.execute(com)
            if curs.rowcount > 0:
                print('In table ' + t)
                for row in curs:
                    print(row)
        connection.commit()
    else:
        print('Bad input')
        return


connection = psycopg2.connect(dbname='testpost', user='shumnyj', password='111', host='localhost')
curs = connection.cursor(cursor_factory=NamedTupleCursor)
p = False
while True:
    print('Select action:\n0: Quit; 1:Add; 2:Remove; 3:Update; 4:Search; 5:Free mode')
    try:
        p = int(input())
    except TypeError and ValueError:
        print('Please enter valid number')
    if p == 0:
        print('exit')
        break
    elif p == 1:
        db_add()
    elif p == 2:
        db_remove()
    elif p == 3:
        db_update()
    elif p == 4:
        db_search()
    elif p == 5:
        c = input()
        try:
            curs.execute(c)
            connection.commit()
        except psycopg2.ProgrammingError:
            print('Invalid command string')
            connection.rollback()
    else:
        print('Please enter valid number')
        p = None

curs.close()
connection.close()
