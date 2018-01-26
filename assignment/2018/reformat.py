from csv import DictReader, DictWriter
from collections import defaultdict

countries = defaultdict(dict)
times = set()
with open('original.csv') as f :
    reader = DictReader(f)
    for line in reader :
        countries[line['LOCATION']][line['TIME']] = line['Value']
        times.add(line['TIME'])
        
for country, vals in countries.items() :
    for time in times :
        if not time in vals :
            vals[time] = ''

with open('oecd-gdp-pc-change-1997-2017.csv', 'w') as f :
    writer = DictWriter(f, ['Country'] + sorted(times))
    writer.writeheader()
    for country, vals in countries.items() :
        vals['Country'] = country
        writer.writerow(vals)
