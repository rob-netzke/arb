def is_conversion(C, P, S, K):
    """given a call, put, current price, and strike, this function returns if a conversion opportunity exists

       input: C: call price, when considering a conversion this may be considered the bid price, aka the market taker price to sell a call
              P: put price, the ask price, or market taker price to buy a put
              S: current price of the underlying
              K: the strike price of both options
        returns: bool -> True if an arbitrage opportunity exists, False otherwise
    """
    return C - P - S + K > 0

def find_first_conversion(data, price):
    """starting at the lowest strike in the chain, naively search for a conversion and return the order details when one is found

        input: data: dictionary {
            key 'CALL_BID': list of bid offers on calls in the chain
            key 'CALL_ASK': list of ask offers
            key 'PUT_BID': ...
            key 'PUT_ASK: ...
            key 'STRIKE': list of strike prices with liquid options
        }
        s_0: current (market) price of the underlying
        returns: dict: {
            key 'sell call @: ': suggested value to sell the call for,
            key 'buy put @: ': suggested value to buy the put for,
            'strike: ': strike price of both options,
            'edge': the theorectial edge gained by the trade, no considering fees or slippage
        } 
                OR None if no conversion is found
    """
    C_BID = data['CALL_BID'] 
    P_ASK = data['PUT_ASK']
    STRIKE = data['STRIKE']
    ## finds the first conversion in the chain
    #O(N) in the worst case
    for index in range(len(C_BID)):
        call_price = C_BID[index]
        put_price = P_ASK[index]
        strike = STRIKE[index]
        if is_conversion(call_price, put_price, price, strike):
            delta = call_price - put_price - price + strike
            return  {
                'sell call @: ': call_price,
                'buy put @: ': put_price,
                'strike: ': strike,
                'edge': round(delta,2)
            }
    return None

def find_best_conversion(data, price):
    """starting at the lowest strike in the chain, iteratively search for a conversion. 
        if one is found, check if it is better than the existing best conversion

        input: data: dictionary {
            key 'CALL_BID': list of bid offers on calls in the chain
            key 'CALL_ASK': list of ask offers
            key 'PUT_BID': ...
            key 'PUT_ASK: ...
            key 'STRIKE': list of strike prices with liquid options
        }
        s_0: current (market) price of the underlying
        returns: dict: {
            key 'sell call @: ': suggested value to sell the call for,
            key 'buy put @: ': suggested value to buy the put for,
            'strike: ': strike price of both options,
            'edge': the theorectial edge gained by the trade, no considering fees or slippage
        } 
                OR None if no conversion is found
    """
    C_BID = data['CALL_BID'] 
    P_ASK = data['PUT_ASK']
    STRIKE = data['STRIKE']

    best_conversion = 0 ## if the market is neutral then C(K) - P(K) - S_0 + K = 0
    order = dict()

    #O(N) runtime 
    for index in range(len(C_BID)):
        call_price = C_BID[index]
        put_price = P_ASK[index]
        strike = STRIKE[index]
        if is_conversion(call_price, put_price, price, strike):
            delta = call_price - put_price - price + strike
            if delta > best_conversion:
                best_conversion = delta
                order = {
                    'sell call @: ': call_price,
                    'buy put @: ': put_price,
                    'strike: ':strike,
                    'edge: ': round(delta,2)
                }        
    return order
