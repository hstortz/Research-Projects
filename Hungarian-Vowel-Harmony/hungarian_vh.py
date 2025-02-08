"""CompLing1 Final Project, Dorothy Kuterbach & Hannah Stortz, SBU Fall 2024

PURPOSE: To rank the active participation of vowels in the Hungarian process of backness harmony.
Statistical analysis intended to determine the consistency of Hungarian vowel harmony,
as well as provide clarity about the status of contested neutral vowels.
Given a vowel inventory, the user will specify vowels for [front]/[back]/[neutral] features.
Prints a table of each vowel, its feature specification, and its percent score in harmony/neutrality.
Also creates a file that contains disharmonic words.
Users can compare results for multiple distributions of vowels/features to determine optimal specification.
Created specifically for analyzing Hungarian backness harmony, but may have applications for other systems of vowel harmony.
"""



### GLOBAL VARIABLES
dashed = "--------------------"


def format_file(filename, vowels, front, back):
    """formats a Leipzig Hungarian Corpus file to include only the vowel sequences of words and their frequency
    input: 
        vowels (str): all vowels in the language
        front (str): all [front] vowels
        back (str): all [back]
        filename (str): a tab-separated file containing
            index
            word
            frequency (descending order)
    return:
        (None): creates two new tab seperated files containing 
            vowel_seqs.txt
                vowel sequence (extracted from word)
                frequency (descending order)
            disharmonic.txt
                words containing both front and back vowels
                frequency (descending order)
    """  
    with open(filename, "r", encoding="utf-8") as f:
        with open("vowel_seqs.txt", "w", encoding="utf-8") as new_f:
            with open("disharmonic.txt", "w", encoding = "utf-8") as dis_f:
        
                for line in f.readlines():
                    fr = False
                    bk = False

                    line = line.split("\t")

                    v_seq = ""
                    invalid = False
                    for char in line[1]:
                        char = char.lower()
                        if char in vowels:
                            v_seq += char
                            if char in front:
                                fr = True
                            elif char in back:
                                bk = True
                        elif char == "-" or char == "," or char == "–":
                            invalid = True
                        
                    if (len(v_seq) != 0) and invalid == False:
                        new_f.write(v_seq + "\t" + line[2])
                        if fr == True and bk == True:
                            dis_f.write(line[1] + "\t" +line[2])
    return


def collapse_neut(neutral, target):
    """makes neutral vowels transparent by deleting non-target neutral vowels; also deletes lines that have a vowel sequence length of 1
    input:
        neutral (str): all neutral vowels
        target (str): the vowel to be preserved
    return:
        (None): creates a new tab-separated file of relevant lines containing
            vowel sequences, minus non-target neutrals (if len > 1)
            frequency (descending order)
    """
    with open("vowel_seqs.txt", "r", encoding = "utf-8") as vf, open("collapsed.txt", "w", encoding = "utf-8") as ff:
        for line in vf:
            line = line.split()
            og_seq = line[0]
            new_seq = ""
            if target in og_seq:
                for v in og_seq:
                    if v == target:
                        new_seq += v
                    elif v not in neutral:
                        new_seq += v
                if len(new_seq) > 1:
                    ff.write(f"{new_seq}\t{line[1]}\n")
    return


def find_all(seq, target):
    """finds all non-initial instances of a target vowel within a vowel sequence
    input:
        seq (str): the string to search
        target (str): the vowel being looked for
    return:
        indices (tuple): a list of the indices of all occurrences of the target vowel in the sequence
    """
    indices = [i for i, char in enumerate(seq) if char == target and i != 0] 
    return tuple(indices)


def calc_h_score(front, back, neutral, target, incl_freq):
    """calculates how actively a given vowel participates in vowel harmony if it is specified as [front]/[back],
    or how neutrally it behaves if it is specified as [neutral]
    input:
        front (str): all [front] vowels
        back (str): all [back] vowels
        neutral (str): all neutral vowels
        target (str): the vowel to be analyzed
        incl_freq (bool): whether to weigh bigram occurrences by word frequency
    return:
        score (float): percent faithfulness to harmony/neutrality, rounded to 2 decimal places
    """
    collapse_neut(neutral, target)
    score = 0
    after_f = after_b = before_f = before_b = fnb = bnf = 0

    with open("collapsed.txt", "r", encoding="utf-8") as f:
        for line in f:
            line = line.split()
            seq, freq = line[0], 1
            if incl_freq == True:
                freq = float(line[1])
            
            indices = find_all(seq, target)
            for i in indices:
                if seq[i-1] in front:
                    after_f += freq
                    if target in neutral and i < len(seq)-1:
                        if seq[i+1] in front:
                            before_f += freq
                        elif seq[i+1] in back:
                            before_b += freq
                            fnb += freq
                elif seq[i-1] in back:
                    after_b += freq
                    if target in neutral and i < len(seq)-1:
                        if seq[i+1] in front:
                            before_f += freq
                            bnf += freq
                        elif seq[i+1] in back:
                            before_b += freq
    
    after_total = after_f + after_b
    before_total = before_f + before_b
    if target in front:
        score = (after_f/after_total)*100
    elif target in back:
        score = (after_b/after_total)*100
    elif target in neutral:
        score = (1-((fnb+bnf)/before_total))*100
        
    return round(float(score), 2)


def get_ranking(vowels, front, back, neutral, incl_freq):
    """prints a table of the harmonic scores of each vowel given a user-defined set of vowel groupings by feature; 
    the user has the option to restart by generating a new set of scores, or to exit the program
    input:
        vowels (str): all vowels in the language
        front (str): all [front] vowels
        back (str): all [back] vowels
        neutral (str): all neutral vowels
        incl_freq (bool): whether to weigh bigram occurrences by word frequency

    return:
        (None): prints a table of vowels, specified features, and scores; loops to prompts() or exits program
    """
    h_scores = [calc_h_score(front, back, neutral, vowel, incl_freq) for vowel in vowels]
    vf_pairs = [f'{vowel} ({"front" if vowel in front else "back" if vowel in back else "neutral"})' for vowel in vowels]
    
    print(dashed)
    print("Harmony and neutrality scores given the provided feature specifications:")
    for vf, score in zip(vf_pairs, h_scores):
        print(str(vf) + "\t" + str(score))
    print(dashed)

    # determine whether to run the program again or quit
    yn_dict = {"y":True, "yes":True, "n":False, "no":False}
    yn = ""
    while yn.strip().lower() not in yn_dict.keys():
        yn = input("Would you like to calculate a new set of scores? (Y/N):\n")
    if yn_dict[yn] == True:
        print(dashed)
        prompts(vowels)
    else:
        return 


def prompts(vowels):
    """prompts the user to specify front/back/neutral features for all vowels in the language,
    as well as which corpus will be analyzed and whether to consider word frequencies in the harmony/neutrality scores;
    includes error messages to make sure all vowels are specified for features exactly once
    input:
        vowels (str): a pre-defined list of all the vowels in the language
    return:
        (None): calls relevant functions to calculate scores given feature specifications
    """
    # collect user specifications of vowel features
    print("Please assign feature specifications by listing (type or copy-paste) relevant vowels. No special characters.")
    fully_specified = False
    while not fully_specified:
        print(f"Vowel inventory: {vowels}")
        front = input("Front vowels:\n").strip().lower()
        back = input("Back vowels:\n").strip().lower()
        neutral = input("Neutral vowels:\n").strip().lower()
        all = front + back + neutral
        
        if set(all).difference(set(vowels)) != set():
            print(f"Error: invalid character\n{dashed}")
            continue
        if set(vowels).difference(set(all)) != set():
            print(f"Error: missing vowels\n{dashed}")
            continue
        if len(all) != len(set(all)):
            print(f"Error: duplicate vowels\n{dashed}")
            continue
        fully_specified = True

    # determine which corpus to analyze
    corpus_sizes = {"10":10, "10k":10, "30":30, "30k":30, "100":100, "100k":100, "300":300, "300k":300}
    selected_size = ""
    while selected_size.strip().lower() not in corpus_sizes.keys():
        selected_size = input("Enter which Leipzig corpus size to analyze (10k, 30k, 100k, 300k):\n")
    format_file(f"corpus_{corpus_sizes[selected_size]}k.txt", vowels, front,back)

    # determine whether to factor word frequencies in the analysis
    yn_dict = {"y":True, "yes":True, "n":False, "no":False}
    yn = ""
    while yn.strip().lower() not in yn_dict.keys():
        yn = input("Would you like to factor word frequencies into the analysis? (Y/N):\n")

    # print a table given the provided information
    get_ranking(vowels, front, back, neutral, yn_dict[yn])
    
    return


def main():
    ### HUNGARIAN VOWEL INVENTORY
    vowels = "aáeéiíoóöőuúüű" 
    
    ### OPEN USER INTERFACE
    prompts(vowels)


if __name__ == "__main__":
    main()