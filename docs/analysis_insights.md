# Findings and recommendations

All figures are for 1 January to 31 December 2015 and come from the Power BI model. Revenue is quantity times list price. The data has no costs, customer ids or locations, so everything here is about sales, timing and mix.

## 1. Overview: a steady year

- **Totals:** $817,860 revenue, 49,574 pizzas, 21,350 orders. Average order value is $38.31 and the average order holds 2.32 pizzas.
- **Monthly revenue** stays in a narrow band: $64.0K (October) to $72.6K (July). There is no growth trend and no strong seasonality. The three weakest months in total are September ($64.2K), October ($64.0K) and December ($64.7K), but September and October have empty days. Per trading day the months run from $2,157 (December) to $2,370 (October), within about 10% of each other, and December is the weakest.
- **Category mix of revenue:** Classic $220.1K (26.9%), Supreme $208.2K (25.5%), Chicken $195.9K (24.0%), Veggie $193.7K (23.7%). The four categories are within about three points of each other.
- **Best sellers by revenue:** Thai Chicken ($43.4K), Barbecue Chicken ($42.8K), California Chicken ($41.4K), Classic Deluxe ($38.2K) and Spicy Italian ($34.8K). Chicken pizzas take three of the top five revenue places.

## 2. Trends and anomalies: 16 unusual days

A day is flagged when its revenue is 2 or more standard deviations from the daily average. The average is $2,284.53 and the standard deviation $405.38, over the 358 days that had orders, so the thresholds are $3,095.28 (spike) and $1,473.77 (drop).

| Day | Revenue | Orders | Avg order value | Z score | Flag | Best seller that day |
|---|---|---|---|---|---|---|
| Sun 1 Feb | $3,189.20 | 87 | $36.66 | 2.23 | Spike | California Chicken |
| Sun 22 Mar | $1,259.25 | 37 | $34.03 | -2.53 | Drop | Pepperoni |
| Fri 15 May | $3,386.15 | 94 | $36.02 | 2.72 | Spike | Pepperoni |
| Fri 3 Jul | $3,443.00 | 93 | $37.02 | 2.86 | Spike | Pepperoni |
| Sat 4 Jul | $3,864.20 | 105 | $36.80 | 3.90 | Spike | Classic Deluxe |
| Fri 17 Jul | $3,131.65 | 82 | $38.19 | 2.09 | Spike | Southwest Chicken, California Chicken |
| Fri 24 Jul | $3,204.40 | 75 | $42.73 | 2.27 | Spike | Pepperoni |
| Thu 1 Oct | $3,202.15 | 84 | $38.12 | 2.26 | Spike | Sicilian |
| Thu 15 Oct | $4,320.20 | 107 | $40.38 | 5.02 | Spike | Hawaiian |
| Fri 6 Nov | $3,157.50 | 73 | $43.25 | 2.15 | Spike | Mexicana, Hawaiian |
| Sun 22 Nov | $1,368.70 | 43 | $31.83 | -2.26 | Drop | Sicilian |
| Thu 26 Nov | $4,405.95 | 113 | $38.99 | 5.23 | Spike | Hawaiian |
| Fri 27 Nov | $4,422.45 | 115 | $38.46 | 5.27 | Spike | Classic Deluxe |
| Sun 27 Dec | $1,419.00 | 35 | $40.54 | -2.14 | Drop | Vegetables + Vegetables |
| Tue 29 Dec | $1,353.25 | 27 | $50.12 | -2.30 | Drop | California Chicken, Big Meat |
| Wed 30 Dec | $1,337.80 | 32 | $41.81 | -2.34 | Drop | Southwest Chicken, California Chicken |

- **11 spikes and 5 drops.** The three biggest spikes (15 Oct, 26 Nov, 27 Nov) are above 5 standard deviations and sit at 107 to 115 orders against about 60 on a typical day.
- **Spikes on consecutive days.** 3 July (z = 2.86) falls the day before 4 July, so the report's Trends caption groups them as 3 to 4 July; 4 July is the larger of the two.
- **The biggest spikes came from more orders, not bigger baskets.** On 15 Oct, 26 Nov, 27 Nov and 4 Jul the average order value was $36.80 to $40.38, close to the yearly $38.31.
- **Drops cluster at the end of the year.** Three of the five drops fall between 27 and 30 December, with 25 December having no orders at all. The other drops are Sun 22 Mar and Sun 22 Nov.
- **Treat the count with care.** If daily revenue were normally distributed, about 4.6% of days (roughly 16 of 358) would fall outside 2 standard deviations by chance, so 16 flagged days is about what chance alone gives. The rule also ignores the weekday pattern: 6 of the 11 spikes are Fridays and 3 of the 5 drops are Sundays, the busiest and quietest days. Only the three days above 5 standard deviations clearly stand out.
- **Causes are not in the data.** Some dates line up with public holidays in the United States (4 July, 26 November), but the data does not say where the business operates, so treat that as a hypothesis to check against a holiday and event calendar.
- **Partial weeks:** the first and last week of 2015 are partial and are marked on the weekly chart.

## 3. Day and hour: two daily peaks, Friday leads

- **Hours:** orders peak in the 12:00 hour (2,520) and the 13:00 hour (2,455), then again in the 17:00 hour (2,336) and 18:00 hour (2,399). The 12:00 and 13:00 hours together hold 23.3% of orders and the 17:00, 18:00 and 19:00 hours 31.6%. Almost nothing happens before 11:00 (9 orders in total) or after 22:00 (28 orders at 23:00).
- **Days:** Friday is busiest with 3,538 orders ($136.1K revenue), averaging 70.8 orders per trading day. Sunday is quietest with 2,624 orders ($99.2K), averaging 50.5. Friday brings in about 37% more revenue than Sunday over the year.
- **Time between orders** averages 11.0 minutes. It is shortest at 11:00 to 13:00 (7.6 to 8.6 minutes), and grows after 21:00 (16.0 minutes at 21:00, 20.8 at 22:00, 25.5 at 23:00, which rests on only 28 orders). The gap is measured from the previous order the same day, so it reflects demand, not kitchen speed.

## 4. Products and sizes: Classic by volume, Large by revenue

- **By quantity:** Classic leads with 14,888 pizzas (30.0%), then Supreme 11,987 (24.2%), Veggie 11,649 (23.5%) and Chicken 11,050 (22.3%).
- **Classic is the cheapest category.** Its quantity weighted average price is $14.78, against $17.73 (Chicken), $17.37 (Supreme) and $16.63 (Veggie). It sells the most pizzas but ranks first on revenue only by a small margin.
- **Top 5 by quantity:** Classic Deluxe 2,453, Barbecue Chicken 2,432, Hawaiian 2,422, Pepperoni 2,418, Thai Chicken 2,371. The top five are within 4% of each other, so no single pizza dominates.
- **Bottom 5 by quantity:** Brie Carre 490, Mediterranean 934, Calabrese 937, Spinach Supreme 950, Soppressata 961. Brie Carre sells about one fifth as many as the best seller and earns the least revenue ($11.6K).
- **Sizes:** Large is 38.2% of pizzas and 45.9% of revenue. Medium is 31.5% of pizzas and 30.5% of revenue. Small is 29.1% of pizzas but only 21.8% of revenue. X Large (552) and XX Large (28) together are about 1% of pizzas.

## 5. Ingredients and price

- **Top ingredients by pizzas sold:** Garlic 27,913, Tomatoes 27,052, Red Onions 19,834, Red Peppers 16,562, Mozzarella Cheese 10,569, Pepperoni 10,540, Spinach 10,166, Mushrooms 9,729, Chicken 8,618, Capocollo 6,692. Ingredient totals add up to more than total pizzas, because a pizza counts under every ingredient it contains.
- **Mozzarella as recorded:** it appears only on Classic (4,840), Supreme (2,418) and Veggie (3,311) pizzas, not on Chicken pizzas, and tomato sauce is not recorded as an ingredient. Nothing was added to the data.
- **Slowest ingredients:** Soppressata Salami 961; Friggitello Peppers, Pancetta and 'Nduja Salami 937 each; Plum Tomatoes 934; and Pears, Prosciutto, Thyme, Caramelized Onions and Brie Carre Cheese at 490 each. These volumes equal the sales of the slowest pizzas that use them (Soppressata, Calabrese, Mediterranean, Brie Carre), so each of these ingredients is carried for one slow pizza.
- **Price against volume:** across the four categories, quantity weighted average price and pizzas sold have a correlation of -0.95, so the cheapest category sells the most. With four points this is a hint. Classic alone drives it: without Classic the other three categories give -0.47. Across individual pizza names the correlation is much weaker (-0.30), and that is the more cautious reading.

## 6. Orders: most orders hold several pizzas

- **Single and multi:** 8,201 orders (38.4%) contain one distinct pizza and size (one order line) and 13,149 (61.6%) contain two or more.
- **Pizzas per order:** 1 pizza 8,111 orders (38.0%), 2 pizzas 6,152 (28.8%), 3 pizzas 3,207 (15.0%), 4 or more 3,880 (18.2%).
- **Order value grows with basket size:** $16.52 for one pizza, $32.99 for two, $49.38 for three and $83.14 for four or more.
- **Time since the previous order** (first order of each day excluded, 20,992 orders): under 5 minutes 7,948 (37.9%), 5 to 10 minutes 4,900 (23.3%), 10 to 15 minutes 2,954 (14.1%), 15 to 30 minutes 3,721 (17.7%), 30 minutes or more 1,469 (7.0%).

## Recommendations

1. **Staff and prep for the two peaks.** Concentrate labour and dough and topping prep in the 12:00 to 13:59 and 17:00 to 19:59 windows, which hold 55% of orders, and add capacity on Fridays.
2. **Check the spike days before planning around them.** The biggest spikes (4 July, 15 October, 26 and 27 November) came from order volume. With one year of data it is unknown whether they recur. Thanksgiving moves each year and 15 October has no known cause, so compare them with an event calendar first.
3. **Test ways to lift small baskets.** Nearly four in ten orders hold a single pizza and size, and order value rises by about $16 for each extra pizza. The data cannot show that an offer would add pizzas, so test bundles, side items and a second pizza offer.
4. **Test featuring Large first.** It earns 45.9% of revenue from 38.2% of pizzas. This is revenue only, and without costs it is unknown whether Large earns more margin.
5. **Review the bottom of the menu.** Brie Carre sells 490 pizzas and is the only pizza that uses five of its ingredients. Check its sizes and the wastage on those ingredients before deciding to remove it or relaunch it with a promotion.
6. **Test price before changing it.** Classic is the cheapest and most popular category. A small price test on Classic would show whether volume holds, which the four-point correlation cannot.
7. **Fill the soft spots.** Sundays are the quietest day and December is the weakest month per trading day (about $2,157 against $2,285 for the year). Target promotions there rather than at peak days.

## Limits of this analysis

One year of data means no year-on-year comparison and no way to separate seasonality from noise. There is no cost data, so no profit view. The correlation is on four points. Anomaly causes are hypotheses, not findings.
