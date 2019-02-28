'''
    Three different types of search
'''

def simpleSearch(query,inverted_index):
    if query not in inverted_index:
        return 'No Results'
    #get the list from inverted dictionary
    results = inverted_index[query]
    #remove the repeat name
    sorted_result = list(set(results))
    #dictionary to store the name:number pairs
    results_with_number = {}
    #make name:value pairs
    for item in sorted_result:
        number = results.count(item)
        results_with_number[item] = number
    
    return results_with_number

def booleanSearch(query,inverted_index):
    #get the query list
    query_list = []
    query_list = query.split(' ')
    #ente rthe AND search mode
    if 'and' in query_list and 'or' in query_list:
        return 'Invalid Input'

    elif 'and' in query_list:
        #remove AND from query list
        query_list.remove('and')
        for query in query_list:
            if query not in inverted_index:
                return 'No Results'
        results = inverted_index[query_list[0]]
        #remove the repeat name
        sorted_result = list(set(results))
        query_list.remove(query_list[0])
        for terms in query_list:
            temp = inverted_index[terms]
            #remove the repeat name
            sorted_temp = list(set(temp))
            sorted_result_temp = list(sorted_result)
            for val in sorted_result_temp:
                if val not in sorted_temp:
                    sorted_result.remove(val)

    #enter the OR search mode
    elif 'or' in query_list:
        # remove OR from query list
        query_list.remove('or')
        not_no_result = False
        query_list_temp = list(query_list)
        for query in query_list_temp:
            if query in inverted_index:
                not_no_result = True
            elif query not in inverted_index:
                query_list.remove(query)
        if (not not_no_result):
            return 'No Results'

        results = inverted_index[query_list[0]]
        #remove the repeat name
        sorted_result = list(set(results))
        query_list.remove(query_list[0])

        sorted_result_temp = list(sorted_result)
        for terms in query_list:
            temp = inverted_index[terms]
            #remove the repeat name
            sorted_temp = list(set(temp))
            for val in sorted_temp:
                if val not in sorted_result_temp:
                    sorted_result.append(val)
    else:
        return 'Invalid Input'

    return sorted_result

def multiwordsSearch(query,totalInfo):
    file_collection = totalInfo.file_collection
    position_information = totalInfo.position_information
    #get the query list
    query_list = []
    query_list = query.split(' ')
    #get the list from inverted dictionary
    if query_list[0] not in file_collection:
        return 'No Results'
    results = file_collection[query_list[0]]
    #remove the repeat name
    sorted_result = list(set(results))
    final_results = list(sorted_result)
    #see if the next position word is the same as query list
    for doc in sorted_result:
        position = position_information[doc].index(query_list[0])
        for query in query_list:
            temp = list(position_information[doc])
            if temp[position] != query:
                final_results.remove(doc)
                break
            position +=1
    if len(final_results) == 0:
        return 'No Results'
    return final_results

def rankingSearch(query,final_word_list,totalInfo):
    normalized_vector = totalInfo.normalize_vector
    doc_idf = totalInfo.doc_idf
    #get the query list
    query_list = []
    query_list=query.split(' ')
    #construct query vector
    query_vector = {}
    for term in final_word_list:
        if term in query_list:
            query_vector[term] = 1
        elif term not in query_list:
            query_vector[term] = 0
        else:
            return 'No Results'
    query_weights = {}
    # Calulate TF-IDF: weight of Query
    for term in query_vector:
        query_weights[term] = query_vector[term] * doc_idf[term]

    doc_ranking = {}
    
    for doc in normalized_vector:
        temp = 0
        for term in normalized_vector[doc]:
            temp = temp + normalized_vector[doc][term] * query_weights[term]
        doc_ranking[doc] = temp

    #delete ranking value = 0
    temp_doc_ranking = dict(doc_ranking)
    for doc in temp_doc_ranking:
        if doc_ranking[doc] == 0:
            del doc_ranking[doc]

    sorted_by_value = sorted(doc_ranking.items(), key=lambda kv: kv[1])
    sorted_by_value.reverse()
    if len(sorted_by_value) == 0:
        return 'No Results'
    return sorted_by_value