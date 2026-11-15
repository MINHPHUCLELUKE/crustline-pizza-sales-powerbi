# Metric definitions

| Term | Definition |
|---|---|
| Order | One distinct `order_id`. Orders are numbered 1 to 21,350 by date and time in `Dim_Order` |
| Order line | One row of the source file: one pizza at one size on one order, with a quantity |
| Pizza (unit) | One pizza sold. Quantity is summed across order lines |
| Revenue | Quantity times the price of that pizza and size, summed line by line. It is a list price figure, with no discounts, taxes or costs |
| Average order value | Total revenue divided by total orders |
| Average pizzas per order | Total quantity sold divided by total orders |
| Trading day | A day with at least one order. 358 of the 365 days of 2015 are trading days |
| Daily average and standard deviation | Mean and population standard deviation of daily revenue across trading days ($2,284.53 and $405.38) |
| Anomaly | A day whose revenue is 2 or more standard deviations above (spike) or below (drop) the daily average. 16 days |
| Z score | Daily revenue minus the daily average, divided by the standard deviation |
| Average price | Quantity weighted price per pizza sold: revenue divided by pizzas sold, for the pizzas in the current filter |
| Single item order | An order with one distinct pizza (one `pizza_id`, so one pizza at one size), whatever the quantity. 8,201 orders |
| Multi item order | An order with two or more distinct pizzas. 13,149 orders |
| Pizzas per order (bands) | Total pizzas on the order, shown as 1, 2, 3 and 4 or more. This counts quantity, so the 1 band has 8,111 orders and differs from the single item count |
| Turnaround, gap | Minutes between an order and the previous order on the same day. The first order of each day has no gap. 20,992 orders have a gap |
| Hour | Hour of the order time, 0 to 23. Orders occur from 09:00 to 23:00 |
| Peak hour, peak day | The hour and the weekday with the most orders in the current filter |
| Avg orders per day | Orders divided by the number of days with at least one order |
| Ingredient volume | Pizzas sold that contain the ingredient. A pizza counts once under each ingredient it contains, so ingredient volumes do not add up to total pizzas |
| Correlation | Pearson correlation between average price and pizzas sold across the four categories (-0.95) |
