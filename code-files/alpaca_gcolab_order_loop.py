# type: ignore
# loop

for i in range(1, num_orders + 1):
    try:
        order = trade_client.submit_order(req)
		
		print(f"Order {i}/{num_orders}: {order_side.value.upper()} {order_size} {symbol} | status: {order.status}")

    except Exception as e:
        print(f"Order {i}/{num_orders} failed: {e}")

    if i < num_orders:
        time.sleep(interval_seconds)

print("Done.")