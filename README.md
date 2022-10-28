# arb
option arbitrage algorithms

## motivation
one definition of arbitrage is the simultaneous purchase and sale of the same asset in different markets in order to profit from tiny differences in the asset's listed price. the options market is a unique opportunity for arbitrage as the underlying market and the option market can differ, but are directly related. through one clearing house/exchange, there may exist an opportunity for ways to make small profits at no* risk (real world risks are explored later). traditional arbitrage takes advantage of price discrepancies on multiple clearing houses/exchanges. 

although small profits at no risk are nice, solving the underlying problem can be more fun. the challenge here was to look at the option chain once and determine the best arbitrage opportunity. a naive search could include looking over the entire chain a bunch of times, saving some information about each potential trade, and taking the best one at the end by some sort of array operation. that's very slow and surely the opportunity would be traded away by the time you've determined you can make a profitable trade. as with many problems in computer science, by breaking an arbitrage opportunity into smaller parts, it allows for a one-time look at the option chain. the motivation behind this repo was to figure out a clever way to break the problem down.

all algorithms in this repository run in, at worst, O(N) runtime where N is the number of strikes with liquid options in the option chain. the code has very detailed comments on the inputs and outputs of each function. again, this code was to solve a challenge (and to help get a job, please hire me), but some algorithms can run between O(1) and O(N) runtime, which, depending on the tech-stack, internet connection, broker, brokerage fees, market liquidity, and luck MIGHT make you a couple cents. 

## risks (don't use this code with real money)

execution risk: in practice, this is probably the biggest risk. if you try to execute the strategy by executing each portion in multiple legs, there is a chance that one order is filled and another is not. in this situation there is tremendous directional risk. as far as my knowledge goes, unless you are a special firm, you cannot complete each portion of the strategy in a single order. 

pin risk: in the very stange situation that the underlying asset expires directly at the strike price of held options contracts, there is a risk you are assigned a bunch of shares you don't want or someone will be asking for a bunch of shares you don't have. this outcome is unlikely but the probability is not 0. 

interest rate risk: i did not account for this risk in the algorithm, but there is a capital requirement to execute the strategy, and because the profits are so small, you'd be better off in a bond instead of holding the position to expiration.

early assignment risk: similar to the pin risk, there is a change one leg of the order is executed in an American-style option and the rest of the legs will have to be closed. 

dividend risk: if you are expecting a dividend from holding a stock in your calculation and you don't get one, that's not good.

## methodology

Starting with some definitions:

- C(K): the call price at strike K (this price depends on if you are trying to buy or sell the option)

- P(K): the put price at strike K (this price depends on if you are trying to buy or sell the option)

- S: price of the underlying instrument. simplified to be the mid-price

- K: the strike price of the option

- put-call parity: there is no advantage in the stock or option market, by definition: C(K) - P(K) = S - K

- synthetic: the combination of a call and a put to behave exactly as 100 shares of the underlying. a long synthetic consists of buying a call and shorting a put, this   behaves the same as longing 100 shares of the underlying. conversely, a short syntheic consits of shorting a call and buying a put, this behaves the same as selling   short 100 sahres of the underlying

### reversal

a reversal is a situation where it is advantegous to sell short 100 shares of the underlying and simultaneously purchase a synthetic long. this occurs when C(K) - P(K) < S - K which implies C(K) - P(K) - S + K < 0. if executed and held to execution, the difference between the price of underlying and the price of the synthetic long is the profit of the trade.

### conversion

a conversion is just the opposite of a reversal. it is a situation where it is advantegous to long 100 shares of the underlying and simultaneously purchase a synthetic short. this occurs when C(K) - P(K) > S - K which implies C(K) - P(K) - S + K > 0. the profit is the difference as described in the reversal.

### box spread

a box spread is may be defined as the combination of a reversal and a converion. if there is a profitable reversion at a strike lower than a profitable conversion, a trader may execute the reversal and conversion simulatenously. in total, the trader profits the difference of the distance between the two strikes and the value the box spread is purchased for. a trader could also sell boxes, but the box spread algorithm only considers buying them. 

## description of algorithms

conversion and reversal algorithms simply iterate over the option chain and return the first opportunity of arbitrage or iteratively improve the proposed arbitrage opportunity until the end of the chain. 

the box spread algorithm iterates over the chain until a reversal is found. if one is found, then the algorithm searches for a conversion. as the search continues, and if no conversion is found, the best reversal available is updated. if a box spread is found, then the search essentially resets to find a better box. once the end of the chain is reached, the cheapest box spread, that offers the highest net profit, is returned. capital requirements are not considered.

## potential improvements

- the algorithm could potentially search for opportunities to buy OR sell boxes

- technically, a box can exist even if it does not contain a reversal and conversation, but it is probably better to simply execute the reversal or conversion in this   case

- robustness in accepted inputs could be improved
