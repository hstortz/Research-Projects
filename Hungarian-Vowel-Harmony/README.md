# Project-kuterbach-stortz

## FILES
corpus_Nk.txt: Text files of Leipzig Hungarian corpora such that N = 10, 30, 100, or 300. The files are word frequencies collected from a corpus containing Nk sentences. Entries are in the  format: key \t word \t frequency. "Words" include proper nouns, fixed multi-word expressions, and special characters. 

hungarian_vh.py: Python file containing program code. The purpose of the program is to rank the participation of individual vowels in Hungarian vowel harmony by determining how consistently they participate in backness harmony, or how neutrally they behave.

vowel_seqs.txt: A blank file that is used by the program to record vowel sequences and frequencies from a corpus file. Vowel sequences are extracted from each word entry (consonants are not copied). "Words" include proper nouns, but not multi-word expressions or special characters. Entries are in the format: vowel sequence \t frequency.

disharmonic.txt: A blank file that is used by the program to record disharmonic words and the frequencies at which they occur from the corpus file. Words are added to the file when format_file() detects that they contain both front and bac vowels as specified by the user. Entries are in the format: word \t frequency.

collapsed.txt: A blank file that is used by the program to record relevant vowels in a vowel sequence, as well as frequency. Vowel sequences and frequencies are copied from vowel_seqs.txt, but non-target neutral vowels are deleted, as well as entries where the length of the vowel sequence is only 1. Entries are in the format: collapsed vowel sequence \t frequency.


## CODE LAYOUT
format_file(): The program first formats the corpus file by creating another file that contains only lowercased vowel sequences and frequencies. For each line in the original file, only vowels and the associated word frequency are copied onto the new vowel_seqs.txt file. Additionally, disharmonic words (words containing both front and back vowels) are copied along with their frequency onto disharmonic.txt.

collapse_neut(): The vowel_seqs.txt file is read, and relevant front/back bigrams are isolated in the vowel sequences. This is accomplished by copying only non-neutral vowels and associatied frequencies to a new collapsed.txt file. When the function is called, a target vowel is passed as an argument, and this target vowel is always preserved regardless of whether or not it is neutral. Additionally, vowel sequences of length 1 are excluded as harmony does not apply.

find_all(): Finds the indices of all non-initial instances of a target vowel within a vowel sequence. These indices are returned as a tuple.

calc_h_score(): calculates the harmony/neutrality score of a target vowel. This function takes the front/back/neutral specifications as arguments, as well as a target vowel to analyze. First, collapse_neut() is called to format the vowel_seqs.txt into a collapsed file, preserving the target vowel. The find_all() function is called to find each non-initial instance of the target vowel within the collapsed sequence. For each instance of the target vowel, the previous vowel is examined to determine whether the vowel bigram is harmonic or disharmonic (or in the case of neutral vowels, to determine whether there is a bias). Variables are incremented based on whether the target vowel occurs after a front or back vowel, and the incrementation value is either 1 or the word frequency depending on the user's specification.
For front/back vowels, the harmony score is a percentage of harmonic over total occurences. For example, a back vowel that occurs 0% after a front vowel and 100% after a back vowel would have a score of 100.00, while a back vowel that occurs 50% after a front vowel and 50% after a back vowel would have a score of 50.00.
For neutral vowels, the score is determined by trigrams rather than bigrams. A neutral Hungarian vowel can occur in both front-harmonic and back-harmonic words. If the trigram is disharmonic (for example, back-neutral-front), it may be that the neutral vowel is truly a front/back vowel that is occuring disharmonically but is spreading features to subsequent vowels. The score is thus determined by dividing the total disharmonic trigrams over total trigrams where the target vowel occurs. For example, a neutral vowel that occurs 0% in disharmonic sequences and 100% in harmonic sequences would have a score of 100.00, while a neutral vowel that occurs 50% in harmonic sequences and 50% in disharmonic sequences would have a score of 50.00.
The higher the score, the more harmonic/neutral the vowel. The score is returned as a float, rounded to two decimal places.

get_ranking(): Scores are calculated for each vowel. A table is then printed for the user to see each vowel and its score given the predefined front/back/neutral division.

prompts(): Prompts the user to specify front/back/neutral feautres for all vowels in the inventory. The user must also select which corpus to analyze, and whether to factor word frequencies into the scores. Error messages will be displayed if: a non-vowel is entered in the feature specification list; not all vowels in the inventory are given features; a vowel is simultaneously placed into two different feature categories. In the case of an error, the user will be asked to start over. Otherwise, the relevant functions will be called to make calculations and print a table according to the user's specifications.

main(): The Hungarian vowel inventory is built into the program and housed in main(). The prompts() function is then called to open the user interface and begin the body of the program. 


## DESIGN DECISIONS
We decided to not include neutral vowels in vowel sequences when determining whether backness harmony is violated. This is because neutral vowels by definition can occur both in front-harmonic words and back-harmonic words. Therefore they are transparent to harmony, i.e. they do not interfere in the application of harmony. Deleting neutral vowels means that the program can evaluate whether the whole string is dis/harmonic, rather than look at vowel bigrams that may include irrelevant neutral vowels.

We also had to decide whether to increment counts of dis/harmony by 1 or by the frequency of the word that the instance was extracted from. We initially decided that the word frequencies were relevant because there is some free variation between harmonic and disharmonic forms of words. In order to capture whether one of these forms is strongly preferred, we had to use word frequencies. As a result, very common words play a larger role in determining a vowel's score than less common words. So the program captured harmony scores in language use overall, as opposed to harmony scores across the lexicon. However, we ultimately decided to give the user the choice between incrementing by 1 or by word frequency to allow the program to be used in a wider array of projects.


## RESOURCES
WortSchatz Leipzig 2019 Hungarian corpora. Word files from 10K, 30K, 100K, and 300K folders.
https://wortschatz.uni-leipzig.de/en/download/Hungarian

Hayes, Bruce, and Zsuzsa Cziráky Londe. "Stochastic phonological knowledge: The case of Hungarian vowel harmony." Phonology 23.1 (2006): 59-104.


## ANALYSIS
In Hungarian vowel harmony (HVH) there are 14 vowels, 6 back vowels (B), 4-5 front vowels(F), and 4-3 neutral vowels(N). Neutral vowels are considered neutral since they can occur in words with both front vowels and back vowels, and they typically do not affect whether the following vowel is front or back. For example, BNB is a perfectly valid vowel sequence, but BNF is considered disharmonic. There are differing opinions on whether the vowel 'e' should be considered a front or a neutral vowel, since it can occur in words with back vowels, but it is also able to govern the backness of the following vowel. 

With this information, our purpose in writing this program was to see if certain vowels are more likely to occur in disharmonic words, and to see if 'e' should be grouped with the front vowels or the neutral vowels. 

Looking at the results we get, if we consider 'e' to be neutral, then we see that it is the least neutral out of the neutral vowels. This is to be expected and the ranking of the neutral vowels follows the 'height effect' (i,í > é > e) described in Hayes and Londe (2006). Only looking at the differences in scores between 'e' being front and 'e' being neutral, the overall scores are very slightly better if 'e' is considered a neutral vowel, but they are not different enough to make a definitive statement. However, when examining the scores of all vowels together, the average score seems to improve when 'e' is classified as a front vowel, particularly the scores of other front vowels such as 'ű', which suggests that 'e' may actually be a front vowel that occurs disharmonically, but which causes subsequent vowels to be front.

In regards to count vs. frequency, the overall scores were slightly lower when using count instead of frequency, but there was not a huge difference. It has been left to the user to decide which type of data is most relevant to their analysis.

Something that could be improved in the future is taking into account the agglutinative nature of Hungarian word formation, and seeing if certain root types + suffixes are more likely to be harmonic or disharmonic. This would require a corpus that includes morphological information. 


