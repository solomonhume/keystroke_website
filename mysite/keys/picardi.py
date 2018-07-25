#-------------------------------------------------------------------------------
# Name:        cu_keystroke_parser
# Purpose:  Clarkson keystroke data analysis
#
# Author:      Jiaju Huang
# Email:    jiajhua@clarkson.edu
# Created:     01/03/2014
#-------------------------------------------------------------------------------
import os
import distance_score

gamma = 0.5
SAMPLE_CHUNK_SIZE = 200
SAMPLE_NO = 10
replace_matrix={'space':'-', '':'+', ' ':'-', }

R_MEASURE = 2
A_MEASURE = 2
array_m = []

def sort_dic(dic):
    """
    The key of the input dictionary is a digraph or trigraph, and value is (total time of the n-graph, number of occurrences)
    Divide the two we get average time for the n-graph
    This function sort the dictionary by the average time and return a list of the tuples (n-graph, average time)
    """
    return [(k, v[0]*1.0/v[1]) for k,v in sorted(dic.iteritems(), key=lambda (k,v): (v[0]*1.0/v[1],k))]

def sort_dic_by_value(dic):
    """
    input a dictionary, output a list of tuples (key, value), sorted by the values
    """
    return [(k, v) for k,v in sorted(dic.iteritems(), key=lambda (k,v): (v,k))]

def sep_ngraph(lis):
    """
    input a list of ngraphs, return the result having digraphs and trigraphs seperated
    """
    digraphs=[t for t in lis if len(t[0])==2]
    trigraphs=[t for t in lis if len(t[0])==3]
    return digraphs, trigraphs

def calculate_result(test_sample, profile_sample):

    test_digraphs, test_trigraphs = sep_ngraph(test_sample)

    profile_digraphs, profile_trigraphs = sep_ngraph(profile_sample)

    test_ngraphs = [test_digraphs]
    profile_ngraphs = [profile_digraphs]
    result = []
    if A_MEASURE:
        result = distance_score.handle_a_measure(test_ngraphs, profile_ngraphs, result)
    if R_MEASURE:
        result = distance_score.handle_r_measure(test_ngraphs, profile_ngraphs, result)

    #dis_score= [result[0]*0.45+result[1]*0.1 + result[2]*0.45]+  result
    dis_score= result[0]*0.45+result[1]*0.1 + result[2]*0.45
    return dis_score#> THRE


def parse(keystrokes):
    k = [i for i in keystrokes if i[2]==0]
    dic = {}
    for i in range(len(k)-1):
        digraph = str(k[i][1]+ k[i+1][1])
        if 'Backspace' in digraph: continue
        time_diff = k[i+1][0]-k[i][0]
        if 30<= time_diff <= 500:
            dic.setdefault(digraph, [])
            dic[digraph].append(time_diff)
    dic2 = []
    for i in dic:
        dic2.append((i, sum(dic[i])*1.0/len(dic[i])))
    return dic2


def run(profile_sample, test_sample = None):

    profile_sample = parse(profile_sample)
    file = open('data.txt')
    test_sample = []
    for line in file:
        line = line.strip().split('\t')
        #print line
        if len(line)<2: continue
        #print 'at least 2', line
        if line[2]!= '0':continue
        #print 'not equal 0', line
        test_sample.append((int(line[0]), line[1],int(line[2])))
    test_sample = sorted(test_sample)
    test_sample = parse(test_sample)
    return calculate_result(test_sample, profile_sample)

THRE = 0.43

if __name__ == "__main__":

    #for ite in range(10):
        #THRE = 0.5-ite/100.0
        #calculate_result(test_size, profile_size)
    profile_sample = [(379975653, u' ', 0), (379975780, u'i', 0), (379975916, u's', 0), (379976013, u' ', 0), (379976189, u'a', 0), (379976412, u' ', 0), (379976628, u's', 0), (379976788, u'e', 0), (379976868, u'n', 0), (379977100, u't', 0), (379977204, u'e', 0), (379977333, u'n', 0), (379977532, u'c', 0), (379977740, u'e', 0), (379995485, u'Enter', 0), (379995909, u't', 0), (379996061, u'h', 0), (379996172, u'i', 0), (379996372, u' ', 0), (379996493, u's', 0), (379997212, u' ', 0), (379997371, u'i', 0), (379997516, u's', 0), (379997596, u' ', 0), (379997940, u'a', 0), (379998061, u'n', 0), (379998220, u'o', 0), (379998412, u't', 0), (379998533, u'h', 0), (379998677, u'e', 0), (379998741, u'r', 0), (379999651, u'Enter', 0), (380000428, u'a', 0), (380000628, u' ', 0), (380000885, u't', 0), (380000948, u'h', 0), (380001196, u'i', 0), (380001325, u'r', 0), (380001493, u'd', 0), (385950171, u'j', 0), (385950562, u'f', 0), (385950643, u'e', 0), (385950819, u'a', 0), (385951404, u'z', 0), (405010163, u'T', 0), (405010355, u'h', 0), (405010490, u'i', 0), (405010674, u's', 0), (405010779, u' ', 0), (405010963, u'i', 0), (405011202, u's', 0), (405011314, u' ', 0), (405011474, u't', 0), (405011555, u'h', 0), (405011666, u'e', 0), (405012018, u' ', 0), (405012508, u'p', 0), (405012635, u'r', 0), (405012747, u'o', 0), (405013627, u't', 0), (405013795, u'r', 0), (405013883, u'a', 0), (405014299, u'i', 0), (405014531, u'n', 0), (405014683, u'i', 0), (405014811, u'n', 0), (405014940, u'g', 0), (405015147, u' ', 0), (405015548, u'p', 0), (405015674, u'a', 0), (405015819, u'g', 0), (405015955, u'e', 0), (405016083, u'.', 0), (405016547, u' ', 0), (405016915, u'I', 0), (405017171, u' ', 0), (405017395, u'n', 0), (405017515, u'e', 0), (405017714, u'e', 0), (405018131, u'd', 0), (405018283, u' ', 0), (405018412, u't', 0), (405018547, u'o', 0), (405018746, u' ', 0), (405019019, u't', 0), (405019179, u'r', 0), (405019284, u'a', 0), (405019403, u'i', 0), (405019514, u'n', 0), (405019762, u' ', 0), (405020011, u'f', 0), (405020515, u'i', 0), (405020619, u'n', 0), (405020858, u' ', 0), (405021243, u'o', 0), (405021356, u'r', 0), (405021571, u'd', 0), (405021755, u'e', 0), (405021859, u'r', 0), (405021938, u' ', 0), (405022195, u't', 0), (405023195, u'f', 0), (405023786, u'o', 0), (405023923, u'r', 0), (405024018, u' ', 0), (405024162, u't', 0), (405024275, u'h', 0), (405024410, u'i', 0), (405024556, u's', 0), (405024659, u' ', 0), (405024828, u't', 0), (405024978, u'h', 0), (405025523, u'i', 0), (405025675, u'n', 0), (405025755, u'g', 0), (405025899, u' ', 0), (405026138, u't', 0), (405026251, u'o', 0), (405026403, u' ', 0), (405026580, u'w', 0), (405026690, u'o', 0), (405026830, u'r', 0), (405026931, u'k', 0), (405027666, u'.', 0), (405027891, u' ', 0), (405034275, u'Enter', 0), (405035299, u'T', 0), (405035444, u'h', 0), (405035587, u'i', 0), (405035739, u's', 0), (405035795, u' ', 0), (405036076, u'i', 0), (405036346, u's', 0), (405036531, u' ', 0), (405036666, u'a', 0), (405036835, u' ', 0), (405037076, u's', 0), (405037235, u'e', 0), (405037291, u'n', 0), (405037579, u't', 0), (405037699, u'e', 0), (405037804, u'n', 0), (405038003, u'c', 0), (405038203, u'e', 0), (405038434, u'.', 0), (405038666, u' ', 0), (405039059, u'T', 0), (405039267, u'h', 0), (405039427, u'i', 0), (405039563, u's', 0), (405039699, u' ', 0), (405039923, u'i', 0), (405040163, u's', 0), (405040316, u' ', 0), (405040547, u'a', 0), (405040907, u' ', 0), (405041234, u'n', 0), (405042395, u'n', 0), (405042603, u'o', 0), (405043035, u't', 0), (405043139, u'h', 0), (405043331, u'e', 0), (405043427, u'r', 0), (405043555, u'.', 0), (405043923, u' ', 0), (405044903, u'I', 0), (405045107, u' ', 0), (405045266, u'n', 0), (405045395, u'e', 0), (405045531, u'e', 0), (405045803, u'd', 0), (405045923, u' ', 0), (405046123, u't', 0), (405046315, u'o', 0), (405046499, u' ', 0), (405046683, u'p', 0), (405046820, u'a', 0), (405047003, u's', 0), (405047154, u's', 0), (405047347, u' ', 0), (405047490, u't', 0), (405047642, u'h', 0), (405047755, u'e', 0), (405048035, u' ', 0), (405048227, u't', 0), (405048378, u'e', 0), (405048467, u's', 0), (405048594, u't', 0), (405048915, u'.', 0), (405049597, u' ', 0), (405050163, u'P', 0), (405050515, u'e', 0), (405050803, u'r', 0), (405050962, u'i', 0), (405051108, u'i', 0), (405051110, u'o', 0), (405051315, u'd', 0), (405052634, u'd', 0), (405052850, u'.', 0), (405055236, u'i', 0), (405055651, u'o', 0), (405055803, u'd', 0), (405055979, u'.', 0)]

    print run(profile_sample)