#!/usr/bin/python2

# The first part of the program

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
        # print (n + 1)
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

    # return g

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

    for n in channel_temp:
        channel_temp[n] = max(channel_temp[n])

    # print channel_temp

    print channel_temp
    channel_temp = {1: -21, 3: -30, 6: -42, 9: -71, 11: -68, 12: -81}
    print channel_temp

    for k, val in channel_temp.items():
        # print k
        # print val
        channel[k-1] = 10.0**(val/10.0)

    return channel


# The second part of the program

# A section of the program in which the best channel is selected from the
# pool of channels.


#channel = [0, 0, 100, 0, 0, 0, 40, 0, 0, 0, 100, 0, 0]
#channel = [100, 0, 0, 0, 0, 100, 0, 0, 0, 0, 100, 0, 0]
#channel = [10, 0, 0, 0, 10, 0, 0, 0, 10, 0, 10, 0, 0]
#channel = [10, 10, 100, 10, 10, 10, 40, 10, 10, 10, 100, 10, 10]
#channel = [0.025119, 0, 0, 0, 0.000158, 0, 0, 0, 0.000398, 0, 0.063096, 0, 0]


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

# The function of determining the level of interference on the selected
# channel (x). Produces the distribution in which areas to use the
# integration functions described above.


def computational_function(x, channel_parse, ALF, t):
    
    channel = channel_parse
    # Points of kink of the envelope function for the channel of which
    # we calculate.
    
    x0 = ALF + 5*x    
    x1 = ALF + 5*x - 20
    x2 = ALF + 5*x - 11
    x3 = ALF + 5*x - 9
    x4 = ALF + 5*x + 9
    x5 = ALF + 5*x + 11
    x6 = ALF + 5*x + 20
    
    # i - Channel number that creates impact
    
    i = 0
    
    # The sum of the effects of all sections of the signal of all
    # channels.
    
    ss = 0
    
    # The sum of the effects of the central sections of the signal of
    # all channels.
    
    sss = 0

    # We are doing the number of the channel for the time being, the
    # number of possible channels.
    
    while i < (t + 0):

        # The sum of the interference from other channels in the section
        # from -9 to 9 for the computed channel.
        
        s1 = 0
        
        # The sum of the interference from other channels in the section
        # from -11 to -9 and 9 to 11 for the computed channel.
        
        s2 = 0
        
        # The sum of the interference from other channels in the section
        # from -20 to -11 and 11 to 20 for the computed channel.
        
        s3 = 0
        
        # Breakpoints of the envelope function for channels that create
        # an impact, including our channel.
        
        i0 = ALF + 5*i
        i1 = ALF + 5*i - 20
        i2 = ALF + 5*i - 11
        i3 = ALF + 5*i - 9
        i4 = ALF + 5*i + 9
        i5 = ALF + 5*i + 11
        i6 = ALF + 5*i + 20

        # Calculation for the case when the selected channel is not empty
        # and not on the same channel as the calculated one.
        
        if (channel[i-0] != 0) and (i != x):

            
            # The case where the selected channel is intersected by
            # frequencies with the calculated ones and lies to the
            # left of it along the frequency axis.
            
            if ((i6 > x1) and (x6 > i6)):
                
                # Option when the number of channels differs by seven.
                
                if (i6 < x2):
                    s3 = s3 + sumFunction5(channel[i-0], i6-i0, x1-i0)
                
                # Option when the number of channels differs by six.
                
                elif (i6 < x3):
                    s2 = s2 + sumFunction5(channel[i-0], i6-i0, x2-i0)
                    s3 = s3 + sumFunction5(channel[i-0], x2-i0, i5-i0)
                    s3 = s3 + sumFunction4(channel[i-0], i5-i0, x1-i0)
                
                # Option when the number of channels differs by five.
                
                elif ((i6 - x1) == 15):
                    s1 = s1 + sumFunction5(channel[i-0], i6-i0, x3-i0)
                    s2 = s2 + sumFunction5(channel[i-0], x3-i0, x2-i0)
                    s3 = s3 + sumFunction5(channel[i-0], x2-i0, i5-i0)
                    s3 = s3 + sumFunction4(channel[i-0], i5-i0, i4-i0)
                    s3 = s3 + sumFunction3(channel[i-0], i4-i0, x1-i0)
                
                # Option when the number of channels differs by four.
                
                elif ((i6 - x1) == 20):
                    s1 = s1 + sumFunction5(channel[i-0], i6-i0, i5-i0)
                    s2 = s2 + sumFunction4(channel[i-0], i5-i0, i4-i0)
                    s3 = s3 + sumFunction3(channel[i-0], i4-i0, x1-i0)
                
                # Option when the number of channels differs by three.
                
                elif ((i6 - x1) == 25):
                    s1 = s1 + sumFunction5(channel[i-0], i6-i0, i5-i0)
                    s1 = s1 + sumFunction4(channel[i-0], i5-i0, i4-i0)
                    s1 = s1 + sumFunction3(channel[i-0], i4-i0, x3-i0)
                    s2 = s2 + sumFunction3(channel[i-0], x3-i0, x2-i0)
                    s3 = s3 + sumFunction3(channel[i-0], x2-i0, x1-i0)
                
                # Option when the number of channels differs by two.
                
                elif ((i6 - x1) == 30):
                    s2 = s2 + sumFunction5(channel[i-0], i6-i0, x4-i0)
                    s1 = s1 + sumFunction5(channel[i-0], x4-i0, i5-i0)
                    s1 = s1 + sumFunction4(channel[i-0], i5-i0, i4-i0)
                    s1 = s1 + sumFunction3(channel[i-0], i4-i0, x3-i0)
                    s2 = s2 + sumFunction3(channel[i-0], x3-i0, x2-i0)
                    s3 = s3 + sumFunction3(channel[i-0], x2-i0, i3-i0)
                    s3 = s3 + sumFunction2(channel[i-0], i3-i0, x1-i0)
                
                # Option when the number of channels differs by one.
                
                elif ((i6 - x1) == 35):
                    s3 = s3 + sumFunction5(channel[i-0], i6-i0, x5-i0)
                    s2 = s2 + sumFunction5(channel[i-0], x5-i0, x4-i0)
                    s1 = s1 + sumFunction5(channel[i-0], x4-i0, i5-i0)
                    s1 = s1 + sumFunction4(channel[i-0], i5-i0, i4-i0)
                    s1 = s1 + sumFunction3(channel[i-0], i4-i0, x3-i0)
                    s2 = s2 + sumFunction3(channel[i-0], x3-i0, x2-i0)
                    s3 = s3 + sumFunction3(channel[i-0], x2-i0, i3-i0)
                    s3 = s3 + sumFunction2(channel[i-0], i3-i0, i2-i0)
                    s3 = s3 + sumFunction1(channel[i-0], i2-i0, x1-i0)

            # The case where the selected channel is intersected by
            # frequencies with the calculated ones and lies to the
            # right of it along the frequency axis.
           
            elif ((i1 > x1) and (x6 > i1)):
                
                # Option when the number of channels differs by seven.
                
                if (i1 > x5):
                    s3 = s3 + sumFunction1(channel[i-0], x6-i0, i1-i0)
                
                # Option when the number of channels differs by six.
                
                elif (i1 > x4):
                    s2 = s2 + sumFunction1(channel[i-0], x5-i0, i1-i0)
                    s3 = s3 + sumFunction1(channel[i-0], i2-i0, x5-i0)
                    s3 = s3 + sumFunction2(channel[i-0], x6-i0, i2-i0)
                
                # Option when the number of channels differs by five.
                
                elif ((x6 - i1) == 15):
                    s1 = s1 + sumFunction1(channel[i-0], x4-i0, i1-i0)
                    s2 = s2 + sumFunction1(channel[i-0], x5-i0, x4-i0)
                    s3 = s3 + sumFunction1(channel[i-0], i2-i0, x5-i0)
                    s3 = s3 + sumFunction2(channel[i-0], i3-i0, i2-i0)
                    s3 = s3 + sumFunction3(channel[i-0], x6-i0, i3-i0)
                
                # Option when the number of channels differs by four.
                
                elif ((x6 - i1) == 20):
                    s1 = s1 + sumFunction1(channel[i-0], i2-i0, i1-i0)
                    s2 = s2 + sumFunction2(channel[i-0], i3-i0, i2-i0)
                    s3 = s3 + sumFunction3(channel[i-0], x6-i0, i3-i0)
                
                # Option when the number of channels differs by three.
                
                elif ((x6 - i1) == 25):
                    s1 = s1 + sumFunction1(channel[i-0], i2-i0, i1-i0)
                    s1 = s1 + sumFunction2(channel[i-0], i3-i0, i2-i0)
                    s1 = s1 + sumFunction3(channel[i-0], x4-i0, i3-i0)
                    s2 = s2 + sumFunction3(channel[i-0], x5-i0, x4-i0)
                    s3 = s3 + sumFunction3(channel[i-0], x6-i0, x5-i0)
                
                # Option when the number of channels differs by two.
                
                elif ((x6 - i1) == 30):
                    s2 = s2 + sumFunction1(channel[i-0], x3-i0, i1-i0)
                    s1 = s1 + sumFunction1(channel[i-0], i2-i0, x3-i0)
                    s1 = s1 + sumFunction2(channel[i-0], i3-i0, i2-i0)
                    s1 = s1 + sumFunction3(channel[i-0], x4-i0, i3-i0)
                    s2 = s2 + sumFunction3(channel[i-0], x5-i0, x4-i0)
                    s3 = s3 + sumFunction3(channel[i-0], i4-i0, x5-i0)
                    s3 = s3 + sumFunction4(channel[i-0], x6-i0, i4-i0)
                
                # Option when the number of channels differs by one.
                
                elif ((x6 - i1) == 35):
                    s3 = s3 + sumFunction1(channel[i-0], x2-i0, i1-i0)
                    s2 = s2 + sumFunction1(channel[i-0], x3-i0, x2-i0)
                    s1 = s1 + sumFunction1(channel[i-0], i2-i0, x3-i0)
                    s1 = s1 + sumFunction2(channel[i-0], i3-i0, i2-i0)
                    s1 = s1 + sumFunction3(channel[i-0], x4-i0, i3-i0)
                    s2 = s2 + sumFunction3(channel[i-0], x5-i0, x4-i0)
                    s3 = s3 + sumFunction3(channel[i-0], i4-i0, x5-i0)
                    s3 = s3 + sumFunction4(channel[i-0], i5-i0, i4-i0)
                    s3 = s3 + sumFunction5(channel[i-0], x6-i0, i5-i0)

            # The case when the channels do not intersect.
            
            else:
                s1 += 0
                s2 += 0
                s3 += 0
                
            s = (s1 + (s2*(1.0/100.0)) + (s3*(1.0/163.0)))
            s0 = (s1 + (s2*(1.0/100.0)))
            i += 1
        
        # Calculation for the case when the selected channel is on the
        # same channel as the calculated one.
        
        elif (i == x):
            s3 = s3 + sumFunction1(channel[i-0], i2-i0, i1-i0)
            s2 = s2 + sumFunction2(channel[i-0], i3-i0, i2-i0)
            s1 = s1 + sumFunction3(channel[i-0], i4-i0, i3-i0)
            s2 = s2 + sumFunction4(channel[i-0], i5-i0, i4-i0)
            s3 = s3 + sumFunction5(channel[i-0], i6-i0, i5-i0)
            s = (s1 + (s2*(1.0/100.0)) + (s3*(1.0/163.0)))
            s0 = (s1 + (s2*(1.0/100.0)))
            i += 1

        # Calculation for the case where the selected channel is empty.
        
        else:
            s1 += 0
            s2 += 0
            s3 += 0
            s = s1 + s2*(1.0/100.0) + s3*(1.0/163.0)
            s0 = (s1 + (s2*(1.0/100.0)))
            i += 1

        ss += s
        sss += s0
    
    # Adding to the result pool on the channel.
    
    # g.append(ss*10)
    # h.append(sss*10)
    return ss*10



if __name__ == "__main__":
    myFile = "myjson.txt"
    jsObj = open(myFile, mode = 'r')
    wifi_input = json.load(jsObj)
    print (result_function(wifi_input))
    jsObj.close()



