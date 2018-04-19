'''Generic database entry class factory.'''

def tryfloat(val) :
    '''Convert a value to float if possible.'''
    try :
        return float(val)
    except ValueError :
        return val

def attr_name(name) :
    '''Replace characters that can't be used in attribute names with '_'.'''
    newname = ''
    for char in name :
        if char.isalnum() :
            newname += char
        else :
            newname += '_'
    return '_' + newname

def get_duplicates(seq) :
    '''Check for duplicates in a sequence.'''
    seen = set()
    duplicates = []
    for obj in seq :
        if obj in seen :
            duplicates.append(obj)
        else :
            seen.add(obj)
    return duplicates

def class_factory(readonly, attr1, *attrs) :
    '''Make a database entry class with the given attributes. Attributes can
    be given as (name, doc) pairs. If readonly = True the setters for the 
    attributes will be disabled.'''

    # Check if they're (name, doc) pairs. If not, set the doc to blank.
    attrs = (attr1,) + attrs
    if isinstance(attr1, (tuple, list)) :
        attrs, docs = zip(*attrs)
    else :
        docs = tuple('' for i in xrange(len(attrs)))

    # Check for duplicates.
    dups = get_duplicates(attrs)
    if dups :
        raise ValueError('Duplicate attributes ' + repr(dups) + ' in\n' + repr(attrs))

    # Get the internal attribute names and make sure there're no duplicates.
    slots = []
    for attr in attrs :
        internattr = attr_name(attr)
        # If there's already an internal attribute with this name, keep adding '_'
        # to the name til it's unique.
        while internattr in slots :
            internattr += '_'
        slots.append(internattr)
    slots = tuple(slots)
    
    # Make the class with the given attributes.
    class Entry(object) :
        '''A database entry.'''

        __slots__ = slots
        _attrs = dict(zip(attrs, slots))
        
        def __init__(self, **attrs) :
            '''Assign the attribute values.'''

            if len(attrs) != len(self.__slots__) :
                raise ValueError('__init__() takes exactly {0} arguments ({1} given)'\
                                 .format(str(len(self.__slots__)+1),
                                         len(attrs) + 1))

            for name, attr in attrs.items() :
                setattr(self, Entry._attrs[name], tryfloat(attr))

        @staticmethod
        def attributes() :
            '''Get the attribute names.'''
            return Entry._attrs.keys()
                    
    # Generate the properties of the class with getters and setters.
    # If readonly is True the setter is None.
    getterstr = "lambda self : getattr(self, '{0}')"
    if readonly :
        setterstr = 'None'
    else :
        setterstr = "lambda self, val : setattr(self, '{0}', tryfloat(val))"

    for attr, internattr, doc in zip(attrs, slots, docs) :
        setattr(Entry, attr,
                property(fget = eval(getterstr.format(internattr)),
                         fset = eval(setterstr.format(internattr)),
                         fdel = None, doc = doc))

    return Entry
