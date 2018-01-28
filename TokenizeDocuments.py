from nltk.tokenize import *

import xml.etree.ElementTree as ET

from nltk.corpus import stopwords

from SeparateWordsWithSpaces import infer_spaces
from nltk.stem.porter import PorterStemmer

import re,glob,os,csv

import nltk



from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer

#Path to OWLS files for the Web Services
path2='C:/Users/chinmay/Desktop/OWLS-TC4_PDDL/htdocs/domains/1.1/economy/'

#Converting CAmel Case to normal
def convert(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

#tokenize OWLS files
def Tokenize(xmlstr):

    a=xmlstr.decode("utf-8")
    a=a.split('\n')

    alist=""

    for i in range(0,len(a)):

      alist+=a[i]

    alist_withoutTags=regexp_tokenize(alist, r'<.*?>', gaps=True)


    string=""

    for i in range(0,len(alist_withoutTags)):

        string=string+" "+alist_withoutTags[i]

    string=string.split(' ')
    # string=string.split('\t')


    alist_withoutTagsHttphash=[]



    for i in range(0,len(string)):


        a=regexp_tokenize(''.join(string[i].split()), r'.?http.*?#', gaps=True)

        alist_withoutTagsHttphash.append(a)

    alist_withoutTagsHttphash = [x for x in alist_withoutTagsHttphash if x != []]


    #print(alist_withoutTagsHttphash)


    string_2=""
    for i in range(0,len(alist_withoutTagsHttphash)):

        string_2=string_2+str(alist_withoutTagsHttphash[i][0])+" "

    string_2=string_2.split(' ')



    alist_withoutTagsHttphashHttp=[]

    for i in range(0,len(alist_withoutTagsHttphash)):


        a=regexp_tokenize(str(string_2[i]), r'http.*', gaps=True)

        alist_withoutTagsHttphashHttp.append(a)

    #print(alist_withoutTagsHttphashHttp)

    alist_withoutTagsHttphashHttp = [x for x in alist_withoutTagsHttphashHttp if x != []]

    WordList=[]

    for i in range(0,len(alist_withoutTagsHttphashHttp)):

        WordList.append(re.sub(r'[\W_]+|\d+', '', alist_withoutTagsHttphashHttp[i][0]))

    WordList  = [word for word in WordList if word not in ["getRequest","getResponse","None","XSL","get"]]

    WordList=[ chunk for chunk in WordList if not chunk.endswith("Soap") ]

    FinalWordList=[]

    for i in range(0,len(WordList)):

        result=convert(WordList[i])

        resultList=result.split("_")



        for j in range(0,len(resultList)):

            FinalWordList.append(resultList[j])

    FinalFinalWordList=[]

    for i in range(0,len(FinalWordList)):

        result=infer_spaces(FinalWordList[i])

        resultList1=result.split(" ")



        for j in range(0,len(resultList1)):

            FinalFinalWordList.append(resultList1[j])

    list_words=[]

    for wor in FinalFinalWordList:

        if len(wor)>3:

            list_words.append(wor)

        else:

            if wor in ['age','aid','atm','bat','bed','box','bus','buy','car','day','ear','ear','fan','fee','fun','gel','geo','gps','hot','ion','job','key','low','map','max','net','new','old','pan','pan','pro','raw','sea','tax','tea','use','web','zip','zoo']:

                list_words.append(wor)





    filtered_words = [word for word in list_words if word not in stopwords.words('english')]

    return filtered_words





def main():



    for word in ['communication','food','weapon','geography','education','medical','simulation','travel','economy']:

        path2='C:/Users/chinmay/Desktop/OWLS-TC4_PDDL/htdocs/domains/1.1/'+str(word)+'/'

        for filename in glob.glob(os.path.join(path2, '*.owls')):

            print(filename)
            tree = ET.parse(filename)
            root = tree.getroot()

            xmlstr = ET.tostring(root, encoding='utf8', method='xml')

            WOrdList=Tokenize(xmlstr)

            actualFileName=os.path.basename(filename)
            actualFileName=actualFileName[0:len(actualFileName)-4]

            theFile=open("F:/OWLS-TC/"+str(word)+"/"+str(actualFileName)+"txt", 'w+')

            OutList=""

            for l in range(0,len(WOrdList)):

                OutList+=WOrdList[l]+" "

            theFile.write(OutList)

#uncomment this to genrate files containing tokens of each web service owls
#and then comment this to genrate the TF-IDF matrix


#main()




path = 'F:/OWLS-TC'
token_dict = {}
stemmer = PorterStemmer()

def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed

def tokenize(text):
    tokens = nltk.word_tokenize(text)

    return tokens

for subdir, dirs, files in os.walk(path):
    for file in files:
        file_path = subdir + os.path.sep + file

        category=subdir.split("\\")


        shakes = open(file_path, 'r')
        text = shakes.read()
        lowers = text.lower()

        file=file+"$"+str(category[1])

        token_dict[file] = lowers



#this can take some time
tfidf = TfidfVectorizer(tokenizer=tokenize, stop_words='english', min_df = 0)
tfs = tfidf.fit_transform(token_dict.values())

tf_idf_values=tfs.toarray()
features=tfidf.get_feature_names()
file_name=list(token_dict.keys())

main_csv=[]

sublist=[]

for i in range(0,len(features)+2):

    if i<len(features):

        sublist.append(features[i])

    if i==len(features):

        sublist.append("FileName")

    if i==len(features)+1:

        sublist.append("Category")

print(len(sublist))

main_csv.append(sublist)

for j in range(0,len(file_name)):

    sublist1=[]

    res=file_name[j]
    name=res.split("$")

    FileName=name[0]
    Category=name[1]



    for k in range(0,len(tf_idf_values[j])):

        sublist1.append(tf_idf_values[j][k])

    sublist1.append(FileName)
    sublist1.append(Category)

    main_csv.append(sublist1)

with open("data.csv", "w",newline="") as f:
    writer = csv.writer(f)
    writer.writerows(main_csv)























