# QA checklist

Report figures were checked against independent calculations: sums of parts, separate DAX queries over the base tables, and a calculation outside Power BI that reads the source CSV directly (check 23). The file itself is the only source, so the checks show the model matches the file and is internally consistent, not that the file matches an outside system.

| # | Check | Expected | Model result | Method | Status |
|---|---|---|---|---|---|
| 1 | Revenue by category adds up to total revenue | $817,860.05 | $220,053.10 + $208,197.00 + $195,919.50 + $193,690.45 = $817,860.05 | Sum of four category values | Pass |
| 2 | Revenue by size adds up to total revenue | $817,860.05 | $178,076.50 + $249,382.25 + $375,318.70 + $14,076.00 + $1,006.60 = $817,860.05 | Sum of five size values | Pass |
| 3 | Revenue by weekday adds up to total revenue | $817,860.05 | $107,329.55 + $114,133.80 + $114,408.40 + $123,528.50 + $136,073.90 + $123,182.40 + $99,203.50 = $817,860.05 | Sum of seven weekday values | Pass |
| 4 | Pizzas by category add up to total quantity | 49,574 | 14,888 + 11,987 + 11,050 + 11,649 = 49,574 | Sum of four category values | Pass |
| 5 | Pizzas by size add up to total quantity | 49,574 | 14,403 + 15,635 + 18,956 + 552 + 28 = 49,574 | Sum of five size values | Pass |
| 6 | Orders by weekday add up to total orders | 21,350 | 2,794 + 2,973 + 3,024 + 3,239 + 3,538 + 3,158 + 2,624 = 21,350 | Sum of seven weekday values | Pass |
| 7 | Orders by hour add up to total orders | 21,350 | Hours 9 to 23 sum to 21,350 | Sum of fifteen hourly values | Pass |
| 8 | Single plus multi item orders equal total orders | 21,350 | 8,201 + 13,149 = 21,350 | Sum of two values | Pass |
| 9 | Orders by pizzas per order add up to total orders | 21,350 | 8,111 + 6,152 + 3,207 + 3,880 = 21,350 | Sum of four bands | Pass |
| 10 | Single item orders match an independent definition | 8,201 | 8,201 orders with one distinct pizza and 8,201 orders with exactly one order line | Separate DAX query over the order and fact tables | Pass |
| 11 | Orders with a gap equal orders minus first orders of each day | 21,350 - 358 = 20,992 | 7,948 + 4,900 + 2,954 + 3,721 + 1,469 = 20,992 | Sum of five gap bands | Pass |
| 12 | Trading days equal 365 minus days without orders | 358 | 365 - 7 listed empty days = 358 | Date table against order dates | Pass |
| 13 | Daily average revenue | $817,860.05 / 358 = $2,284.53 | $2,284.53 | Division outside the model | Pass |
| 14 | Anomaly thresholds and count | $2,284.53 +/- 2 x $405.38 = $1,473.77 to $3,095.28 | 16 days outside the band (11 above, 5 below) | Separate DAX query listing days by z score | Pass |
| 15 | Average order value | $817,860.05 / 21,350 = $38.31 | $38.31 | Division outside the model | Pass |
| 16 | Average pizzas per order | 49,574 / 21,350 = 2.32 | 2.32 | Division outside the model | Pass |
| 17 | Weighted average price by category | Revenue / pizzas: Classic $14.78, Chicken $17.73, Supreme $17.37, Veggie $16.63 | Same four values | Division outside the model | Pass |
| 18 | Price vs quantity correlation by category | -0.9496 | -0.9496 | Pearson formula recomputed outside Power BI from the four category totals | Pass |
| 19 | Mozzarella volume splits by category | 10,569 | 4,840 (Classic) + 2,418 (Supreme) + 3,311 (Veggie) + none for Chicken = 10,569 | Matrix against ingredient total | Pass |
| 20 | Share figures | Size shares of pizzas 29.1%, 31.5%, 38.2%, 1.1%, 0.1%; of revenue 21.8%, 30.5%, 45.9%, 1.7%, 0.1% | Same values | Division outside the model | Pass |
| 21 | Friday and Sunday average orders per day | 3,538 / 50 Fridays = 70.8; 2,624 / 52 Sundays = 50.5 | 70.76 and 50.46 | Orders divided by trading days of that weekday | Pass |
| 22 | Cleaned ingredient name | One value `'Nduja Salami`, 937 pizzas | One value, 937 pizzas | Ingredient table and matrix | Pass |
| 23 | Headline figures against the raw CSV | 48,620 rows, 21,350 orders, 49,574 pizzas, $817,860.05 revenue, 91 pizza ids, 358 trading days, daily average $2,284.53, SD $405.38, 16 anomaly days (11 spikes, 5 drops), 8,201 single and 13,149 multi orders, 8,111 / 6,152 / 3,207 / 3,880 by pizzas per order, category and size totals as in checks 1, 2, 4 and 5 | Same values | [`qa/check_totals.py`](../qa/check_totals.py), reading the CSV directly with no Power Query steps (38 checks) | Pass |

## Issues found by these checks, and what changed

1. **Average price** was a simple average of the price list. Check 17 showed it did not match revenue divided by pizzas sold, so the measure was changed to the weighted version.
2. **Single item orders** counted total pizzas, so two of the same pizza counted as multi. Check 10 showed the difference (8,111 against 8,201), so the order type now counts distinct pizzas.
3. **Mozzarella** was added to every pizza in an earlier version. Check 19 showed 14,888 on Classic against 4,840 recorded, so the added rows were removed.

## Not checked

- Hour, weekday, gap, ingredient and correlation figures were checked inside the model and by formula, not by a second read of the CSV.
- Causes of spike and drop days are hypotheses and cannot be tested with this data.
