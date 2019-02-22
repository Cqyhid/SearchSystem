'''
    calculation function
'''
import math

#calculate the idf value for each df
def IDF(document_frequency,total_document_number):
    result = math.log10(total_document_number/document_frequency)
    return result
