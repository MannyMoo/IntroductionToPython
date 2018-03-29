#!/usr/bin/env python

'''Solutions to SUPAPYT assignment 2018.'''

from Database import Database

def get_quarters(db) :
    '''Get the list of quarters for entries in the database.'''
    return [attr for attr in db.Entry.attributes() if attr != 'Country']

def cumulative_change(entry, quarters, requireall = False) :
    '''Get the cumulative change in GDP in % for the given database entry and
    quarters. If requireall = True, None will be returned if any of the changes
    for the given quarters is null, else None will be returned if all the 
    changes are null.'''

    # Check for null changes.
    if requireall :
        if any(getattr(entry, quarter) == '' for quarter in quarters) :
            return None
    else :
        if not any(getattr(entry, quarter) != '' for quarter in quarters) :
            return None
        
    return (reduce(lambda x, y : x * (1. + y/100.),
                   (getattr(entry, quarter) for quarter in quarters if getattr(entry, quarter) != ''),
                   1.) - 1.) * 100.

def cumulative_changes(db, quarters) :
    '''Get the cumulative changes for all countries in the database over the 
    given quarters.'''
    
    return [(entry.Country,
             cumulative_change(entry, quarters)) for entry in db.entries]
    
def prob1(db) :
    '''Find the country and quarter with the highest percentage change and that
    with the lowest precentage change. Some countries are missing data for some 
    quarters (the entry for that quarter is blank), so these missing quarters 
    should be ignored.'''
    
    print 'Prob 1:'
    print '    ' + prob1.__doc__
    print

    changeseq = lambda : ({'country' : entry.Country,
                           'quarter' : quarter,
                           'change' : getattr(entry, quarter)} for entry in db.entries \
                          for quarter in get_quarters(db) \
                          if getattr(entry, quarter) != '')
    qmax = max(changeseq(),
               key = lambda data : data['change'])
    qmin = min(changeseq(),
               key = lambda data : data['change'])
    outputstr = 'The {highlow} quarterly percentage change of any country and quarter was {change:.2f} % \
for {country} in {quarter}'
    print outputstr.format(highlow = 'highest', **qmax)
    print outputstr.format(highlow = 'lowest', **qmin)
    print
    
def prob2(db) :
    '''For each quarter, take the average of the changes in GDP across all countries 
    (ignoring blank entries). Find the quarter with the highest average change and 
    the quarter with the lowest average change.'''

    print 'Prob2:'
    print '    ' + prob2.__doc__
    print
    
    means = [{'quarter' : quarter, 'meanchange' : db.mean(quarter)} for quarter in get_quarters(db)]
    maxmean = max(means, key = lambda mean : mean['meanchange'])
    minmean = min(means, key = lambda mean : mean['meanchange'])
    outputstr = 'The quarter with the {highlow} average change is {quarter} at {meanchange:.2f} %'
    print outputstr.format(highlow = 'highest', **maxmean)
    print outputstr.format(highlow = 'lowest', **minmean)
    print

def prob3(db) :
    '''Find the cumulative percentage change for each country. To do so, start with 1 and 
    for each quarter (that isn't blank) multiply it by (1 + change/100). Eg, the first two 
    changes for Greece (GRC) are 0.575928 and 1.69888, so the cumulative change is 
    1 * (1 + 0.575928/100) * (1 + 1.69888/100) = 1.0228, or +2.28 %. Rank each country 
    according to its cumulative change in GDP.'''

    print 'Prob 3:'
    print '    ' + prob3.__doc__
    print

    totals = cumulative_changes(db, get_quarters(db))
    totals.sort(key = lambda total : total[1])
    print 'Cumulative changes:'
    for country, total in totals :
        if total != None :
            print country, '{0:8.2f}'.format(total), '%'
        else :
            print country, 'None'.rjust(10)
    print
    
def prob4(db) :
    '''Calculate the cumulative percentage change in GDP for all countries 
    for quarters up to and including 2006-Q4, and likewise for quarters from 
    2007-Q1 onwards. Rank each country according to the difference between 
    the cumulative changes in the later and earlier time periods. Some countries 
    have no entries prior to 2007, so these countries should be skipped.'''

    print 'Prob 4:'
    print '    ' + prob4.__doc__
    print

    quarters = get_quarters(db)
    quarters.sort()
    # Split the quarters into the earlier and later periods.
    splitquarter = '2007-Q1'
    ilast = quarters.index(splitquarter)
    firstquarters = quarters[:ilast]
    lastquarters = quarters[ilast:]

    # Get the cumulative changes for each period, removing countries with no
    # entries in either period.
    firsttotals = dict(filter(lambda total : total[1] != None, cumulative_changes(db, firstquarters)))
    lasttotals = dict(filter(lambda total : total[1] != None, cumulative_changes(db, lastquarters)))

    # Get the names of the countries that have non-null entries in both periods.
    nonnullcountries = set(firsttotals).intersection(lasttotals)

    # Get the differences in total change for each country between the two periods.
    difftotals = [(country, lasttotals[country] - firsttotals[country]) for country in nonnullcountries]
    difftotals.sort(key = lambda total : total[1])
    print 'Differences in cumulative GDP change before and after', splitquarter, ':'
    print 'Country', 'Pre', splitquarter, '[%]', 'Post', splitquarter, '[%]', 'Diff. [%]'
    for country, diff in difftotals :
        print country.ljust(7), '{0:15.2f}'.format(firsttotals[country]), '{0:16.2f}'.format(lasttotals[country]), '{0:9.2f}'.format(diff)
    print
    
def main() :
    '''Main method. Make the database from the given file and run the problem solutions.'''
    
    problems = (prob1, prob2, prob3, prob4,)

    from argparse import ArgumentParser

    argparser = ArgumentParser()
    argparser.add_argument('fname', default = 'oecd-gdp-pc-change-1997-2017.csv',
                           help = 'Name of the file from which to read the database (default: oecd-gdp-pc-change-1997-2017.csv).')
    argparser.add_argument('problems', nargs = '*', type = int,
                           help = 'Which problems to run (1-{0}, default: all).'.format(len(problems)),
                           default = range(1, len(problems)+1))

    args = argparser.parse_args()

    db = Database()
    with open(args.fname) as fin :
        db.read_from_csv(fin, True)

    for prob in args.problems :
        if prob not in argparser.get_default('problems') :
            raise IndexError('Problems must be in the range ' + str(argparser.get_default('problems')) + '\n'
                             + argparser.format_help())
        problems[prob-1](db)
        
    return locals()

if __name__ == '__main__' :
    globals().update(main())
