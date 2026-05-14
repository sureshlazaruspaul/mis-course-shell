import alpaca_trade_api as tradeapi # type: ignore
import random
import time
from datetime import datetime
import asyncio

# Configuration
API_KEY = 'PKXO3JBOTMPMPD73JACJZVKGNR'
API_SECRET = '6P7pzsA4kpj7iBH35Gb1XnfHGo7z98xwmmLzpK11mnrL'
BASE_URL = 'https://paper-api.alpaca.markets'

STOCK_UNIVERSE = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'JPM']
ORDER_DELAY = 0.5
MAX_ORDERS = 100
SHARES_RANGE = (1, 10)

# PDT and Balance Requirements
MINIMUM_BALANCE = 25000
BALANCE_BUFFER = 5000
REQUIRED_BALANCE = MINIMUM_BALANCE + BALANCE_BUFFER

# Initialize API
api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')

# Global counters
buy_count = 0
sell_count = 0
demo_stopped = False


def verify_pdt_and_balance():
    """Verify PDT flag is enabled and balance meets requirements"""
    try:
        account = api.get_account()
        
        pdt_enabled = account.pattern_day_trader
        portfolio_value = float(account.portfolio_value)
        buying_power = float(account.buying_power)
        
        print("="*80)
        print("ACCOUNT VERIFICATION")
        print("="*80)
        print(f"Pattern Day Trader Status: {pdt_enabled}")
        print(f"Portfolio Value: ${portfolio_value:,.2f}")
        print(f"Buying Power: ${buying_power:,.2f}")
        print(f"Required Balance: ${REQUIRED_BALANCE:,.2f} (${MINIMUM_BALANCE:,.2f} + ${BALANCE_BUFFER:,.2f} buffer)")
        print("="*80)
        
        # Check PDT status
        if not pdt_enabled:
            print("\n❌ ERROR: Pattern Day Trader flag is NOT enabled!")
            print("   You need PDT status to run this HFT demo.")
            print("   Contact Alpaca support to enable PDT for your paper trading account.")
            return False
        else:
            print("\n✅ Pattern Day Trader flag is enabled")
        
        # Check balance
        if portfolio_value < REQUIRED_BALANCE:
            print(f"\n❌ ERROR: Insufficient balance!")
            print(f"   Current: ${portfolio_value:,.2f}")
            print(f"   Required: ${REQUIRED_BALANCE:,.2f}")
            print(f"   Shortfall: ${REQUIRED_BALANCE - portfolio_value:,.2f}")
            print("\n   Paper trading accounts should have sufficient balance by default.")
            print("   Contact Alpaca support if you need to increase your paper trading balance.")
            return False
        else:
            print(f"✅ Balance requirement met (${portfolio_value:,.2f} >= ${REQUIRED_BALANCE:,.2f})")
        
        print("\n" + "="*80)
        print("✅ ALL CHECKS PASSED - Ready to trade!")
        print("="*80 + "\n")
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR verifying account: {e}")
        return False


def check_balance_during_trading():
    """Check if balance is still above minimum during trading"""
    global demo_stopped
    
    try:
        account = api.get_account()
        portfolio_value = float(account.portfolio_value)
        
        if portfolio_value < REQUIRED_BALANCE:
            print("\n" + "="*80)
            print("⚠️  WARNING: Balance dropped below required minimum!")
            print(f"   Current: ${portfolio_value:,.2f}")
            print(f"   Required: ${REQUIRED_BALANCE:,.2f}")
            print("   STOPPING DEMO FOR SAFETY")
            print("="*80)
            demo_stopped = True
            return False
        
        return True
    except Exception as e:
        return True


def get_current_price(symbol):
    try:
        trade = api.get_latest_trade(symbol)
        return trade.price
    except:
        return None


def get_account_info():
    try:
        account = api.get_account()
        return {
            'buying_power': float(account.buying_power),
            'cash': float(account.cash),
            'portfolio_value': float(account.portfolio_value),
            'daytrade_count': account.daytrade_count,
            'status': account.status,
            'pattern_day_trader': account.pattern_day_trader
        }
    except:
        return None


def place_random_order():
    global buy_count, sell_count
    
    if not check_balance_during_trading():
        return None
    
    symbol = random.choice(STOCK_UNIVERSE)
    side = random.choice(['buy', 'sell'])
    qty = random.randint(*SHARES_RANGE)
    
    try:
        order = api.submit_order(
            symbol=symbol, qty=qty, side=side,
            type='market', time_in_force='day'
        )
        if side == 'buy':
            buy_count += 1
        else:
            sell_count += 1
        return order
    except:
        return None


def display_terminal_summary():
    account_info = get_account_info()
    timestamp = datetime.now().strftime('%H:%M:%S')
    
    if account_info:
        balance_status = "OK" if account_info['portfolio_value'] >= REQUIRED_BALANCE else "LOW"
        pdt_status = "ENABLED" if account_info['pattern_day_trader'] else "DISABLED"
        
        print(f"\n[{timestamp}] "
              f"BUYS: {buy_count} | SELLS: {sell_count} | "
              f"Balance: ${account_info['portfolio_value']:,.2f} ({balance_status}) | "
              f"PDT: {pdt_status}")
    else:
        print(f"\n[{timestamp}] BUYS: {buy_count} | SELLS: {sell_count} | Balance: ERROR")


def cancel_all_orders():
    try:
        api.cancel_all_orders()
        return True
    except:
        return False


def close_all_positions():
    try:
        positions = api.list_positions()
        if not positions:
            return True
        for position in positions:
            api.close_position(position.symbol)
        return True
    except:
        return False


async def terminal_summary_loop():
    while not demo_stopped:
        await asyncio.sleep(60)
        if not demo_stopped:
            display_terminal_summary()


async def trading_loop(max_orders, delay):
    global demo_stopped
    
    for i in range(max_orders):
        if demo_stopped:
            print("\n⚠️  Demo stopped due to balance check failure")
            break
            
        place_random_order()
        await asyncio.sleep(delay)


async def run_demo(max_orders=MAX_ORDERS, delay=ORDER_DELAY):
    global buy_count, sell_count, demo_stopped
    
    buy_count = 0
    sell_count = 0
    demo_stopped = False
    
    # Verify PDT and balance before starting
    if not verify_pdt_and_balance():
        print("\n❌ Pre-flight checks failed. Cannot start demo.")
        return
    
    print("\n" + "="*80)
    print("HFT DEMONSTRATION STARTED")
    print("="*80)
    print(f"Max Orders: {max_orders}")
    print(f"Order Delay: {delay} seconds")
    print(f"Required Balance: ${REQUIRED_BALANCE:,.2f}")
    print("Terminal updates: Every 1 minute")
    print("="*80)
    
    display_terminal_summary()
    
    try:
        await asyncio.gather(
            trading_loop(max_orders, delay),
            terminal_summary_loop()
        )
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user")
    
    print("\n" + "="*80)
    print("DEMO COMPLETED")
    print("="*80)
    display_terminal_summary()
    
    # Final balance check
    account_info = get_account_info()
    if account_info:
        final_balance = account_info['portfolio_value']
        if final_balance < REQUIRED_BALANCE:
            print(f"\n⚠️  WARNING: Final balance (${final_balance:,.2f}) below required minimum!")
        else:
            print(f"\n✅ Final balance check passed: ${final_balance:,.2f}")
    
    cleanup = input("\nCleanup? (cancel orders & close positions) [y/n]: ").lower()
    if cleanup == 'y':
        cancel_all_orders()
        close_all_positions()
        print("\n✓ Cleanup complete")


if __name__ == "__main__":
    asyncio.run(run_demo(max_orders=MAX_ORDERS, delay=ORDER_DELAY))