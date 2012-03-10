
# Plugin Module Skeleton
# Module Name: <name>
# Author Name: <author>
# Contact(opt): <email> <irc> <twitter>
# Description: <description of what module does, how it should be used, ... >
# ----------------------------------------------------------------------------
# Template.py includes most Python libraries you should need
# Try to limit your use of 3rd party libraries as much as possible, you don't know what the target system will have installed
# and it's generally not advisable to install tons of software, libraries, etc on a system you're testing. Anything you install, you usually need to clean up afterwards.

# The modules should not be entire Python scripts. do not include things like #!/usr/bin/python, don't include getopt, argparse, etc
# try to stick to things like sys.argv[1], in general modules that require only one or two arguments if they do require arguments
# ex: ./intersect-custom.py --crackpws <pwfile> <wordlist>
# the creation tool will take the name of your module file ('Module1.fnc') and use the first letter as the getopt parameter
# Since this file is called Module1, we would have ./Intersect-Custom.py -m  OR ./Intersect-Custom.py --module1
# More information coming soon, along with working version of the Payload Generator

# Start of module

def module1():
   
    # this is where you do stuff
    # if your module is larger than one or two functions, make a class
   
    variable = something
    variable1 = something_else

    if variable == 'yes':
        do_some_stuff
        do_other_stuff
	answer = output
        if answer == 'more':
            do_more_stuff
	    print("we did lots of stuff!")
        else:
            print("we're done!")
            function1(answer)
    if not variable == 'yes':
        print("we can't do stuff yet!")
        sys.exit()
      

def function1(answer):

    # do more stuff
    input = answer
    if file exists(input) is True:
        open(input)
        for line in input:
            print("more stuff!")
    if file does not exist(input):
        print("doh!")

