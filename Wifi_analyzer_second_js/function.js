


var fs = require('fs');
var myFile = "myjson.txt";
var jsObj = fs.readFileSync(myFile, 'utf8');

// jsObj - object with data on the wifi channels.

var wifi_input = JSON.parse(jsObj);
console.log(result_function(wifi_input));

// Reading data json and initializing

function result_function(wifi_input) {
    
    // How many channels from which we choose

    var t = 13;

    // Frequency of the first channel

    var ALF = 2412;

    var channel_parse = parse_function(wifi_input);

    // g - The impact pool on the channels, from the first to the last
    // channel. Taking into account all the effects of signal sections.
    
    var g = [];
    
    var n=0;
    var next;

    while (n < (t + 0)) {
        next = computational_function(n, channel_parse, ALF, t);
        g[n] = next;
        n += 1;
    }

    return g;
}

function parse_function(wifi_input) {

    var channel = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
    var wifi_output = {};
    var channel_temp = {};
    var point_data = {};
    var chan;
    var max_temp;
    var k;

    for (var key in wifi_input) {
        var index = key.split('.');

        if (wifi_output[index[7]] == undefined) {
            wifi_output[index[7]] = { bssid: '', rssi: '', channel: ''};
        }

        if (index[8] == 'RSSI') {            
            wifi_output[index[7]].rssi = parseInt(wifi_input[key]);
        }
        if (index[8] == 'BSSID') {          
            wifi_output[index[7]].bssid = wifi_input[key];
        }
        if (index[8] == 'Channel') {
            wifi_output[index[7]].channel = wifi_input[key];
        }
    }

    for (var key in wifi_output) {
        chan = parseInt(wifi_output[key].channel);
        if (channel_temp[chan] == undefined) {
            channel_temp[chan] = [];
        }
        channel_temp[chan].push(wifi_output[key].rssi);
    }
    
    for (var key in channel_temp) {
        channel[parseInt(key) - 1] = Math.pow(10.0, (Math.max.apply(null, channel_temp[key])/10.0));
    }
   
    return channel;
}

// A section of the program in which the best channel is selected from the
// pool of channels.


// A set of functions. They are an integral of the signal envelope
// function at different sites.
// Sites (in MHz from the frequency of the selected channel):
// 1) -infinity to -20
// 2) -20 to -11
// 3) -11 to -9
// 4) -9 to 9
// 5) 9 to 11
// 6) 11 to 20
// 7) 20 to infinity

// y - Signal strength
// x - The point for which we assume the integral


function function1(y, x) {
    return 0;
}

function function2(y, x) {
    result = y*((7.0/(16300.0*2))*x*x + (12.0/815.0)*x);
    return result;
}

function function3(y, x) {
    result = y*((99.0/(200.0*2))*x*x + (1091.0/200.0)*x);
    return result;
}

function function4(y, x) {
    result = y * x;
    return result;
}

function function5(y, x) {
    result = y*((-99.0/(200.0*2))*x*x + (1091.0/200.0)*x);
    return result;
}

function function6(y, x) {
    result = y*((-7.0/(16300.0*2))*x*x + (12.0/815.0)*x);
    return result;
}

function function7(y, x) {
    return 0;
}

// A set of functions that get the value of integrals from previous
// functions for an interval.

// Sites (in MHz from the frequency of the selected channel):
// 1) -20 to -11
// 2) -11 to -9
// 3) -9 to 9
// 4) 9 to 11
// 5) 11 to 20
// For other sites do not count, so obviously the value will be zero.

// y - Signal strength
// x2 - The point for which we assume the integral, which is greater than
// the value of the second
// x2 - The point for which we assume the integral, which is less than
// the value of the second


function sumFunction1(y, x2, x1) {
    result = function2(y, x2) - function2(y, x1);
    return result;
}

function sumFunction2(y, x2, x1) {
    result = function3(y, x2) - function3(y, x1);
    return result;
}

function sumFunction3(y, x2, x1) {
    result = function4(y, x2) - function4(y, x1);
    return result;
}

function sumFunction4(y, x2, x1) {
    result = function5(y, x2) - function5(y, x1);
    return result;
}

function sumFunction5(y, x2, x1) {
    result = function6(y, x2) - function6(y, x1);
    return result;
}


// A function that generates a calculation for the pool from the
// calculation conditions and boundary points.

function choice_of_coordinates_all(dictionary, key_number_first) {


    var key_number_temp = [0, 0, 0, 0, 0, 0];
    var key_number = 0;
    var min_dict;
    key_number_temp[4] = key_number_first[2];

    
    if ((key_number_first[0] == 0) && (key_number_first[1] == 0)) {
        choice_of_coordinates(0, 1);
        while ((key_number_temp[0] == 0) || (key_number_temp[1] == 0)) {
            choice_of_coordinates(0, 1);
        }
    }
    else if ((key_number_first[0] == 0) && (key_number_first[1] != 0)) {
        console.log("error 400");
    }
    else if (key_number_first[1] != 0) {
        key_number_temp[0] = key_number_first[0];
        key_number_temp[1] = key_number_first[1];
    }

    if ((key_number_temp[2] == 0) && (key_number_temp[3] == 0)) {
        choice_of_coordinates(2, 3);
    }

    var result = {res1: key_number_temp, res2: dictionary};
    return result;

    // A function that selects a pair of points and only one with the
    // lowest value and removes them from the point pool.

    function choice_of_coordinates(n1, n2) {

        for (var key in dictionary) {
            //console.log(key);
            //console.log(dictionary[key]);

            min_dict = dictionary[key];

            for (var k in dictionary) {
                if (dictionary[k] < min_dict) {
                    min_dict = dictionary[k];
                }
            }
        
            if (dictionary[key] == min_dict) {//Math.min.apply(null, dictionary)
                
                var dic_count = 0;
                for (var key_temp in dictionary) {
                    if (dictionary[key_temp] == dictionary[key]){
                        dic_count++;
                    }
                }

                if (dic_count == 1) {
                    var index = key.split('.');

                    if (index[0] == 'x') {
                        key_number = index[1];
                        key_number_temp[n1] = key_number;
                        //for (var k2 in dictionary) {
                        //  if (dictionary[k2] < min_dict) {
                        //      
                        //  }
                        //}

                    }
                    else if (index[0] == 'i') {
                        key_number = index[1];
                        key_number_temp[n2] = key_number;
                    }
                    if (key_number_temp[4] == 0) {
                        if ((key_number_temp[0] == 0) || (key_number_temp[1] == 0)) {
                            delete dictionary[key];
                            break;
                        }
                        key_number_temp[4] = key;
                    }
                    else {
                        key_number_temp[5] = key;
                    }
                    delete dictionary[key];
                    break;
                }
                else if (dic_count == 2) {
                    var index = key.split(".");

                    if (index[0] == 'x') {

                        key_number = index[1];

                        key_number_temp[n1] = key_number;

                        for (var key2 in dictionary) {
                            var index2 = key2.split('.');

                            if ((dictionary[key2] == dictionary[key]) && (index2[0] == 'i')) {
                                key_number = index2[1];
                                key_number_temp[n2] = key_number;

                                if (key_number_temp[4] == 0) {
                                    key_number_temp[4] = key2;
                                }
                                else {
                                    key_number_temp[5] = key;
                                }

                                delete dictionary[key];
                                delete dictionary[key2];
                                break;
                            }
                        }
                    }
                    else if (index[0] == 'i') {

                        key_number = index[1];
                        key_number_temp[n2] = key_number;

                        for (var key2 in dictionary) {

                            if ((dictionary[key2] == dictionary[key]) && (index2[0] == 'x')) {
                                key_number = index2[1];
                                key_number_temp[n1] = key_number;

                                if (key_number_temp[4] == 0) {
                                    key_number_temp[4] = key;
                                }
                                else {
                                    key_number_temp[5] = key2;
                                }
                                delete dictionary[key];
                                delete dictionary[key2];
                                break;
                            }
                        }
                    }
                break;
                }
            }
            else {
                continue;
            }
        }
    }
}

// A function that receives input values, a selected channel, a channel
// list with receive strength, a low-frequency level of the minimum
// channel, and a number of channels. Displays the interference level
// for the selected channel.

function computational_function(x, channel_parse, ALF, t) {

    // Function of selection of integration function and integration
    // conditions, gives the result of integration.

    function billing_function(key_number_temp, lis, power) {

        if (key_number_temp[0] == 0) {
            console.log("error !!!");
        }
        if (key_number_temp[1] == 0) {
            console.log("error !!!!");
        }   
        if (key_number_temp[0] == 1) {
            koeff = 1.0/163.0;
        }
        else if (key_number_temp[0] == 2) {
            koeff = 1.0/100.0;
        }
        else if (key_number_temp[0] == 3) {
            koeff = 1.0;
        }
        else if (key_number_temp[0] == 4) {
            koeff = 1.0/100.0;
        }
        else if (key_number_temp[0] == 5) {
            koeff = 1.0/163.0;
        }
        else if (key_number_temp[0] == 6) {
            koeff = 0.0;
        }

        x1 = parseInt(lis[key_number_temp[4]]) - i0;
        x2 = parseInt(lis[key_number_temp[5]]) - i0;

        if (key_number_temp[1] == 1) {
            s = sumFunction1(power, x2, x1);
        }
        else if (key_number_temp[1] == 2) {
            s = sumFunction2(power, x2, x1);
        }
        else if (key_number_temp[1] == 3) {
            s = sumFunction3(power, x2, x1);
        }
        else if (key_number_temp[1] == 4) {
            s = sumFunction4(power, x2, x1);
        }
        else if (key_number_temp[1] == 5) {
            s = sumFunction5(power, x2, x1);
        }
        else if (key_number_temp[1] == 6) {
            s = 0.0;
        }
        return s*koeff;
    }

    var lix = {};
    var lii = {};   
    var koeff = 0;
    var power = 1;
    var i = 0;
    var summ = 0;
    var channel = channel_parse;
    lix['x.1'] = ALF + 5*x - 20;
    lix['x.2'] = ALF + 5*x - 11;
    lix['x.3'] = ALF + 5*x - 9;
    lix['x.4'] = ALF + 5*x + 9;
    lix['x.5'] = ALF + 5*x + 11;
    lix['x.6'] = ALF + 5*x + 20;

    // Re-election on all channels.

    while (i < (t + 0)) {

        var s = 0;
        var key_number = [0, 0, 0, 0];
        var key_number_first = [0, 0, 0];
        var i0 = ALF + 5*i;
        var lis = {};
        var lis_temp = {};
        var key_number_temp;
        lii['i.1'] = ALF + 5*i - 20;
        lii['i.2'] = ALF + 5*i - 11;
        lii['i.3'] = ALF + 5*i - 9;
        lii['i.4'] = ALF + 5*i + 9;
        lii['i.5'] = ALF + 5*i + 11;
        lii['i.6'] = ALF + 5*i + 20;

        for (var key in lix) {
            lis[key] = lix[key];
        }
        for (var key in lii) {
            lis[key] = lii[key];
        }
        for (var key in lis) {
            lis_temp[key] = lis[key];
        }       

        // Reselection across the entire pool of coordinates to
        // calculate for the selected channel.

        while (Object.keys(lis_temp).lenght != 0) {

            var ex = choice_of_coordinates_all(lis_temp, key_number_first);

            key_number_temp = ex.res1;
            lis_temp = ex.res2;

            if ((key_number_temp[2] == 0) && (key_number_temp[0] != 0)) {
                key_number_first[0] = key_number_temp[0];
            }
            else if (key_number_temp[2] != 0) {
                key_number_first[0] = key_number_temp[2];
            }
            else {
                console.log("error 401");
            }
            if ((key_number_temp[3] == 0) && (key_number_temp[1] != 0)) {
                key_number_first[1] = key_number_temp[1];
            }
            else if (key_number_temp[3] != 0) {
                key_number_first[1] = key_number_temp[3];
            }
            else {
                console.log("error 402");
            }
            if (key_number_temp[5] != 0) {
                key_number_first[2] = key_number_temp[5];
            }
            else {
                console.log("error 403");
            }

            summ += billing_function(key_number_temp, lis, channel[i]);

            if ((key_number_temp[2] == 6) || (key_number_temp[3] == 6)) {
                break;
            }
        } 
        i += 1;
    }
    return summ*10;
}
