'''
    This file will read the file one by one and return the content to search.py
'''
import os
import math
from Function import IDF

def fileReading(file_path):

    path = file_path #directory path
    files= os.listdir(path) #get the name of all files under the directory
    word_list = []
    word_list_origi = []
    inverted_index = {}
    position_information = {}

    for file in files: #go through the directory
        doc_word_list = []
        if not os.path.isdir(file): #open the file if it is not the directory
            f = open(path+"/"+file) #open file 
            iter_f = iter(f) #create iteration
            str = ""
            for line in iter_f: #read every line in the file
                str = str + line
            #split by blank
            word_list_origi = str.split(' ')
            for term in word_list_origi:
                word_list.append(term.lower())
                doc_word_list.append(term.lower())
            position_information[file] = doc_word_list
            #remove stop words
        f1 = open('C:/Users/Alpha/Desktop/IR/Assignment-1/english.stop')
        iter_f1 = iter(f1) #create iteration
        str = ""
        for line in iter_f1: #read every line in the file
            str = str + line
        # split by blank
        stop_word_list=str.split("\n")
        temp_word_list = list(word_list)
        for words in temp_word_list:
            if words in stop_word_list:
                word_list.remove(words)

        # inverted indexing
        for word in doc_word_list:
            if word in inverted_index:
                inverted_index[word].append(file)
            else:
                inverted_index[word]=[file]
    print('Sorting completed!')
    
    return inverted_index , position_information

'''
    reading the file to term vectors
'''

def termVectorFileReading(file_path):
    path = file_path #directory path
    files= os.listdir(path) #get the name of all files under the directory
    final_word_list = []
    doc_term_vector = {}
    doc_frequency = {}
    total_document_number = 0
    #word_list_set is term in document
    #final_word_list is term collection

    for file in files: #go through the directory
        total_document_number += 1
        word_list = []
        word_list_origi = []
        if not os.path.isdir(file): #open the file if it is not the directory
            f = open(path+"/"+file) #open file 
            iter_f = iter(f) #create iteration
            str = ""
            for line in iter_f: #read every line in the file
                str = str + line
            #split by blank
            word_list_origi=str.split(' ')
            for term in word_list_origi:
                word_list.append(term.lower())
            #delete repeat words in one document
            
            word_list_set = list(set(word_list))

        for word in word_list:
            if word not in final_word_list:
                final_word_list.append(word)

        for word in word_list_set:
            if word not in doc_frequency:
                doc_frequency[word] = 1
            else:
                doc_frequency[word] += 1 #document frequency df+1

    

    #remove stop words
    f1 = open('C:/Users/Alpha/Desktop/IR/Assignment-1/english.stop')
    iter_f1 = iter(f1) #create iteration
    str = ""
    for line in iter_f1: #read every line in the file
        str = str + line
    #split by blank
    stop_word_list=str.split("\n")
    temp_final_word_list = list(final_word_list)
    for words in temp_final_word_list:
        if words in stop_word_list:
            final_word_list.remove(words)

    for file in files: #go through the directory
        word_list = []
        word_list_origi = []
        if not os.path.isdir(file): #open the file if it is not the directory
            f = open(path+"/"+file) #open file 
            iter_f = iter(f) #create iteration
            str = ""
            for line in iter_f: #read every line in the file
                str = str + line
            #split by blank
            word_list_origi=str.split(' ')
            for term in word_list_origi:
                word_list.append(term.lower())

            temp = {}
            for word in final_word_list:
                if word not in word_list:
                    temp[word] = 0
                else:
                    number = word_list.count(word)
                    temp[word] = number
        
        #doc_term_vector[document] is the tf
        doc_term_vector[file] = temp

    # Calulate IDF
    doc_idf = {}
    for term in doc_frequency:
        doc_idf[term] = IDF(doc_frequency[term], total_document_number)
    
    # Calulate TF-IDF: weight
    doc_tf_idf = {}
    for doc in doc_term_vector:
        doc_tf_idf[doc] = {}
        for term in doc_term_vector[doc]:
            doc_tf_idf[doc][term] =  doc_term_vector[doc][term] * doc_idf[term]  # TF * IDF

    #calculate euclidean
    doc_distance = {}
    for doc in doc_tf_idf:
        temp = 0
        for term in doc_tf_idf[doc]:
            temp += math.pow(doc_tf_idf[doc][term],2)
        temp = math.sqrt(temp)
        doc_distance[doc] = temp

    # Normalization : weight / distance

    doc_normalization = {}
    for doc in doc_tf_idf:
        doc_normalization[doc] = {}
        for term in doc_tf_idf[doc]:
            doc_normalization[doc][term] =  doc_tf_idf[doc][term] / doc_distance[doc]
 
    print('Sorting completed!')
    print('the total word number is ')
    print(len(final_word_list))
    return doc_normalization, final_word_list, doc_idf
