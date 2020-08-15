#Joel Feddes
#This program will analyze user-text, or text from a csv file, and tell you if its positively or negatively associated basd on the text's adjectives.

def analyze_text(user_text,sentiments):    #analyze user text to see if it can be found in the sentiments dictionary
                                            # if it is, figure out if it has a multiplier or if it is alone.
    user_text = user_text.lower().strip()   #Lowercase and strip text
    parts = user_text.split(" ")            #split text into parts to be analyzed
    result = 0
    for i,part in enumerate(parts):         #Assign the parts to a specific position (i being rank, part being word)
        part = remove_punct(part)
        multiplier = 1                      #initiate multiplier to 1 to begin with.
        contribution = 0
        if part in sentiments:              #check to see if the word is a word in the sentiments library
            score = sentiments[part]        #since the word is here, find the associated score
            if i > 0:                       
                word_before = parts[i-1]    #check if the word "not" is one place infront of the word we're looking at
                                            #if it is, make adjustments to the score
                if word_before == "not":
                    multiplier = -1
                    contribution = contribution + (score * multiplier)
                    result = result + contribution
                    if contribution != 0:
                        print("%-15s%10.4f%10.4f%10.4f" % (part,score,multiplier,contribution))
                        
                elif word_before in ["very","really","totally","extremely","super"]:
                    multiplier = 2
                    contribution = contribution + (score * multiplier)
                    result = result + contribution
                    if contribution != 0:
                        print("%-15s%10.4f%10.4f%10.4f" % (part,score,multiplier,contribution))
                          
                elif word_before in ["slightly","pretty","mildly","somewhat"]:
                    multiplier = 0.5
                    contribution = contribution + (score * multiplier)
                    result = result + contribution
                    if contribution != 0:
                        print("%-15s%10.4f%10.4f%10.4f" % (part,score,multiplier,contribution))   

                elif word_before == "too":
                    multiplier = -0.5
                    contribution = contribution + (score * multiplier)
                    result = result + contribution
                    if contribution != 0:
                        print("%-15s%10.4f%10.4f%10.4f" % (part,score,multiplier,contribution))   
                  
                else:
                    contribution = contribution + (score * multiplier)
                    result = result + contribution
                    if contribution != 0:
                        print("%-15s%10.4f%10.4f%10.4f" % (part,score,multiplier,contribution))
            if i > 1:
                word_before_before = parts[i-2] 
                if word_before_before == "not": #Condition for "not" before 2 spaces ahead of the adjective. Not working :'(
                    multiplier = -1
                    contribution = contribution + (score * multiplier)
                    result = result + contribution
                    if contribution != 0:
                        print("%-15s%10.4f%10.4f%10.4f" % (part,score,multiplier,contribution))
            if i ==0: #Instance where the first word could be an adjective (like in the shinyhappy.txt file)
                contribution = contribution + (score * multiplier)
                result = result + contribution
                if contribution != 0:
                    print("%-15s%10.4f%10.4f%10.4f" % (part,score,multiplier,contribution))
    return result #return overall score!

def print_analysis_heading():
    print("\n%s" % "*** Analysis ***".center(45))
    print("%-15s%10s%10s%10s" % ("Word","Score","Mult", "Contrib"))
    print("-" * 45)
    
def judge_sentiments(text_score):           #Judge_sent. will calculate the rating of a specified text-based input. 
    result = ""
    if text_score < -0.5:
        return "negative"
    elif text_score < 0:
        return "slightly negative"
    elif text_score == 0:
        return "neautral"
    elif text_score < 0.5:
        return "slightly positive"
    else:
        return "positive"
    
        
def read_sentiments(fname):     #Create function to analyze the sentiments file.
    result = {}                 #Store the adjectives in emmpty library
    fvar = open(fname,"r")
    for line in fvar:
        line = line.strip()
        if line != "" and line[0] != "#":   #only look at lines that ARENT empty and DONT start with a #.
                                            #Lines beginning with a # are comment lines.
            parts = line.split("\t")        #split line into parts by the tabs
            for part in parts:              
                if "#a" in part:            #analyze and look at only lines with #a involved (#a denotes an adjective).
                    adjective = parts[0][:-2]   #Select the first string in parts, then select only the part of the string without the #a at the end.
                    score = float(parts[1])     #float-ify score associated with the adjective-value.
                    result[adjective] = score   #result[adjective] = score. So, when I implement adjective "key",
                                                #it leads me to the value associated with it (score).
    fvar.close()
    return result 

def remove_punct(adjective):    #Function created to remove punction. I want bad NOT bad,. I prefer good commas.
    if "," in adjective:
        adjective = adjective[:-1]
    elif "'" in adjective:
        adjective = adjective[:-1]
    elif ";" in adjective:
        adjecctive = adjective[:-1]
    elif ":" in adjective:
        adjective = adjective[:-1]
    elif "!" in adjective:
        adjective = adjective[:-1]
    elif "." in adjective:
        adjective = adjective[:-1]
    elif "?" in adjective:
        adjective = adjective[:-1]
    elif "-" in adjective:
        adjective = adjective[:-1]
    else:
        adjective = adjective
    return adjective

def read_text_file(text_file):  #This function allows us to read through a text-based, space-seperated, file. 
    result = []                 #I want to create a list of the words in the text file.
    fvar = open(text_file,"r")  #Open the text_file in read.
    for line in fvar:           #Look through each line in the file.
        line = line.strip().lower()    #Strip the crap off and lowercase
        parts = line.split(" ") #Split the lines into parts by the spaces
        result.extend(parts)    #Extend the result list. Not append, I want one list. Not a list, list, list etc.
    fvar.close()
    return result #Return list of words in the file.

def analyze_text_file(text_list,sentiments):    #This function analyzes the list of words I fouond from the text_file.
    result = 0 #Total score
    for i,part in enumerate(text_list): #Do as we did in the prior function. I could've probably have done some adjusting
                                        #and cut this sucker down into 1 function instead of two massive ones.
                                        #but here we are.
        part = part.lower()
        part = remove_punct(part)       #Remove any punctuation before we check if its in sentiments.
        contribution = 0  
        multiplier = 1
        if part in sentiments:          #Check if the word is in our library (sentiments)
            score = sentiments[part]    #it is? Give me that score!
            if i > 0:
                word_before = text_list[i-1]    #rest below is the same deal as above.
                if word_before == "not":
                    multiplier = -1
                    contribution = contribution + (score * multiplier)
                    result = result + contribution
                    if contribution != 0:
                        print("%-15s%10.4f%10.4f%10.4f" % (part,score,multiplier,contribution))
                elif word_before in ["very","really","totally","extremely","super"]:
                    multiplier = 2
                    contribution = contribution + (score * multiplier)
                    result = result + contribution
                    if contribution != 0:
                        print("%-15s%10.4f%10.4f%10.4f" % (part,score,multiplier,contribution))
                          
                elif word_before in ["slightly","pretty","mildly","somewhat"]:
                    multiplier = 0.5
                    contribution = contribution + (score * multiplier)
                    result = result + contribution
                    if contribution != 0:
                        print("%-15s%10.4f%10.4f%10.4f" % (part,score,multiplier,contribution))   

                elif word_before == "too":
                    multiplier = -0.5
                    contribution = contribution + (score * multiplier)
                    result = result + contribution
                    if contribution != 0:
                        print("%-15s%10.4f%10.4f%10.4f" % (part,score,multiplier,contribution))  
                else:
                    contribution = contribution + (score * multiplier)
                    result = result + contribution
                    if contribution != 0:
                        print("%-15s%10.4f%10.4f%10.4f" % (part,score,multiplier,contribution))
            if i > 1:
                word_before_before = text_list[i-2]
                if word_before_before == "not":
                    multiplier = -1
                    contribution = contribution + (score * multiplier)
                    result = result + contribution
                    if contribution != 0:
                        print("%-15s%10.4f%10.4f%10.4f" % (part,score,multiplier,contribution))
            if i ==0:   #account for the first word, if it is an adjective.
                contribution = contribution + (score * multiplier)
                result = result + contribution
                if contribution !=0:
                    print("%-15s%10.4f%10.4f%10.4f" % (part,score,multiplier,contribution))
                    
    return result #return the goods!

#main

fname = input("Enter in the sentiments.txt file: ")
sentiments = read_sentiments(fname) #Create a dictionary containing the adjectives called sentiments.
go_again = input("What would you like to do?\n1. Analyze a single tweet\n2. analyze a file\n3. Exit\nEnter the number of your choice: ").strip()
#Ask user what action they want to perform^

while go_again == "1" or "2":   #While user wants to do something relevant, let them.
    if go_again == "1":         #Instance where user wants to find the rating of a tweet.
        rating = ""             #reset rating after each run.
        tweet_score = 0
        user_text = input("Enter text to analyze: ")        #Ask user for the tweet. Hand typed.
        print_analysis_heading()                            
        text_score = analyze_text(user_text,sentiments)   #Calculate and print the score of each word in the tweet and calculate the total score of the tweet.
        rating = judge_sentiments(text_score)              #Based on the tweet_score, determine if the tweet is a positive, negative, or somewhere inbetwee, tweet.
        print("\nWith a score of %0.4f, the text is judged %s." % (text_score,rating))
        go_again = input("\nWhat would you like to do?\n1. Analyze a single tweet\n2. analyze a file\n3. Exit\nEnter the number of your choice: ").strip()
        #Ask user if they want to go again.^

    elif go_again == "2":   #Instance where user wants to finds the rating of a text-based, space-seperted, file.
        rating = ""         #Reset rating after each run.
        text_score = 0
        text_file = input("Enter the name of the file to analyze: ")  #Ask user for the name of the text-based file they want to evaluate.
        text_list = read_text_file(text_file)   #Creates a list of the words in the text-file.
        print_analysis_heading()
        text_score = analyze_text_file(text_list,sentiments)    #Calculate the score for each word in the file and print it.
                                                                #Also calculate the total score, but don't print yet.
        rating = judge_sentiments(text_score)                   #Based on the total score, determine the rating.
        print("\nWith a score of %0.4f, the file is judged %s." % (text_score,rating))    #Print total score of file.
        go_again = input("\nWhat would you like to do?\n1. Analyze a single tweet\n2. analyze a file\n3. Exit\nEnter the number of your choice: ").strip()
        #allow user to do another action or quit.^

    else:
        break
