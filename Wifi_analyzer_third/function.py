#!/usr/bin/python2

from copy import deepcopy
import json

# Reading data json and initializing

def result_function(wifi_input):
    
    # How many channels from which we choose

    t = 13

    # Frequency of the first channel

    ALF = 2412

    channel_parse = parse_function(wifi_input)

    # g - The impact pool on the channels, from the first to the last
    # channel. Taking into account all the effects of signal sections.
    
    g = []
    
    n=0
    while n < (t + 0):

        g.append(computational_function(n, channel_parse, ALF, t))
        n += 1

    k = max(g)
    n = 0
    h = []
    while n < (t + 0):
        h.append(g[n]/k)
        n += 1
    print k
    return h


def parse_function(wifi_input):

    channel = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    wifi_output = {}
    channel_temp = {}
    tr_prefix = 'InternetGatewayDevice.LANDevice.1.WiFi.Radio.1.X_MGTS_NeighborAP'

    for key in wifi_input:
        index = int(key.split(".")[-2])
        wifi_output[index] = {
            'rssi': int(wifi_input['%s.%s.RSSI' % (tr_prefix, index)]),
            'bssid': wifi_input['%s.%s.BSSID' % (tr_prefix, index)],
            'channel': int(wifi_input['%s.%s.Channel' % (tr_prefix, index)])
        }

    for point_data in wifi_output.values():
        if point_data['channel'] not in channel_temp:
            channel_temp[point_data['channel']] = []
        channel_temp[point_data['channel']].append(point_data['rssi'])

    print channel_temp

    for n in channel_temp:
        channel_temp[n] = max(channel_temp[n])

    print channel_temp
    channel_temp = {1: -21, 3: -30, 6: -42, 9: -71, 11: -68, 12: -81}
    print channel_temp

    for k, val in channel_temp.items():
        channel[k-1] = 10.0**(val/10.0)

    print channel
    return channel


# A section of the program in which the best channel is selected from the
# pool of channels.


# A set of functions. They are an integral of the signal envelope
# function at different sites.
# Sites (in MHz from the frequency of the selected channel):
# 1) -infinity to -20
# 2) -20 to -11
# 3) -11 to -9
# 4) -9 to 9
# 5) 9 to 11
# 6) 11 to 20
# 7) 20 to infinity

# y - Signal strength
# x - The point for which we assume the integral


def function1(y, x):
    return 0

def function2(y, x):
    result = y*((7.0/(16300.0*2))*x**2 + (12.0/815.0)*x)
    return result

def function3(y, x):
    result = y*((99.0/(200.0*2))*x**2 + (1091.0/200.0)*x)
    return result

def function4(y, x):
    result = y * x
    return result

def function5(y, x):
    result = y*((-99.0/(200.0*2))*x**2 + (1091.0/200.0)*x)
    return result

def function6(y, x):
    result = y*((-7.0/(16300.0*2))*x**2 + (12.0/815.0)*x)
    return result

def function7(y, x):
    return 0


# A set of functions that get the value of integrals from previous
# functions for an interval.

# Sites (in MHz from the frequency of the selected channel):
# 1) -20 to -11
# 2) -11 to -9
# 3) -9 to 9
# 4) 9 to 11
# 5) 11 to 20
# For other sites do not count, so obviously the value will be zero.

# y - Signal strength
# x2 - The point for which we assume the integral, which is greater than
# the value of the second
# x2 - The point for which we assume the integral, which is less than
# the value of the second


def sumFunction1(y, x2, x1):
    result = function2(y, x2) - function2(y, x1)
    return result

def sumFunction2(y, x2, x1):
    result = function3(y, x2) - function3(y, x1)
    return result

def sumFunction3(y, x2, x1):
    result = function4(y, x2) - function4(y, x1)
    return result

def sumFunction4(y, x2, x1):
    result = function5(y, x2) - function5(y, x1)
    return result

def sumFunction5(y, x2, x1):
    result = function6(y, x2) - function6(y, x1)
    return result


# A function that generates a calculation for the pool from the
# calculation conditions and boundary points.

def choice_of_coordinates_all(dictionary, key_number_first):


    # A function that selects a pair of points and only one with the
    # lowest value and removes them from the point pool.

    def choice_of_coordinates(n1, n2):

        for key, value in dictionary.items():
        
            if value == min(dictionary.values()):
                l = dictionary.values().count(value)

                if l == 1:
                    index = key.split(".")[0]

                    if index == "x":

                        key_number = int(key.split(".")[1])
                        key_number_temp[n1] = key_number

                    elif index == "i":
                        key_number = int(key.split(".")[1])
                        key_number_temp[n2] = key_number

                    if (key_number_temp[4] == 0):
                        if ((key_number_temp[0] == 0) or\
                            (key_number_temp[1] == 0)):
                            del dictionary[key]
                            break
                        key_number_temp[4] = key
                    else:
                        key_number_temp[5] = key
                    del dictionary[key]
                    break

                elif l == 2:
                    index = key.split(".")[0]

                    if index == "x":
                        key_number = int(key.split(".")[1])
                        key_number_temp[n1] = key_number

                        for key2, value2 in dictionary.items():

                            if (value2 == value)\
                                and (key2.split(".")[0] == "i"):
                                key_number = int(key2.split(".")[1])
                                key_number_temp[n2] = key_number

                                if (key_number_temp[4] == 0):
                                    key_number_temp[4] = key2
                                else:
                                    key_number_temp[5] = key
                                del dictionary[key]
                                del dictionary[key2]
                                break

                    elif index == "i":
                        key_number = int(key.split(".")[1])
                        key_number_temp[n2] = key_number

                        for key2, value2 in dictionary.items():

                            if (value2 == value)\
                                and (key2.split(".")[0] == "x"):
                                key_number = int(key2.split(".")[1])
                                key_number_temp[n1] = key_number

                                if (key_number_temp[4] == 0):
                                    key_number_temp[4] = key
                                else:
                                    key_number_temp[5] = key2
                                del dictionary[key]
                                del dictionary[key2]
                                break

                break

            else:
                continue


    key_number_temp = [0, 0, 0, 0, 0, 0]
    key_number = 0
    key_number_temp[4] = key_number_first[2]

    
    if (key_number_first[0] == 0) and (key_number_first[1] == 0):
        choice_of_coordinates(0, 1)

        while (key_number_temp[0] == 0) or (key_number_temp[1] == 0):
            choice_of_coordinates(0, 1)

    elif (key_number_first[0] == 0) and (key_number_first[1] != 0):
        print "error 400"
    elif (key_number_first[1] != 0):
        key_number_temp[0] = key_number_first[0]
        key_number_temp[1] = key_number_first[1]

    if (key_number_temp[2] == 0) and (key_number_temp[3] == 0):
        choice_of_coordinates(2, 3)


    return key_number_temp, dictionary


# A function that receives input values, a selected channel, a channel
# list with receive strength, a low-frequency level of the minimum
# channel, and a number of channels. Displays the interference level
# for the selected channel.

def computational_function(x, channel_parse, ALF, t):


    # Function of selection of integration function and integration
    # conditions, gives the result of integration.

    def billing_function(key_number_temp, lis, power):

        if (key_number_temp[0] == 0):
            print "error !!!"
        if (key_number_temp[1] == 0):
            print "error !!!!"
    
        if (key_number_temp[0] == 1):
            koeff = 1.0/163.0
        elif (key_number_temp[0] == 2):
            koeff = 1.0/100.0
        elif (key_number_temp[0] == 3):
            koeff = 1.0
        elif (key_number_temp[0] == 4):
            koeff = 1.0/100.0
        elif (key_number_temp[0] == 5):
            koeff = 1.0/163.0
        elif (key_number_temp[0] == 6):
            koeff = 0.0


        x1 = int(lis[key_number_temp[4]]) - i0
        x2 = int(lis[key_number_temp[5]]) - i0


        if (key_number_temp[1] == 1):
            s = sumFunction1(power, x2, x1)
        elif (key_number_temp[1] == 2):
            s = sumFunction2(power, x2, x1)
        elif (key_number_temp[1] == 3):
            s = sumFunction3(power, x2, x1)
        elif (key_number_temp[1] == 4):
            s = sumFunction4(power, x2, x1)
        elif (key_number_temp[1] == 5):
            s = sumFunction5(power, x2, x1)
        elif (key_number_temp[1] == 6):
            s = 0.0

        return s*koeff

    lix = {}
    lii = {}
    
    koeff = 0
    power = 1
    i = 0
    summ = 0
    channel = channel_parse

    lix["x.1"] = ALF + 5*x - 20
    lix["x.2"] = ALF + 5*x - 11
    lix["x.3"] = ALF + 5*x - 9
    lix["x.4"] = ALF + 5*x + 9
    lix["x.5"] = ALF + 5*x + 11
    lix["x.6"] = ALF + 5*x + 20

    # Re-election on all channels.

    while i < (t + 0):

        s = 0
        key_number = [0, 0, 0, 0]
        key_number_first = [0, 0, 0]

        i0 = ALF + 5*i    
        lii["i.1"] = ALF + 5*i - 20
        lii["i.2"] = ALF + 5*i - 11
        lii["i.3"] = ALF + 5*i - 9
        lii["i.4"] = ALF + 5*i + 9
        lii["i.5"] = ALF + 5*i + 11
        lii["i.6"] = ALF + 5*i + 20

        lis = dict(lix.items() + lii.items())
        lis_temp = deepcopy(lis)

        # Reselection across the entire pool of coordinates to
        # calculate for the selected channel.

        while (len(lis_temp) != 0):

            key_number_temp,\
            lis_temp = choice_of_coordinates_all(lis_temp,\
                               key_number_first)

        
            if (key_number_temp[2] == 0) and (key_number_temp[0] != 0):
                key_number_first[0] = key_number_temp[0]
            elif (key_number_temp[2] != 0):
                key_number_first[0] = key_number_temp[2]
            else:
                print "error 401"

            if (key_number_temp[3] == 0) and (key_number_temp[1] != 0):
                key_number_first[1] = key_number_temp[1]
            elif (key_number_temp[3] != 0):
                key_number_first[1] = key_number_temp[3]
            else:
                print "error 402"

            if (key_number_temp[5] != 0):
                key_number_first[2] = key_number_temp[5]
            else:
                print "error 403"

            summ += billing_function(key_number_temp, lis, channel[i])

            if ((key_number_temp[2] == 6) or (key_number_temp[3] == 6)):
                break

        i += 1
        
    return summ*10



if __name__ == "__main__":
    myFile = "myjson.txt"
    jsObj = open(myFile, mode = 'r')
    wifi_input = json.load(jsObj)
    print (result_function(wifi_input))
    jsObj.close()



