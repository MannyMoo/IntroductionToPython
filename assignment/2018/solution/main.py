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

    # Loop over the changes, converting them to fractional changes, and calculate
    # the product, ignoring empty entries, then subtract 1 and multiply by 100 to 
    # convert back to percent.
    return (reduce(lambda x, y : x * (1. + y/100.),
                   (getattr(entry, quarter) for quarter in quarters if getattr(entry, quarter) != ''),
                   1.) - 1.) * 100.

def cumulative_changes(db, quarters) :
    '''Get the cumulative changes for all countries in the database over the 
    given quarters.'''
    
    return [{'country' : entry.Country,
             'cumulativechange' : cumulative_change(entry, quarters)} for entry in db.entries]
    
def prob1(db) :
    '''Find the country and quarter with the highest percentage change and that
    with the lowest precentage change. Some countries are missing data for some 
    quarters (the entry for that quarter is blank), so these missing quarters 
    should be ignored.'''
    
    print 'Prob 1:'
    print '    ' + prob1.__doc__
    print

    # Function that returns a generator expression to loop over every country
    # and every quarter in the database and store the country, quarter and
    # change in a dict.
    changeseq = lambda : ({'country' : entry.Country,
                           'quarter' : quarter,
                           'change' : getattr(entry, quarter)} for entry in db.entries \
                          for quarter in get_quarters(db) \
                          if getattr(entry, quarter) != '')

    # Find the max & min changes.
    qmax = max(changeseq(),
               key = lambda data : data['change'])
    qmin = min(changeseq(),
               key = lambda data : data['change'])

    # Use the min & max dicts to format the output string.
    outputstr = 'The {highlow} quarterly percentage change of any country and quarter \
was {change:.2f} % for {country} in {quarter}'
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

    # Get a list of the mean changes per quarter then find the min & max
    means = [{'quarter' : quarter, 'meanchange' : db.mean(quarter)}
             for quarter in get_quarters(db)]
    maxmean = max(means, key = lambda mean : mean['meanchange'])
    minmean = min(means, key = lambda mean : mean['meanchange'])

    # Use the min & max dicts to format the output string.
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

    # Get the cumulative changes for each country and sort them.
    totals = cumulative_changes(db, get_quarters(db))
    totals.sort(key = lambda total : total['cumulativechange'])

    # Use different output strings for non-null & null cumulative changes.
    outputstr = '{country} {cumulativechange:8.2f} %'
    outputstrnull = '{country} {cumulativechange:>10}'
    print 'Cumulative changes:'
    for total in totals :
        if total['cumulativechange'] != None :
            print outputstr.format(**total)
        else :
            print outputstrnull.format(**total)
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
    isplit = quarters.index(splitquarter)
    prequarters = quarters[:isplit]
    postquarters = quarters[isplit:]

    # Get the cumulative changes for each period, removing countries with no
    # entries in either period.
    pretotals = {total['country'] : total['cumulativechange']
                 for total in cumulative_changes(db, prequarters)
                 if total['cumulativechange'] != None}
    posttotals = {total['country'] : total['cumulativechange']
                 for total in cumulative_changes(db, postquarters)
                 if total['cumulativechange'] != None}

    # Get the names of the countries that have non-null entries in both periods.
    nonnullcountries = set(pretotals).intersection(posttotals)

    # Get the differences in total change for each country between the two periods
    # and sort them.
    difftotals = [{'country' : country,
                   'pretotal' : pretotals[country],
                   'posttotal' : posttotals[country],
                   'difftotal' : posttotals[country] - pretotals[country]}
                  for country in nonnullcountries]
    difftotals.sort(key = lambda total : total['difftotal'])

    # Print the output, nicely formatted.
    print 'Differences in cumulative GDP change before and after', splitquarter, ':'
    print
    header = 'Country | Pre {0} [%] | Post {0} [%] | Diff. [%]'.format(splitquarter)
    print header
    print '-' * len(header)
    outputstr = '{country:<7} | {pretotal:15.2f} | {posttotal:16.2f} | {difftotal:9.2f}'
    for total in difftotals :
        print outputstr.format(**total)
    print
    
def main() :
    '''Main method. Make the database from the given file and run the problem solutions.'''
    
    problems = (prob1, prob2, prob3, prob4,)

    from argparse import ArgumentParser

    argparser = ArgumentParser()
    argparser.add_argument('fname', nargs = '?',
                           default = 'oecd-gdp-pc-change-1997-2017.csv',
                           help = 'Name of the file from which to read the database\
 (default: oecd-gdp-pc-change-1997-2017.csv).')
    argparser.add_argument('problems', nargs = '*', type = int,
                           help = 'Which problems to run (1-{0}, default: all).'.format(len(problems)),
                           default = range(1, len(problems)+1))

    args = argparser.parse_args()

    db = Database()
    with open(args.fname) as fin :
        db.read_from_csv(fin, True)

    for prob in args.problems :
        if prob not in argparser.get_default('problems') :
            raise IndexError('Problems must be in the range '
                             + str(argparser.get_default('problems')) + '\n'
                             + argparser.format_help())
        problems[prob-1](db)
        
    return locals()

if __name__ == '__main__' :
    globals().update(main())
