# coding=utf-8
# Stan 2007-10-10, 2012-10-28
"""
*** Библиотека ***
Интерфейс PySide-Db для работы c модулем xlrd
"""
import re                       # регулярные выражения
import xlrd                     # XLS reader


# Возращает значение из ячейки [row, col] листа sh
# Это упрощённая функция и предназначена для использования в пределах этого модуля
def get_value(sh, row, col):
    try:
        cell_type = sh.cell_type(row, col)
        val = None if cell_type == xlrd.XL_CELL_ERROR else sh.cell_value(row, col)
        if isinstance(val, basestring):
            val = val.strip()
    except IndexError:
        val = None
    return val


# Сравнивает ячейку [row, col] в листе sh с регулярным выражением match
# Возращает найденное по шаблону или None при ошибке
def contain_value(sh, row, col, seaching_value):
    val = get_value(sh, row, col)
    if val:
        type1 = type(val)
        type2 = type(seaching_value)
        if type1 != type2:
            try:
                val = type2(val)
            except:
#                 print "search: %s (%s)" % (seaching_value, type(seaching_value))
#                 print "found:  %s (%s)" % (val, type(val))
                return None

        if isinstance(seaching_value, basestring):
            result = re.match(seaching_value, val)
            return result
        else:
            if val == seaching_value:
                return True
            else:
                return False
    return None


# Ищет значение search в листе sh
# Возращает [row, col] если нашёл и None в противном случае
# sh - лист; search - значение для поиска
def search_value(sh, seaching_value):
    for i in xrange(sh.ncols):
        for j in xrange(sh.nrows):
            if contain_value(sh, j, i, seaching_value):
                return j, i
    return None


# Ищет следующие по горизонтали значения после ячейки с текстом start
# можно задать стоп-ячейку с текстом stop
def search_hor_value(sh, formsearch):
    found = []      # массив найденных значений
    hint = ""
    form_len = len(formsearch)

    if form_len == 2:
        [x0, y0] = formsearch
        str = get_value(sh, y0, x0)
        found.append(str)

    elif form_len == 3:
        [x0, y0, pattern] = formsearch
        str = get_value(sh, y0, x0)
        try:
            res = re.match(pattern, str, re.MULTILINE | re.DOTALL)
        except Exception, e:
            print u"Ошибка при выборке данных!"
            print u"Проверьте ячейки, из которой извлекаются данные"
            print u"Возможно, у Вас неправильно настроен шаблон"
            print e
            print u"pattern: %s" % pattern
            print u"str:     %s" % str
            res = None
        if res:
            reslist = res.groups()
            found.append(reslist[0])
        else:
            hint = str

    elif form_len == 7:
        [start, stop, offset, max, min, empty, ml] = formsearch
        xy = search_value(sh, start)
        if xy != None:                  # если start-ячейка найдена
            y0, x0 = y, x = xy          # координаты
            ind = 0                     # длина массива
            if not offset:              # если надо искать со start-ячейки
                str = get_value(sh, y, x)
                res = re.match(r"([^ ]+) {1,}(.+)", str, re.MULTILINE | re.DOTALL)
                # !!! нужно, чтобы отбрасывалось start
                if res:
                    reslist = res.groups()
                    found.append(reslist[1])
                    ind = 1
#               res = re.split(r" {3,}", str)       # для множественного извлечения
#               if res:
#                   found = res[1:]
#                   ind = len(res) - 1
                else:
                    hint = str
            if not ind:                 # если ещё ничего не найдено
                x += offset
                if x < sh.ncols:
                    for x in range(x, sh.ncols):
                        if ind >= max:
                            break
    
                        str = get_value(sh, y, x)
                        if str:
                            if stop:
                                res = re.search(stop, unicode(str))     # проба!!!
                                if res:
                                    break
                            found.append(str)
                            ind += 1
                        else:
                            hint = str

                    for i in range(len(found), max):
                        found.append("")

    else:
        print u"Неправильный formsearch [%s]" % form_len

    return [x0, y0, found] if found else hint
