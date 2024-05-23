import math
from scipy.stats import norm

def d1(up, sp, t, r, v, d):
    return (math.log(up / sp) + (r - d + 0.5 * v ** 2) * t) / (v * math.sqrt(t))

def nd1(up, sp, t, r, v, d):
    return math.exp(-(d1(up, sp, t, r, v, d) ** 2) / 2) / (math.sqrt(2 * math.pi))

def call_price(up, sp, t, r, v, d):
    return math.exp(-d * t) * up * norm.cdf(d1(up, sp, t, r, v, d)) - sp * math.exp(-r * t) * norm.cdf(d1(up, sp, t, r, v, d) - v * math.sqrt(t))

def put_price(up, sp, t, r, v, d):
    return sp * math.exp(-r * t) * norm.cdf(-d1(up, sp, t, r, v, d) + v * math.sqrt(t)) - up * math.exp(-d * t) * norm.cdf(-d1(up, sp, t, r, v, d))

def option_vega(up, sp, t, r, v, d):
    return 0.01 * up * math.sqrt(t) * nd1(up, sp, t, r, v, d)

def option_vomma(up, sp, t, r, v, d):
    d1_val = d1(up, sp, t, r, v, d)
    nd1_val = nd1(up, sp, t, r, v, d)
    return 0.01 * up * math.sqrt(t) * d1_val * nd1_val

def calculate_iv(option_price, S, K, T, r, q, option_type):
    if option_type == 'call':
        option_func = lambda sigma: black_scholes_call(S, K, T, r, q, sigma) - option_price
    elif option_type == 'put':
        option_func = lambda sigma: black_scholes_put(S, K, T, r, q, sigma) - option_price
    else:
        raise ValueError("Invalid option type")
    
    return brentq(option_func, 0.01, 2.0)

def black_scholes_call(S, K, T, r, q, sigma):
    d1 = (math.log(S / K) + (r - q + sigma**2 / 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    return S * math.exp(-q * T) * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)

def black_scholes_put(S, K, T, r, q, sigma):
    d1 = (math.log(S / K) + (r - q + sigma**2 / 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    return K * math.exp(-r * T) * norm.cdf(-d2) - S * math.exp(-q * T) * norm.cdf(-d1)
