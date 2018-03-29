'''Generic database class for statistical analysis.'''

from Entry import class_factory
from csv import DictReader, DictWriter

def median(vals) :
    '''Get the median of a sequence.'''
    vals = sorted(vals)
    if len(vals) == 1 :
        return vals[0]
    if len(vals) %2 == 1 :
        return vals[len(vals)/2 + 1]
    return (vals[len(vals)/2-1] + vals[len(vals)/2])/2

class Database(object) :
    '''Generic database class for statistical analysis.'''

    # Just contains the list of entries, and the class type of the entries.
    __slots__ = ('entries', 'Entry')

    class DBIterator(object) :
        '''Iterator over an attribute of the entries in the database.'''
        __slots__ = ('db', 'attr')
        
        def __init__(self, db, attr) :
            '''Constructor, takes the Database and the name of the attribute 
            over which to iterate.'''
            
            # Just to check that the db Entry class has the given attr,
            # will raise an exception if not.
            getattr(db.Entry, attr)

            self.db = db
            self.attr = attr

        def __iter__(self) :
            '''Iterate over the entries.'''
            return (getattr(entry, self.attr) for entry in self.db.entries)

    class DBNonNullIterator(DBIterator) :
        '''Iterator over entries in the Database with non-null values of 
        a given attribute.'''

        __slots__ = ('null',)
        
        def __init__(self, db, attr, null = '') :
            '''Constructor, takes the Database and the name of the attribute 
            over which to iterate.'''
            Database.DBIterator.__init__(self, db, attr)
            self.null = null
                                
        def __iter__(self) :
            '''Iterate over the entries with non-null values.'''
            return (getattr(entry, self.attr) for entry in self.db.entries \
                    if getattr(entry, self.attr) != self.null)
                     
    def __init__(self, entries = []) :
        '''Constructor. Just takes the list of entries.'''
        self.entries = list(entries)
        # Keep a reference to the class of the entries in the list.
        if entries :
            self.Entry = self.entries[0].__class__
        else :
            self.Entry = None
            
    def read_from_csv(self, datafile, readonly, attrs = None) :
        '''Read from an open file (or other iterable) using csv.DictReader. 
        If attrs is given it defines the names of the columns in the file; 
        if not given the names are taken from the first line in the file.'''

        if not attrs :
            reader = DictReader(datafile)
        else :
            reader = DictReader(datafile, fieldnames = attrs)

        self.Entry = class_factory(readonly, *reader.fieldnames)
        for row in reader :
            self.entries.append(self.Entry(**row))

    def write_to_csv(self, fname) :
        '''Write the db to a file in csv format.'''

        # Needs to be opened in binary mode (on Windows)
        with open(fname, 'bw') as foutput :
            attrs = self.Entry.attributes()
            writer = DictWriter(foutput, attrs)
            writer.writeheader()
            for entry in self :
                writer.writerow({attr : getattr(entry, attr) for attr in attrs})
            
    def iterator(self, attr) :
        '''Get an iterator over an attribute of the entries in the db.'''
        return Database.DBIterator(self, attr)

    def non_null_iterator(self, attr, null = '') :
        '''Get an iterator over an attribute of the entries in the db 
        for entries with non-null values.'''
        return Database.DBNonNullIterator(self, attr, null)
    
    def _stat(self, attr, operation, default = None, null = '') :
        '''Calculate a statistic on the attribute 'attr' using the method
        'operation' on non-null entries in the db. If there're no non-null
        entries, return 'default'.'''
        # Check that there's at least one non-null value in the db.
        if any(True for val in self.non_null_iterator(attr, null)) :
            return operation(self, attr, null)
        return default

    def _mean(self, attr, null) :
        '''Calculate the mean of non-null entries.'''
        n = 0
        mean = 0.
        for val in self.non_null_iterator(attr, null) :
            mean += val
            n += 1
        return mean/n
    
    def mean(self, attr, null = '') :
        '''Calculate the mean of non-null entries. Returns None if there're
        no non-null entries.'''
        return self._stat(attr, Database._mean)

    def _meansq(self, attr, null) :
        '''Calculate the mean of the square of non-null entries.'''
        n = 0
        meansq = 0.
        for val in self.non_null_iterator(attr, null) :
            meansq += val**2.
            n += 1
        return meansq/n
        
    def meansq(self, attr, null = '') :
        '''Calculate the mean of the square of non-null entries. Returns None
        if there're no non-null entries.'''
        return self._stat(attr, Database._meansq, null)

    def stddev(self, attr, null = '') :
        '''Calculate the standard deviation of non-null entries. Returns None
        if there're no non-null entries.'''
        return self._stat(attr,
                          (lambda self, attr, null : \
                           max(self.meansq(attr, null) - self.mean(attr, null)**2, 0.)**.5),
                          null)

    def min(self, attr, null = '') :
        '''Get the minimum of non-null entries. Returns None if there're no 
        non-null entries.'''
        return self._stat(attr,
                          (lambda self, attr, null : min(self.non_null_iterator(attr, null))),
                          null)

    def max(self, attr, null = '') :
        '''Get the maximum of non-null entries. Returns None if there're no 
        non-null entries.'''
        return self._stat(attr,
                          (lambda self, attr, null : max(self.non_null_iterator(attr, null))),
                          null)

    def median(self, attr, null = '') :
        '''Get the median of non-null entries. Returns None if there're no 
        non-null entries.'''
        return self._stat(attr,
                          (lambda self, attr, null : median(self.non_null_iterator(attr, null))),
                          null)

    def stats(self, attr, null = '') :
        '''Get a dict of the min, max, mean, median and standard deviation of
        non-null entries.'''
        return {'min' : self.min(attr, null),
                'max' : self.max(attr, null),
                'mean' : self.mean(attr, null),
                'median' : self.median(attr, null),
                'stddev' : self.stddev(attr, null)}

    def print_stats(self, attr, form = None) :
        '''Print the min, max, mean, median and standard deviation of non-null 
        entries. Optionally provide a formatting string, eg '4.2f'.'''
        if form :
            form = '{0:' + form + '}'
        else :
            form = '{0}'
        stats = self.stats(attr)
        for attr in 'min', 'max', 'mean', 'median', 'stddev' :
            print attr.ljust(6), ':', form.format(stats[attr])
            
    def sort(self, attr) :
        '''Sort the entries according to the value of the given attribute.'''
        self.entries.sort(key = lambda entry : getattr(entry, attr))

    def filter(self, test) :
        '''Return a Database of entries satisfying the method 'test'.'''
        return Database(filter(test, self.entries))

    def __iter__(self) :
        '''Iterate over entries in the db.'''
        return iter(self.entries)
