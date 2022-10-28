from utils.conversions import is_conversion
from utils.reversals import is_reversal

def find_best_box_spread(data, s_0):
    """
    finds the optimal box spread to buy in O(N) where N is the number of strikes,
    on the condition that the box spread is composed of both a valid (theoretically profitable) conversion and reversal

    input: data: dictionary {
        key 'CALL_BID': list of bid offers on calls in the chain
        key 'CALL_ASK': list of ask offers
        key 'PUT_BID': ...
        key 'PUT_ASK: ...
        key 'STRIKE': list of strike prices with liquid options
    }
    s_0: current (market) price of the underlying

    returns: dictionary {
        key 'theo': theoretical value of the box spread at expiration
        key 'cost': cost of the box spread
        key 'net': net profit of purchasing the box spread at the current quotes
    }
    """
    C_BID = data['CALL_BID'] 
    C_ASK = data['CALL_ASK']
    P_BID = data['PUT_BID']
    P_ASK = data['PUT_ASK']
    STRIKE = data['STRIKE']

    best_reversal = dict()
    best_box = dict()

    ## assert all lists are the same length
    assert ((len(C_BID) == len(C_ASK)) & (len(C_BID) == len(P_BID)) & (len(C_BID) == len(P_ASK)) & (len(C_BID) == len(STRIKE)))

    for index in range(len(C_BID)):
        ## find a reversal if we haven't found one yet
        if not best_reversal:
            call_price = C_ASK[index]
            put_price = P_BID[index]
            strike = STRIKE[index]
            if is_reversal(call_price, put_price, s_0, strike):
                minimize = call_price - put_price - s_0 + strike
                cost = call_price - put_price 
                best_reversal = {
                    'cost': cost,
                    'strike': strike,
                    'minimize': minimize
                }
        ## if a reversal exists then search for a conversion
        else:
            call_bid = C_BID[index]
            put_ask = P_ASK[index]
            call_ask = C_ASK[index]
            put_bid = P_BID[index]
            strike = STRIKE[index]

            if is_conversion(call_bid, put_ask, s_0, strike):
                if not best_box:
                    credit = put_ask - call_bid
                    wide = strike - best_reversal['strike']
                    box_spread_cost = best_reversal['cost'] + credit
                    net = wide - box_spread_cost
                    best_box = {
                        'theo': wide,
                        'cost': box_spread_cost,
                        'net' : net
                    }
                else:
                    credit = put_ask - call_bid
                    wide = strike - best_reversal['strike']
                    box_spread_cost = best_reversal['cost'] + credit
                    net = wide - box_spread_cost
                    if net > best_box['net']:
                        best_box = {
                            'theo': wide,
                            'cost': box_spread_cost,
                            'net' : net
                        }
            
            if is_reversal(call_ask, put_bid, s_0, strike):
                minimize = call_ask - put_bid - s_0 + strike
                if minimize < best_reversal['minimize']:
                    cost = call_ask - put_bid 
                    best_reversal = {
                        'cost': cost,
                        'strike': strike,
                        'minimize': minimize
                    }
                    
    return best_box