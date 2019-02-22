'''
    operation of the whole project
'''
from Interface import CommandLineInterface
from SearchModes import simpleSearch, booleanSearch

cli = CommandLineInterface() #initialize commandlineinterface
while True:
    mode = cli.search_mode()
    if mode == 'basic' or mode == 'advance' :
        file_collection, position_information = cli.do_path_basic()
        if not file_collection:
            print('the dictionary contains no file')
        else:
            break
    elif mode == 'superior':
        file_collection, final_word_list, doc_idf= cli.do_path_vector()
        if not file_collection:
            print('the dictionary contains no file')
        else:
            cli.do_help()
            break
    else:
        print('incorrect input,please re-enter the command')
    
while True:
    #start to get the user input
    statement = input()
    #give user neccesary information
    if statement == 'help':
        cli.do_help()
    #query search base on different modes
    elif statement == 'query':
        if mode =='basic':
            results = cli.do_query_simple(file_collection)
            cli.display_results(results)
        elif mode == 'advance':
            search_mode = input('phrase search or boolean search?  :')
            if search_mode == 'phrase':
                results = cli.do_query_multiwords(file_collection,position_information)
                cli.display_results(results)
            elif search_mode == 'boolean':
                results = cli.do_query_boolean(file_collection)
                cli.display_results(results)
            else:
                print('incorrect input,please choose phrase or boolean search')
                cli.do_help()
        elif mode == 'superior':
            results = cli.do_query_ranking(final_word_list,file_collection,doc_idf)
            cli.display_results(results)
        else:
            print('incorrect input,please choose correct search mode')
            cli.do_help()
    #exit command
    elif statement == 'exit':
        break
    #incorrect command
    else:
        print('invalid operation, please enter the correct command')
