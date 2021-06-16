'''
CS 331 Programming Assignment 3
Submission by: Matthew Jaobsen & Jackson Miller
'''
import sys, re, math
r = re.compile('[^a-zA-Z0-9! ]')

''' print_cool_message()
    no further explanation needed
'''
def print_cool_message():
    print("\n\n__________________________________\n\n")

''' make_vocab():
    create an array of all words in 'trainingSet.txt'
    substitute all characters that are not a-z, A-Z, or ' ' with ''
    split line into arrray if it is not the classlabel
    make lowercase, sort, return
'''
def make_vocab():
    vocab = []
    with open('trainingSet.txt') as training:
        for line in training:
            line = r.sub(' ',line)
            l = [w for i, w in enumerate(line.split()) if i != len(line)]
            vocab += [w.lower() for w in l if w.lower() not in vocab]
    vocab.sort()
    return vocab

''' process(input_file,output_file,vocab):
        iterate through vocab, print all words seperated by comma
        throw 'classlabel' at end
        iterate through training file
        substitute all characters that are not a-z, A-Z, or ' ' with ' '
        split line into array
        pop last value as that is pos/neg review
        if word in line array is in vocab place a '1,' otherwise '0,'
        finish with tab followed by review rating
'''
def process(input_file,output_file,vocab):
    open(output_file, 'w').close()
    sys.stdout = open(output_file, 'w')
    for word in vocab:
         print(word + ",", end='')
    print("classlabel")
    with open(input_file) as training:
        for line in training:
            line = r.sub(' ',line)
            l = line.split()
            review = l.pop()
            for word in vocab:
                if word in l:
                    print("1,", end='')
                else:
                    print("0,", end='')
            print(review)
    sys.stdout = sys.__stdout__

''' tally_totals():
        open preprocessed train
        increment 4 arrays based on table:
            positive    |   word_present
            True            True
            True            False
            False           True
            False           False
        count total_positive
        count total_negative
'''
def tally_totals(word_and_pos,word_and_neg,none_and_pos,none_and_neg,total_pos,total_neg):
    with open("preprocessed_train.txt", 'r') as data:
        for line in data:
            if re.search('[1]$',line):
                l = line.split(',')
                for index, val in enumerate(l):
                    if val == "1":
                        word_and_pos[index] = word_and_pos[index] + 1
                    elif val == "0":
                        none_and_pos[index] = none_and_pos[index] + 1
                total_pos+=1
            elif re.search('[0]$',line):
                l = line.split(',')
                for index, val in enumerate(l):
                    if val == "1":
                        word_and_neg[index] = word_and_neg[index] + 1
                    elif val == "0":
                        none_and_neg[index] = none_and_neg[index] + 1
                total_neg+=1
    return((total_pos, total_neg))

''' probs(4 arrays,total_pos,total_neg,count):
        iterate through length of vocab
        for each array at index i:
            calculate p(X=u | Y =v):
                # of records with X=u and Y=v + 1 /
                # of records with Y=v + 2
'''
def probs(word_and_pos,word_and_neg,none_and_pos,none_and_neg,total_pos,total_neg,count):
    for i in range(0,count):
        word_and_pos[i] = math.log((word_and_pos[i] + 1) / (total_pos + 2))
        word_and_neg[i] = math.log((word_and_neg[i] + 1) / (total_neg + 2))
        none_and_pos[i] = math.log((none_and_pos[i] + 1) / (total_pos + 2))
        none_and_neg[i] = math.log((none_and_neg[i] + 1) / (total_neg + 2))

''' guess(4 arrays, ratio_positive, ratio_negative, test_file):
        for each line in the test data besides top line:
            place into an array, prob_pos = 0, prob_neg = 0, review = popped list
            for each val in the line:
                if word present calculate word and pos,neg * pos/neg unless its first one
                else calculate no word and pos,neg * pos,neg unless its first one
            pos = pos * pos_ratio
            neg = neg * neg_ratio
            if pos >= neg: positive review and check
            else: negative, and check
'''
def guess(word_and_pos,word_and_neg,none_and_pos,none_and_neg,ratio_pos,ratio_neg,test,train_name,test_name):
    total_correct = 0
    count = 0
    with open(test, 'r') as data:
        for line in data:
            if count > 0:
                l = line.split(',')
                positive = 0
                negative = 0
                review = l.pop()
                for index, word in enumerate(l):
                    if word == "1":
                        if index == 0:
                            positive = word_and_pos[index]
                            negative = word_and_neg[index]
                        else:
                            positive = word_and_pos[index] + positive
                            negative = word_and_neg[index] + negative
                    else:
                        if index == 0:
                            positive = none_and_pos[index]
                            negative = none_and_neg[index]
                        else:
                            positive = none_and_pos[index] + positive
                            negative = none_and_neg[index] + negative
                positive += ratio_pos
                negative += ratio_neg
                if positive >= negative:
                    if int(review) == 1:
                        total_correct += 1
                else:
                    if int(review) == 0:
                        total_correct += 1
            count += 1
    print("trained on:\t"+train_name+"\ntested on:\t" +test_name)
    print("accuracy: " + str(total_correct) + " / " + str(count-1) +" = " + str(total_correct/(count-1)) )

vocab = make_vocab()
count = len(vocab)

process("trainingSet.txt", "preprocessed_train.txt", vocab)
process("testSet.txt", "preprocessed_test.txt", vocab)

word_and_pos = [0] * count
word_and_neg = [0] * count
none_and_pos = [0] * count
none_and_neg = [0] * count
total_pos = 0
total_neg = 0

(total_pos, total_neg) = tally_totals(word_and_pos,word_and_neg,none_and_pos,none_and_neg,total_pos,total_neg)

probs(word_and_pos,word_and_neg,none_and_pos,none_and_neg,total_pos,total_neg,count)

ratio_pos = math.log(total_pos / (total_neg+total_pos))
ratio_neg = math.log(total_neg / (total_neg+total_pos))

sys.stdout = open("results.txt", 'w')
print("CS 331 Programming Assingment 3\nBy: Matthew Jacobsen & Jackson Miller")
print_cool_message()
guess(word_and_pos,word_and_neg,none_and_pos,none_and_neg,ratio_pos,ratio_neg,"preprocessed_train.txt",
"trainingSet.txt","trainingSet.txt")
print_cool_message()
guess(word_and_pos,word_and_neg,none_and_pos,none_and_neg,ratio_pos,ratio_neg,"preprocessed_test.txt",
"trainingSet.txt","testSet.txt")
sys.stdout = sys.__stdout__




