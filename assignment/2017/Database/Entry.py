'''Generic database entry class factory.'''

def tryfloat(val) :
    '''Convert a value to float if possible.'''
    try :
        return float(val)
    except ValueError :
        return val

def class_factory(readonly, attr1, *attrs) :
    '''Make a database entry class with the given attributes. Attributes can
    be given as (name, doc) pairs. If readonly = True the setters for the 
    attributes will be disabled.'''

    attrs = (attr1,) + attrs
    if isinstance(attr1, (tuple, list)) :
        attrs, docs = zip(*attrs)
    else :
        docs = tuple('' for i in xrange(len(attrs)))
                     
    class Entry(object) :
        '''A database entry.'''

        def __init__(self, **attrs) :
            '''Assign the attribute values.'''

            if len(attrs) != len(self.__slots__) :
                raise ValueError('__init__() takes exactly {0} arguments ({1} given)'\
                                 .format(str(len(self.__slots__)+1),
                                         len(attrs) + 1))
                    
            for name, attr in attrs.items() :
                setattr(self, '_' + name, tryfloat(attr))

        @staticmethod
        def attributes() :
            '''Get the attribute names.'''
            return attrs

    Entry.__slots__ = tuple('_' + attr for attr in attrs)
        
    # Generate the properties of the class with getters and setters.
    getterstr = "lambda self : getattr(self, '_{0}')"
    if readonly :
        setterstr = 'None'
    else :
        setterstr = "lambda self, val : setattr(self, '_{0}', tryfloat(val))"

    for attr, doc in zip(attrs, docs) :
        setattr(Entry, attr,
                property(fget = eval(getterstr.format(attr)),
                         fset = eval(setterstr.format(attr)),
                         fdel = None, doc = doc))

    return Entry
