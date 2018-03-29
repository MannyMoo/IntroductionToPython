
# Open the file in read mode.
with open('oecd-gdp-pc-change-1997-2017.csv') as inputfile :
    # Loop over lines in the file.
    for line in inputfile :

        # Split the line by commas, this gives you 
        splitline = line.split(',')

        # The first element in the list is the country name.
        country = splitline[0]

        # Loop over the other elements in the list, which are the
        # percent changes in GDP for that country, and try to
        # convert them from strings to floats.
        changes = []
        for value in splitline[1:] :
            try :
                value = float(value)
            except :
                pass
            changes.append(value)

        # Then we have the name of the country as a string, and a list
        # of the GDP changes as floats.
        print country, changes
