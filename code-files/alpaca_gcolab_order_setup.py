# type: ignore
import time

num_orders = 10
interval_seconds = 15
order_size = 25
order_side = OrderSide.SELL
order_type = OrderType.MARKET

req = MarketOrderRequest(
    symbol=symbol,
    qty=order_size,
    side=order_side,
    type=order_type,
    time_in_force=TimeInForce.DAY,
)
