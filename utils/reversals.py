def is_reversal(C, P, S, K):
    """given a call, put, current price, and strike, this function returns if a reversal opportunity exists
    
       input: C: call price, when considering a reversal this may be considered the ask price, aka the market taker price to buy a call
              P: put price, the bid price, or market taker price to sell a put
              S: current price of the underlying
              K: the strike price of both options
        returns: bool -> True if an arbitrage opportunity exists, False otherwise
    """
    return C - P - S + K < 0

def find_first_reversal(data, price):
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
            key 'buy call @: ': suggested value to buy the call for,
            key 'sell put @: ': suggested value to sell the put for,
            'strike: ': strike price of both options,
            'edge': the theorectial edge gained by the trade, not considering fees, slippage, interest
        } 
                OR None if no conversion is found
    """
    C_ASK = data['CALL_ASK']
    P_BID = data['PUT_BID']
    STRIKE = data['STRIKE']
    
    #O(N) in the worst case
    for index in range(len(C_ASK)):
        call_price = C_ASK[index]
        put_price = P_BID[index]
        strike = STRIKE[index]
        delta = call_price - put_price - price + strike
        if is_reversal(call_price, put_price, price, strike):
            return  {
                'buy call @: ': call_price,
                'sell put @: ': put_price,
                'strike: ': strike,
                'edge': round(-delta, 2)
            }
    return None

def find_best_reversal(data, price):
    """starting at the lowest strike in the chain, iteratively search for a reversal. 
        if one is found, check if it is better than the existing best reversal

        input: data: dictionary {
            key 'CALL_BID': list of bid offers on calls in the chain
            key 'CALL_ASK': list of ask offers
            key 'PUT_BID': ...
            key 'PUT_ASK: ...
            key 'STRIKE': list of strike prices with liquid options
        }
        s_0: current (market) price of the underlying
        returns: dict: {
            key 'buy call @: ': suggested value to buy the call for,
            key 'sell put @: ': suggested value to sell the put for,
            'strike: ': strike price of both options,
            'edge': the theorectial edge gained by the trade, not considering fees, slippage, or interest
        } 
                OR None if no reversal is found
    """
    C_BID = data['CALL_BID'] 
    C_ASK = data['CALL_ASK']
    P_BID = data['PUT_BID']
    P_ASK = data['PUT_ASK']
    STRIKE = data['STRIKE']

    best_reversal = 0 ## if the market is neutral then C(K) - P(K) - S_0 + K = 0
    order = dict()

    #O(N) runtime 
    for index in range(len(C_ASK)):
        call_price = C_ASK[index]
        put_price = P_BID[index]
        strike = STRIKE[index]
        if is_reversal(call_price, put_price, price, strike):
            delta = call_price - put_price - price + strike
            if delta < best_reversal:
                best_reversal = delta
                order = {
                    'buy call @: ': call_price,
                    'sell put @: ': put_price,
                    'strike: ': strike,
                    'edge': round(-delta, 2)
                }        
    return order