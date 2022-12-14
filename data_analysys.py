import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import seaborn as sns
import pycountry_convert as pc
from tkinter import *
import json
from PIL import ImageTk, Image
from tkinter import filedialog
from dataprep.clean import validate_country
from tkinter import Toplevel
from itertools import groupby
import pydot 
import os
from matplotlib.widgets import Slider
import webbrowser
import sys


os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin/'

############################## Functions #########################################

#Created histogram for visitor_useragent(browser and other info) filed from input file
def input_file():
    filename = filedialog.askopenfilename(initialdir="/D",title="Select file for data Analysys")
    print(filename)
    global data, data1
    
    list_result = [json.loads(line)
    for line in open(filename, 'r', encoding='utf-8')]  
      
    data = pd.DataFrame (list_result, columns = ['col_no','ts', 'visitor_uuid', 'visitor_source', 'visitor_device', 'visitor_useragent', 'visitor_ip',
    'visitor_country', 'visitor_referrer', 'env_type', 'env_doc_id', "env_ranking","env_build","env_name","env_component",'event_type',"event_readtime",'subject_type', 'subject_doc_id', 'subject_page', 'cause_type'])
    data1 = data


#Created histogram to analze from which countries the given document has been viewed
def country_histogram():
    top_root = Toplevel()
    top_root.grab_set()
    top_root.geometry('500x500+500+230')
    top_root.iconbitmap('icon.ico')
    top_root.mainloop
    top_root.resizable(False,False)
    global docidval 
    docidval = StringVar()

    textdata = "\nProvide Document Id: \n"
    idlabel = Label(top_root,text=textdata,relief=GROOVE, font=('times',13,'bold'), width=40)
    idlabel.place(x=38,y=20)
    
    idlabel = Label(top_root,text="Enter Documnet Id",relief=GROOVE, font=('times',15,'bold'))
    idlabel.place(x=20,y=140)
    identry = Entry(top_root, font=('roman',15,'bold'),bd=5,textvariable=docidval)
    identry.place(x=200,y=140)
   
    submitbtn = Button(top_root,text='Submit',font=('Lithos Pro Regular',15,'bold'),width=20,bd=5,
    activebackground='blue',activeforeground='white', command=draw_country_histogram)
    submitbtn.place(x=100,y=250)

def draw_country_histogram():
    data1 = data['env_doc_id'] == docidval.get()  
    data2 = data[data1]
    print(data2.shape[0])
    if data2.shape[0]!= 0:
        plt.figure(figsize=(14,14))
        sns.countplot(x='visitor_country',data=data2)
        plt.title("Number of Views from Different Countries")
        plt.show()

#Created histogram to analze from which continent the given document has been viewed
def continent_histogram():
    top_root = Toplevel()
    top_root.grab_set()
    top_root.geometry('500x500+500+230')
    top_root.iconbitmap('icon.ico')
    top_root.mainloop
    top_root.resizable(False,False)
    global docidval 
    docidval = StringVar()

    textdata = "\nProvide Document Id: \n"
    idlabel = Label(top_root,text=textdata,relief=GROOVE, font=('times',13,'bold'), width=40)
    idlabel.place(x=38,y=20)
    
    idlabel = Label(top_root,text="Enter Documnet Id",relief=GROOVE, font=('times',15,'bold'))
    idlabel.place(x=20,y=140)
    identry = Entry(top_root, font=('roman',15,'bold'),bd=5,textvariable=docidval)
    identry.place(x=200,y=140)
   
    submitbtn = Button(top_root,text='Submit',font=('Lithos Pro Regular',15,'bold'),width=20,bd=5,
    activebackground='blue',activeforeground='white', command=draw_continent_histogram)
    submitbtn.place(x=100,y=250)
    
def draw_continent_histogram():

    data1 = data['env_doc_id'] == docidval.get()   
    data2 = data[data1]

# get the continent from given country code
    for i in range(len(data2)):
        if (validate_country(data2['visitor_country'].values[i])):
            data2['visitor_country'].values[i] = pc.country_alpha2_to_continent_code(data2['visitor_country'].values[i])
    
    sns.countplot(x='visitor_country',data=data2)
    plt.title("Number of Views from Different Continents")
    plt.show()

def browser_verbose_histogram():

#Created histogram for visitor_useragent(browser and other info) filed from input file
    plt.figure(figsize=(14,14))
    sns.countplot(x='visitor_useragent',data=data)
    plt.title("Number of Views for Different Browsers")
    plt.show()

def browser_histogram():

#The verbose string from 'visitor_useragent' field is splitted so as to get just browser name
    data['visitor_useragent'].str.split('/',n=1,expand=True)
    split_str = data['visitor_useragent'].str.split('/',n=1,expand=True).rename(columns={0:'Browser',1:'Browser_data'})
    
    plt.figure(figsize=(14,14))
    sns.countplot(x='Browser',data=split_str)
    plt.title("Number of Views for Different Browsers")
    plt.show()

#Depending on total time spent by used reading document, top 10 readers are calculated
def top_readers():
    top_root = Toplevel()
    top_root.grab_set()
    top_root.geometry('500x500+500+230')
    top_root.iconbitmap('icon.ico')
    top_root.mainloop
    top_root.resizable(False,False)

    idlabel = Label(top_root,text="List of Top 10 Readers:(visitor_uuid)",relief=GROOVE, font=('times',13,'bold'))
    idlabel.place(x=100,y=10)
    data1 = data.nlargest(10,'event_readtime')
    x_i = 10
    y_i = 10
   
    text_data= data1['visitor_uuid']
    i = 1
    for value in data1['visitor_uuid']:
        
        index_lable = reader = Label(top_root,text=i, font=('times',12,'bold'))
        reader.place(x=80+x_i,y=100+y_i)
        reader = Label(top_root,text=value, font=('times',12,'bold'), width=30)
        reader.place(x=100+x_i,y=100+y_i)
        y_i += 35
        i = i+1

#For a given document, identify, which all readers and other documents have been read by this readers
def also_like1():
    top_root = Toplevel()
    top_root.grab_set()
    top_root.geometry('500x500+500+230')
    top_root.iconbitmap('icon.ico')
    top_root.mainloop
    top_root.resizable(False,False)
    
    textdata = "\nFor a given document, identify, which other documents\n have been read by this document’s readers. \n"
    idlabel = Label(top_root,text=textdata,relief=GROOVE, font=('times',13,'bold'), width=40)
    idlabel.place(x=38,y=20)
    
    idlabel = Label(top_root,text="Enter Documnet Id",relief=GROOVE, font=('times',13,'bold'))
    idlabel.place(x=20,y=140)
    idlabel = Label(top_root,text="Enter User Id",relief=GROOVE, font=('times',13,'bold'))
    idlabel.place(x=20,y=250)

    global docidval 
    docidval = StringVar()
    global useridval 
    useridval= StringVar()
    identry = Entry(top_root, font=('roman',15,'bold'),bd=5,textvariable=docidval)
    identry.place(x=200,y=140)
    identry = Entry(top_root, font=('roman',15,'bold'),bd=5,textvariable=useridval)
    identry.place(x=200,y=250)
    
    submitbtn = Button(top_root,text='Submit',font=('Lithos Pro Regular',15,'bold'),width=20,bd=5,
    activebackground='blue',activeforeground='white', command=also_like2)
    submitbtn.place(x=100,y=320)

def also_like2():
    
    # find out all the users for given document
    list_uid = []
    for i in range(len(data)):
        if data['env_doc_id'].values[i] == docidval.get() and data['visitor_uuid'].values[i] != useridval.get():
            list_uid.append(str(data['visitor_uuid'].values[i]))
    set_list_uid = set(list_uid)
    list_uid = list(set_list_uid)

    # find all documents read by users listed above
    list_didofusers = dict()
  
    set_list = set()
    for j in range(len(list_uid)):  
        set_list = set()
        for i in range(len(data)):
            if list_uid[j] == data['visitor_uuid'].values[i]:
                #list_didofusers.setdefault(list_uid[j], []).append(data['env_doc_id'].values[i])
                if str(data['env_doc_id'].values[i]) != 'nan':
                    set_list.add(str(data['env_doc_id'].values[i]))

        list_didofusers.setdefault(list_uid[j], []).append(set_list)

    if also_like_graph != True:
#draw tkenter top window
        top_root = Toplevel()
        top_root.grab_set()
        top_root.geometry('500x500+500+230')
        top_root.iconbitmap('icon.ico')
        top_root.mainloop
        top_root.resizable(False,False)
    
        list_doc_uuid = []
        # from dictionary of document id's, extract all the documents and make a list of that document so as to print it
        for capital in list_didofusers.values():
            for i in capital:
                for j in i:
                    if j != docidval.get():
                        list_doc_uuid.append(j)
    
        new_list = []
        for item in list_doc_uuid:
            if str(item) != 'nan':
                new_list.append(item)
        pd1  = pd.DataFrame(new_list , columns=['q_data'])
        count_series = pd1.groupby(['q_data'],as_index=False).size().sort_values(by='size',ascending=False)


        idlabel = Label(top_root,text="List of Document Id's that user may Like:",relief=GROOVE, font=('times',13,'bold'))
        idlabel.place(x=100,y=10)
        x_i = 10
        y_i = 10
   
        i = 1
# display the above list of also like documents on tkinter top window
        for value in count_series['q_data']:
            
            index_lable = reader = Label(top_root,text=i, font=('times',12,'bold'))
            reader.place(x=70+x_i,y=100+y_i)
            reader = Label(top_root,text=value, font=('times',12,'bold'), width=40)
            reader.place(x=90+x_i,y=100+y_i)
            y_i += 35
            i = i+1
    else:
        graph = pydot.Dot(graph_type='digraph')

        list_uid.append(useridval.get())
        graph = pydot.Dot(graph_type='digraph')


        main_node  = pydot.Node(useridval.get(),style="filled",fillcolor="green",shape= "rectangle", bgcolor="green",height="2",fontsize="22")
        main_pork_node  = pydot.Node(docidval.get(),style="filled",fillcolor="red",height="2",fontsize="22")

        graph.add_edge(pydot.Edge(main_node,main_pork_node))

        for j in list_didofusers:
            start_node  = pydot.Node(j,style="filled",fillcolor="pink",shape= "rectangle", height="2",fontsize="22",ranksep ="2")
            graph.add_node(start_node)
            value_dict = list_didofusers[j]
            for i in value_dict:
                for k in i:
                    if (k == docidval.get()):
                        pork_node  = pydot.Node(k,style="filled",fillcolor="green",height="2",fontsize="22")
                    else:
                        pork_node  = pydot.Node(k,style="filled",fillcolor="turquoise", height="2",fontsize="22")
                    graph.add_node(pork_node)
                    graph.add_edge(pydot.Edge(start_node,pork_node))

        graph.write_pdf("current.pdf")
        graph.write_png("current.png")
        webbrowser.open('current.pdf')

# draw a graph for also like functionality
def also_like_graph():
    also_like1()
    global also_like_graph
    also_like_graph = True

def display_tkinter_screen():
    
    ################################## Label ###########################################
    label = Label(root, text="Data Analysys",font=('chiller',30,'italic bold'),relief=RIDGE,borderwidth=4,width=35)
    label.place(x=260,y=0)

    ################################## Frames ##########################################
    dataframe1 = Frame (root,relief=GROOVE,borderwidth=5)
    dataframe1.place(x=20,y=140,width=530,height=540)

    dataframe = Frame (root,relief=GROOVE,borderwidth=5)
    dataframe.place(x=550,y=140,width=530,height=540)

    textdata = "\nPython-based application, that analyses and displays document \n tracking data from a major web site. \n"
    idlabel = Label(dataframe1,text=textdata,relief=GROOVE, font=('times',13,'bold'))
    idlabel.place(x=40,y=200)

    submitbtn = Button(root,text='Select File For Analysys',font=('Lithos Pro Regular',15,'bold'),width=30,bd=5,activeforeground='white', command=input_file)
    submitbtn.place(x=400,y=70)

    country_view_btn = Button(dataframe,text='Histogram of countries',width=35,font=('Courier',15,'bold'),bd=6,activebackground='blue',relief=RIDGE,
    activeforeground='white',command=country_histogram)
    country_view_btn.place(x=40,y=40)

    continent_view_btn = Button(dataframe,text='Histogram of Continents',width=35,font=('Courier',15,'bold'),bd=6,activebackground='blue',relief=RIDGE,
    activeforeground='white',command=continent_histogram)
    continent_view_btn.place(x=40,y=120)

    browser_view_btn = Button(dataframe,text='Histogram of Browsers',width=35,font=('Courier',15,'bold'),bd=6,activebackground='blue',relief=RIDGE,
    activeforeground='white',command=browser_histogram)
    browser_view_btn.place(x=40,y=200)


    top_readers_btn = Button(dataframe,text='Display Top Readers',width=35,font=('Courier',15,'bold'),bd=6,activebackground='blue',relief=RIDGE,
    activeforeground='white',command=top_readers)
    top_readers_btn.place(x=40,y=280)

    also_like_btn = Button(dataframe,text='Also like functionality',width=35,font=('Courier',15,'bold'),bd=6,activebackground='blue',relief=RIDGE,
    activeforeground='white',command=also_like1)
    also_like_btn.place(x=40,y=360)

    also_like_btn = Button(dataframe,text='Graph for Also like functionality',width=35,font=('Courier',15,'bold'),bd=6,activebackground='blue',relief=RIDGE,
    activeforeground='white',command=also_like_graph)
    also_like_btn.place(x=40,y=440)

def display_tkinter_screen_task2():

    global docidval
    docidval = StringVar()

    textdata = "\nProvide Document Id: \n"
    idlabel = Label(root,text=textdata,relief=GROOVE, font=('times',13,'bold'), width=40)
    idlabel.place(x=38,y=20)
        
    idlabel = Label(root,text="Enter Documnet Id",relief=GROOVE, font=('times',15,'bold'))
    idlabel.place(x=20,y=140)
    identry = Entry(root, font=('roman',15,'bold'),bd=5,textvariable=docidval)
    identry.place(x=200,y=140)
    

# check the value of arguments provided from command like and so the tasks as per input provided
    if sys.argv[3] == '2a':
        submitbtn = Button(root,text='Submit',font=('Lithos Pro Regular',15,'bold'),width=20,bd=5,
        activebackground='blue',activeforeground='white', command=draw_country_histogram)
        submitbtn.place(x=100,y=250)
    elif sys.argv[3] == '2b':
        submitbtn = Button(root,text='Submit',font=('Lithos Pro Regular',15,'bold'),width=20,bd=5,
        activebackground='blue',activeforeground='white', command=draw_continent_histogram)
        submitbtn.place(x=100,y=250)

    root.mainloop()
############################# Program Start #######################################
background="#06283D"
framebg="#EDEDED"
framefg="#06283D"
root = Tk()
root.title("Data Analysis of a Document Tracker")
root.geometry("1100x700+210+60")
root.iconbitmap('icon.ico')
root.resizable(False, False)
root.config(bg=background)

# if the data provided from command line all 5 fields given 
if len(sys.argv) == 5 :
    filename = sys.argv[4]
    user_uuid = sys.argv[1]
    doc_uuid = sys.argv[2]
    task_id = sys.argv[3]
    print(filename,user_uuid,doc_uuid, task_id)
    filename = sys.argv[4]
    
    print(filename)
    global data, data1
    
    list_result = [json.loads(line)
    for line in open(filename, 'r', encoding='utf-8')]  
      
    data = pd.DataFrame (list_result, columns = ['col_no','ts', 'visitor_uuid', 'visitor_source', 'visitor_device', 'visitor_useragent', 'visitor_ip',
    'visitor_country', 'visitor_referrer', 'env_type', 'env_doc_id', "env_ranking","env_build","env_name","env_component",'event_type',"event_readtime",'subject_type', 'subject_doc_id', 'subject_page', 'cause_type'])
    data1 = data
    
    if sys.argv[3] == '2a':
        display_tkinter_screen_task2()
    elif sys.argv[3] == '2b':
        display_tkinter_screen_task2()
    elif sys.argv[3] == '3a':
        browser_verbose_histogram()
    elif sys.argv[3] == '3b':
        browser_histogram()
    elif sys.argv[3] == '4':
        top_readers()
    elif sys.argv[3] == '5d':
        also_like1()
    elif sys.argv[3] == '6':
        also_like_graph()

    elif sys.argv[3] == '7':
        pass
elif len(sys.argv) == 1:
    display_tkinter_screen()


root.mainloop()

