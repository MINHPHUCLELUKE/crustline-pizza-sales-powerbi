# Data quality report

The source CSV is imported untouched. Every fix below is made in Power Query, so the raw file stays as delivered and the steps can be repeated on a new export.

## Cleaning applied in Power Query

| Issue or need | What was done | Where |
|---|---|---|
| Columns arrive as text | Types set with the en-US culture: whole numbers, date, time, currency | `data_pizza_clean` |
| Stray spaces and hidden characters in text | `Text.Trim` and `Text.Clean` on ingredients, category, name, pizza id and size | `data_pizza_clean` |
| Size is a code (S, M, L, XL, XXL) | Added `size_name` and `size_order` so labels read well and sort in size order | `data_pizza_clean` |
| Ingredients are one comma separated cell | Split on ", " into one row per pizza and ingredient, then trimmed | `pizza_ingredients` |
| One ingredient name arrives with a garbled first character (the file is not UTF-8 and a stray byte before "Nduja Salami" does not decode) | The name is rebuilt as `'Nduja Salami` from the text that follows the garbled character, so it is one clean value and sorts and filters correctly. 937 pizzas use it | `pizza_ingredients` |
| Long names with filler words | "The " and " Pizza" removed from pizza names | `Dim_Pizza` |
| Repeated pizza rows | Distinct rows give 91 pizza and size combinations | `Dim_Pizza` |

## Findings about the data

| Finding | Effect | How it is handled |
|---|---|---|
| 7 of 365 days have no orders: 24 and 25 September, 25 December, and 5, 12, 19 and 26 October | Daily averages over 365 days would be too low | Daily average, standard deviation and anomaly test use the 358 trading days. The date table keeps all 365 days |
| First and last week of 2015 are partial weeks | The first and last weekly bars look short | A note on the weekly chart says so |
| Almost no orders before 11:00 or after 22:00 (9 orders at 09:00 and 10:00, 28 at 23:00) | Hourly gap averages at those hours rest on very few orders | Charts keep all hours. The text quotes the late-evening gaps with the 23:00 value flagged as small |
| First order of each day has no previous order | There is no gap to measure | The gap is left blank and excluded from averages. 358 orders have no gap, so 20,992 of 21,350 do |
| Ingredient lists are partial | Mozzarella is listed on three of four categories (not Chicken) and tomato sauce is never listed | Ingredients are used exactly as recorded. No base ingredient is added |
| An ingredient counts once for every pizza that contains it | Ingredient volumes add up to more than total pizzas | Documented in the definitions. Ingredient totals are used for ranking only |
| Price is a list price per pizza and size | Revenue ignores discounts, taxes and costs | Documented as a limit. No profit figures are shown |

## Problems found while building, and fixes

- **Garbled ingredient name.** Found while reviewing the ingredient list: one name started with a replacement character. Fixed in Power Query as described above, and checked at 937 pizzas.
- **Average price disagreed with what was sold.** A simple average of the price list gave Classic $16.18, Veggie $16.36, Chicken $16.75 and Supreme $16.79, which ignores how many of each size customers bought. A quantity weighted price (revenue divided by pizzas sold) gives Classic $14.78, Veggie $16.63, Supreme $17.37 and Chicken $17.73, a very different spread, so the price against volume view now uses the weighted price.
- **Single versus multi item orders.** The first rule counted total pizzas, so an order of two of the same pizza counted as multi. It now counts distinct pizzas, giving 8,201 single and 13,149 multi orders.
- **Added base ingredients.** An early version added mozzarella and tomato sauce to every pizza. That overstated both (mozzarella appeared on every pizza, 14,888 on Classic against 4,840 recorded), so it was removed.
