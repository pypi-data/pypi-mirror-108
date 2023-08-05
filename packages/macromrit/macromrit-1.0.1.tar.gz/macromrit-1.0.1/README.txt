Hey There!!!

I'm C.Amrit Subramanian
the founder and author of this library

Let me just elucidate you.. about why I was too keen on constructing this.

Firstly..  I'm a student, currently pursuing higher education in Chennai, India... From Amrit Vidyalaya 

Yep.. now hopefully, it's the right time to smash the reasons, why I manufactured this package.

Getting your grooves under the category of python might be simple as proclaimed... But
When it's time to deal with ridiculous challenges like writing files[i.e csv, txt & bin] via python, that's gonna make you run frenzy.

With all due respect, in order to terminate excessive stress and chores from a programmer's life, I conceived this package to make ends meet right and work well mostly, under various aspects and phases.

If you are craving to find a package that could chop off unnecessary lines of code from your tremendous, massive project... Hey, congrats you're at the right destination to achieve your horizon. This is my motto & would certainly try my best to enhance and amplify this library...

Thanks For Supporting...


INSTRUCTIONS TO ABIDE:

    this package consists of 6 functions that you can import and implement
    
    i]write_txt(filename, fillers)
        ->this function help's you to create a txt file and append the elements you wanna, to the file you've provided.
        ->have to enter the file name first.
        ->then enter the string you wanna append in a single go.
    
    ii]read_txt(filename, mode)
        ->this function helps you read the txt file via the read function.
        ->you should input p for printing the content or r for using the content for programming purposes in the function after the filename.
    
    iii]write_csv(filename, total_columns, total_rows)
        ->this function help's you to create a csv file and append the elements you wanna, to the file you've provided.
        ->have to enter the file name first.
        ->then enter the total number of columns you wanna have in your csv file.
        -> enter 0 if you are gonna append to a csv file that already exists else print the no. of columns you wanna have to create a new csv file and write the columns in it.
        ->then enter the total number of rows you wanna write to your csv file.
    
    iv]read_csv(filename, mode)
       ->this function helps you read the csv file list by list.. via reader function from csv.
       ->you should input p for printing the content or r for using the content for programming purposes in the function after the filename.

    v]write_bin(filename, *values)
      ->this function helps you to create and append or direct append to a pickled binary file.
      ->should first provide the file name you wanna create or append elements to.
      ->then write elements one after another with commas separated.. elements might be of whatever datatype you wanna have.

    vi]read_bin(filename, mode)
       ->this function helps you to read a pickled binary file completely.
       ->you should input p for printing the content or r for using the content for programming purposes in the function after the filename.
    
    after downloading the library you should import it using this command: 'import macromrit' or 'from macromrit import <the function you want>'

WHY IS THIS LIBRARY USEFUL & HANDY??:

    _______________________________________________________________________

    normal lines of code to write a txt file:

        with open('filename.txt', 'a') as name:
            print('hello world', file=name)
    
    when you use this library to write a text file:
        
        import macromrit
        macromrit.write_txt('filename.txt', 'hello world')
    _______________________________________________________________________

    normal lines of code to write a csv file with 2 columns and 3 rows:

        import csv
        
        vals = [
        ['name', 'phone'], 
        ['car', 'bike'], 
        ['cycle', 'scooter']
        ]
        
        with open('filename.csv', 'a', newline="") as writer:
            main = csv.writer(writer, delimiter=',')
            main.writerow(['column1', 'column2'])
            main.writerows(vals)

    when you use this library to write a csv file with 2 columns and 3 rows:
        
        import macromrit
        macromrit.write_csv('filename.csv', 2, 3)
    _______________________________________________________________________

    normal lines of code to write a binary file with 5 elements:

        import pickle
        
        x="hello"
        y="hi"
        z="bye"
        a="clown"
        c="pen"

        with open('filename.bin', 'a') as writer:
            pickle.dump(x, writer)
            pickle.dump(y, writer)
            pickle.dump(z, writer)
            pickle.dump(a, writer)
            pickle.dump(c, writer)

    when you use this library to write a binary file with 5 elements:

        import macromrit
        macromrit.write_csv('filename.bin', "hello", "hi", 'bye', 'clown', 'pen')
    _______________________________________________________________________


## THANKS PYTHON ORGANISATION FOR MAKING MY DREAM COME TRUE ##

##########################################################################

cling me via instagram: https://www.instagram.com/amritsubramanian.c/

catch me through email: amritsubramanian.c@gmail.com

grab me on github: https://github.com/macromrit

###########################################################################


thanks for supporting :):):)

Author & Founder of macromrit library |
C.Amrit Subramanian |
a.k.a |
Macromrit |