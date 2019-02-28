'''
    The interface file needs to generate the basic interface in command line which
    allows user to type in the path of collection directory
    It will also display the name of file which contains the search results
'''
from FileReading import termVectorFileReading,fileReading
from SearchModes import simpleSearch,booleanSearch,multiwordsSearch,rankingSearch

class CommandLineInterface():
    
    # initialization
    def __init__(self):
        print('|------------------------------------------------------'
                      '---------------------|')
        print('      Welcome to use simple search system')
        print('|------------------------------------------------------'
                      '---------------------|')
        print("      You can use 'help' command to know more")
        print("      details about the system operation")
        print('|------------------------------------------------------'
                      '---------------------|')
    
    # query simple search
    def do_query_simple(self,file_collection):
        query = input('Please type in the query: ')
        query.lower()
        results = simpleSearch(query,file_collection)
        return results

    # query boolean search
    def do_query_boolean(self,file_collection):
        query = input('Please type in the query: ')
        query.lower()
        results = booleanSearch(query,file_collection)
        return results
    
    # query multiwords
    def do_query_multiwords(self,file_collection,position_information):
        query = input('Please type in the query: ')
        query.lower()
        totalInfo = TotalInfo_position(file_collection,position_information)
        results = multiwordsSearch(query,totalInfo)
        return results

    #query ranking
    def do_query_ranking(self,final_word_list,file_collection,doc_idf):
        query = input('Please type in the query: ')
        query.lower()
        totalInfo = TotalInfo_normalize(file_collection,doc_idf)
        results = {}
        results = rankingSearch(query,final_word_list,totalInfo)
        return results

    # file path basic reading
    def do_path_basic(self):
        print('the absolute path is required, the format is like: "D:\informationretreival\data"')
        file_path = input('Please type in the path of your directory: ')
        file_path.replace("\\","/")
        return fileReading(file_path)

    # file path vector reading
    def do_path_vector(self):
        print('the absolute path is required, the format is like: D:/IR/data')
        file_path = input('Please type in the path of your directory: ')
        file_path.replace("\\","/")
        return termVectorFileReading(file_path)

    # display the results
    def display_results(self,data):
        print(data)

    # choose the search mode
    def search_mode(self):
        print('Simple search only allows user to input one word query')
        print('Advance search allows user to input boolean query or phrase query')
        print('Superior advance search will show the results ordered by ranking')
        input_mode = input('choose the search mode you want("basic","advance" or "superior"): ')
        return input_mode

    def do_help(self):
        print('|------------------------------------------------------'
                      '---------------------|')
        print("You can use 'query' and 'exit' operation in this system")
        print('|------------------------------------------------------'
                      '---------------------|')
        print('you can enter the query you want to search after enter the query mode')
        print('|------------------------------------------------------'
                      '---------------------|')

class TotalInfo_normalize(object):
    def __init__(self,normalize_vector,doc_idf):
        self.normalize_vector = normalize_vector
        self.doc_idf = doc_idf

class TotalInfo_position(object):
    def __init__(self,file_collection,position_information):
        self.file_collection = file_collection
        self.position_information = position_information