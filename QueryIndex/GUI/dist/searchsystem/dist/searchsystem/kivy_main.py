import os
import kivy
kivy.require("1.10.1")

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.factory import Factory
from functools import partial
from FileReading import termVectorFileReading,fileReading
from SearchModes import simpleSearch,booleanSearch,multiwordsSearch,rankingSearch
from os.path import join, isdir


class SearchMode(Screen):
    # choose the basic,advance and superior mode by clicking the button
    def mode_choose(self,mode):
        self.manager.mode = mode


class ConfirmPopup(Screen):

    def __init__(self, **kwargs):
        self.register_event_type('on_answer')
        super(ConfirmPopup, self).__init__(**kwargs)
        self.total_images = 0

    def on_answer(self, filepath, PathInput):
        pass

    def is_dir(self, directory, filename):
        return isdir(join(directory, filename))


class PathInput(Screen):


    #get the user input string, the path of directory
    def get_path(self):
        file_path = self.ids.path.text
        file_path.replace("\\","/")
        self.manager.file_path = file_path
        if (not os.path.isdir(file_path)):
            self.ids.error_info.text = 'Invalid Path'
            return 0
        mode = self.manager.mode
        if mode == 'basic' or mode == 'advance' :
            file_collection, position_information = fileReading(file_path)
            self.manager.file_collection = file_collection
            self.manager.position_information = position_information
        elif mode == 'superior':
            file_collection, final_word_list, doc_idf= termVectorFileReading(file_path)
            self.manager.file_collection = file_collection
            self.manager.final_word_list = final_word_list
            self.manager.doc_idf = doc_idf

    #change the screen base on different mode    
        mode = self.manager.mode
        if mode == "advance":
            self.manager.current = "amo"
        elif mode == "basic" or mode == "superior":
            self.manager.current = "q"

    def change_path(self, filepath):
        self.ids.path.text = filepath
    
    def popup_func(self):
        content = ConfirmPopup()
        content.bind(on_answer=self._on_answer)
        self.popup = Popup(title="Select Folder",
                           content=content,
                           size_hint=(None, None),
                           size=(500, 500),
                           auto_dismiss=False)
        self.popup.open()
        
    
    def _on_answer(self, instance, answer, obj):
        self.popup.dismiss()


class AdvanceModeOption(Screen):
    #choose to use boolean search or 
    def get_search_mode(self,search_mode):
        self.manager.search_mode = search_mode

class Query(Screen):

    def search(self):
        
        #get the user input query
        self.manager.query_origin = self.ids.query.text
        self.manager.query = self.ids.query.text.lower()
        #do the search
        if self.manager.mode =='basic':
            results = self.manager.do_query_simple(self.manager.file_collection)
        elif self.manager.mode == 'advance':
            if self.manager.search_mode == 'phrase':
                results = self.manager.do_query_multiwords(self.manager.file_collection,self.manager.position_information)
            elif self.manager.search_mode == 'boolean':
                results = self.manager.do_query_boolean(self.manager.file_collection)
        elif self.manager.mode == 'superior':
            results = self.manager.do_query_ranking(self.manager.final_word_list,self.manager.file_collection,self.manager.doc_idf)

        #delete previous results
        delete_button = self.manager.doc_result_button
        for button in delete_button:
            self.ids.results.remove_widget(button)
            
        if results == 'No Results':
            self.error_message = Label(text=results)
            self.manager.doc_result_button.append(self.error_message)
            self.ids.results.add_widget(self.error_message)
        elif results == 'Invalid Input':
            self.error_message = Label(text=results)
            self.manager.doc_result_button.append(self.error_message)
            self.ids.results.add_widget(self.error_message)
        else:
            # generate result button bsc self:
            if self.manager.mode == 'basic':
                for doc in results:
                    self.button = Button(text = doc + " have " + str(results[doc]) + " times")
                    buttoncallback = partial(self.display_results, doc)
                    self.button.bind(on_press = buttoncallback)
                    self.manager.doc_result_button.append(self.button)
                    self.ids.results.add_widget(self.button)
            elif self.manager.mode == 'advance':
                for doc in results:
                    self.button = Button(text = doc)
                    buttoncallback = partial(self.display_results, doc)
                    self.button.bind(on_press = buttoncallback)
                    self.manager.doc_result_button.append(self.button)
                    self.ids.results.add_widget(self.button)
            elif self.manager.mode == 'superior':
                for doc in results:
                    self.button = Button(text = "Rank " + str(results.index(doc) + 1) + ": " + str(doc[0]) + " with score " + str(round(doc[1], 2)))
                    buttoncallback = partial(self.display_results, doc)
                    self.button.bind(on_press = buttoncallback)
                    self.manager.doc_result_button.append(self.button)
                    self.ids.results.add_widget(self.button)
    
    #display the results by clicking the button
    def display_results(self, *args):
        query_term = self.manager.query_origin
        query_list = query_term.split(' ')
        if 'and' in query_list:
            #remove AND from query list
            query_list.remove('and')
        elif 'or' in query_list:
            # remove OR from query list
            query_list.remove('or')
        query_term = ""
        for term in query_list:
            query_term = query_term + " " + term
        print(query_term)
        self.manager.current = "dr"
        self.manager.get_screen('dr').ids.query_term.text = "Query: " + query_term
        if self.manager.mode == 'superior':
            self.manager.get_screen('dr').ids.doc_name.text = args[0][0]
            #read the selected file
            path = self.manager.file_path + '/' + args[0][0]
        else:
            self.manager.get_screen('dr').ids.doc_name.text = args[0]
            #read the selected file
            path = self.manager.file_path + '/' + args[0]
        f = open(path) #open file 
        iter_f = iter(f) #create iteration
        doc = ""
        for line in iter_f: #read every line in the file
            doc = doc + line
        temp = doc.split(" ")
        doc = ""
        for parts in temp:
            if parts in query_list:
                parts = '[color=#E5D209]'+ parts +'[/color]'
            doc = doc + ' ' + parts
        self.manager.get_screen('dr').ids.content.text = doc
        print(doc)

class DisplayResults(Screen):
    pass

class ScreenManagement(ScreenManager):
    mode = StringProperty()
    file_path = StringProperty()
    file_collection = {}
    position_information = {}
    doc_idf = {}
    final_word_list = []
    query = StringProperty()
    query_origin = StringProperty()
    search_mode = StringProperty()
    doc_result_button = []

    # query simple search
    def do_query_simple(self,file_collection):
        results = simpleSearch(self.query,file_collection)
        return results

    # query boolean search
    def do_query_boolean(self,file_collection):
        results = booleanSearch(self.query,file_collection)
        return results
    
    # query multiwords
    def do_query_multiwords(self,file_collection,position_information):
        totalInfo = TotalInfo_position(file_collection,position_information)
        results = multiwordsSearch(self.query,totalInfo)
        return results

    #query ranking
    def do_query_ranking(self,final_word_list,file_collection,doc_idf):
        totalInfo = TotalInfo_normalize(file_collection,doc_idf)
        results = []
        results = rankingSearch(self.query,final_word_list,totalInfo)
        return results


class TotalInfo_normalize(object):
    def __init__(self,normalize_vector,doc_idf):
        self.normalize_vector = normalize_vector
        self.doc_idf = doc_idf

class TotalInfo_position(object):
    def __init__(self,file_collection,position_information):
        self.file_collection = file_collection
        self.position_information = position_information

search_system = Builder.load_file('SearchSystem.kv')
class SearchSystemApp(App):
    def build(self):
        return search_system
    
    def mode_name(self, mode_name):
        self.root.ids.screen_query.ids.mode_name.text = mode_name

    def select_path(self, filepath):
        if(filepath != 'cancel'):
            self.root.ids.screen_path_input.ids.path.text = filepath
            self.root.ids.screen_path_input.popup.dismiss()

if __name__ == '__main__':
    SearchSystemApp().run()
    