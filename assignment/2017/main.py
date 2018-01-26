#!/bin/env python

'''Solutions to SUPAPYT assignment 2017.'''

from Database import Database
from collections import Counter

def make_db(fname, skiplines = '#', readonly = True,
            requiredattrs = ('st_dist', 'pl_name', 'st_teff', 'pl_orbeccen',
                             'pl_disc', 'pl_orbper', 'pl_masse', 'st_mass')) :
    '''Read in a database from the given file, skipping lines beginning with
    'skiplines'. Checks that the db entries have all attributes in 'requiredattrs'.'''
    db = Database()
    # Needs to be opened in binary mode (on Windows).
    with open(fname, 'rb') as finput :
        db.read_from_csv((line for line in finput if not line.startswith(skiplines)),
                         readonly = readonly)
    missingattrs = set(requiredattrs).difference(set(db.Entry.attributes()))
    if missingattrs :
        raise Exception('File ' + fname + ' is missing columns ' + str(list(missingattrs)) + '!')
    return db

def prob1(db) :
    '''Find the closest exoplanet and the farthest exoplanet (using st_dist).'''
    
    print 'Prob 1:'
    print 'Find the closest exoplanet and the farthest exoplanet (using st_dist).'
    print

    distmin = db.min('st_dist')
    distmax = db.max('st_dist')
    print 'Closest:'
    for entry in db.filter(lambda entry : entry.st_dist == distmin) :
        print entry.pl_name.ljust(15), entry.st_dist
    print
    print 'Farthest:'
    for entry in db.filter(lambda entry : entry.st_dist == distmax) :
        print entry.pl_name.ljust(15), entry.st_dist
    print
    
def prob2(db) :
    '''Find the minimum, maximum, and mean of the effective 
    temperatures of the exoplanets (using st_teff).'''

    print 'Prob 2:'
    print 'Find the minimum, maximum, and mean of the effective\n'\
        'temperatures of the exoplanets (using st_teff).'
    print
    db.print_stats('st_teff', '.1f')
    print
    
def prob3(db) :
    '''Find the mean, median and standard deviation of the exoplanets' 
    orbital eccentricity (using pl_orbeccen).'''

    print 'Prob 3:'
    print 'Find the mean, median and standard deviation of the exoplanets\'\n'\
        'orbital eccentricity (using pl_orbeccen).'
    print
    db.print_stats('pl_orbeccen', '.3f')
    print
    
def prob4(db) :
    '''Count how many exoplanets have been found in each year (using pl_disc).'''

    print 'Prob 4:'
    print 'Count how many exoplanets have been found in each year (using pl_disc).'
    print

    desccounter = Counter(db.non_null_iterator('pl_disc'))
    for year in xrange(int(min(desccounter)),
                       int(max(desccounter))+1) :
        print year, desccounter.get(year, 0)
    print
    
def prob5(db) :
    '''Find how many exoplanets there are less than 30 pc away, with effective 
    temperature < 3000 K, and orbital eccentricity < 0.2.'''
    
    print 'Prob 5:'
    print 'How many exoplanets are there less than 30 pc away, with effective\n'\
        'temperature < 3000 K, orbital eccentricity < 0.2?'
    print 
    db = db.filter(lambda entry : entry.st_dist < 30 and entry.st_teff < 3000 and entry.pl_orbeccen < 0.2)
    print len(db.entries)
    for entry in db :
        print '{0:15s} Distance: {1:6.2f} pc, T. eff.: {2:6.1f} K, Orb. ecc.: {3:4.2f}'.format(entry.pl_name,
                                                                                               entry.st_dist,
                                                                                               entry.st_teff,
                                                                                               entry.pl_orbeccen)
    print

def prob6(db) :
    '''For each discovery method (pl_discmethod) find the mean orbital duration 
    (pl_orbper), mean planet mass [Earth masses] (pl_masse) and mean stellar mass 
    [Solar masses] (st_mass).'''
    
    print 'Prob 6:'
    print 'For each discovery method (pl_discmethod) find the mean orbital duration\n'\
        '(pl_orbper), mean planet mass [Earth masses] (pl_masse) and mean stellar mass\n'\
        '[Solar masses] (st_mass)'
    print
    
    discmethods = sorted(set(db.non_null_iterator('pl_discmethod')))
    methoddbs = dict((method, db.filter(lambda entry : entry.pl_discmethod == method)) \
                     for method in discmethods)
    header = '{0:30s} | Mean orbital duration [Earth days] | \
Mean planet mass [Earth masses] | Mean stellar mass [Solar masses]'.format('Discovery method')

    outputlens = tuple(str(len(arg)-2) for arg in header.split('|'))
    lineformat = '{0:30s} | {1:' + outputlens[1] + 's} | {2:' + outputlens[2] + 's} | {3:' + outputlens[3] + 's}'

    print header
    for method in discmethods :
        args = [method]
        methoddb = methoddbs[method]
        for attr, form in ('pl_orbper', '.2f'), ('pl_masse', '.1f'), ('st_mass', '.3f') :
            mean = methoddb.mean(attr)
            if mean != None :
                args.append(('{0:' + form + '}').format(mean))
            else :
                args.append(None)
        print lineformat.format(*args)
    
def main() :
    '''Main method. Make the database from the given file and run the problem solutions.'''
    
    problems = (prob1, prob2, prob3, prob4, prob5, prob6)

    from argparse import ArgumentParser

    argparser = ArgumentParser()
    argparser.add_argument('fname', default = 'planets.csv',
                           help = 'Name of the file from which to read the database (default: planets.csv).')
    argparser.add_argument('problems', nargs = '*', type = int,
                           help = 'Which problems to run (1-{0}, default: all).'.format(len(problems)),
                           default = range(1, len(problems)+1))

    args = argparser.parse_args()
    db = make_db(args.fname)

    for prob in args.problems :
        if prob not in argparser.get_default('problems') :
            raise IndexError('Problems must be in the range ' + str(argparser.get_default('problems')) + '\n'
                             + argparser.format_help())
        problems[prob-1](db)
        
    return locals()

if __name__ == '__main__' :
    globals().update(main())
