# Data dictionary

## Source file (raw CSV, 10 columns, one row per order line)

| Column | Type after cleaning | Meaning |
|---|---|---|
| order_id | Whole number | Order identifier. Repeats across the lines of one order |
| date | Date | Order date |
| time | Time | Order time |
| pizza_id | Text | Pizza and size code, unique per pizza and size |
| quantity | Whole number | Pizzas on the line |
| size | Text | Size code: S, M, L, XL, XXL |
| price | Currency | List price of one pizza at that size |
| name | Text | Pizza name |
| category | Text | Classic, Supreme, Veggie or Chicken |
| ingredients | Text | Comma separated ingredient list |

## Model tables (visible and hidden columns)

### Dim_Pizza
| Column | Type | Visible | Notes |
|---|---|---|---|
| pizza_key | Whole number | No | Surrogate key |
| pizza_id | Text | No | Source code |
| name | Text | Yes | Pizza name with "The " and " Pizza" removed |
| category | Text | Yes | Classic, Supreme, Veggie, Chicken |
| size | Text | No | Source size code |
| size_name | Text | Yes | Small, Medium, Large, X Large, XX Large. Sorted by `size_order` |
| size_order | Whole number | No | 1 to 5 |
| price | Currency | No | List price. Use the revenue measures instead |

### Dim_Order
| Column | Type | Visible | Notes |
|---|---|---|---|
| order_key | Whole number | No | Surrogate key, ordered by date and time |
| order_id | Whole number | No | Source order id |
| date, time, order_datetime | Date, time, date and time | No | Order timestamp. `Dim_Date[date]` is used for filtering |
| hour | Whole number | Yes | Hour of the order time |
| gap_min | Decimal | No | Minutes since the previous order the same day, blank for the first order of a day |
| gap_band, gap_band_order | Text, whole number | gap_band only | Buckets of `gap_min`, sorted by the order column |
| distinct_pizzas_in_order | Whole number | No | Distinct pizzas on the order |
| order_type | Text | Yes | Single item or Multi item |
| items_in_order | Whole number | No | Total pizzas on the order |
| items_band | Text | Yes | 1, 2, 3, 4 or more |

### Dim_Date
| Column | Type | Visible | Notes |
|---|---|---|---|
| date | Date | Yes | Every day of 2015. Date table |
| year | Whole number | Yes | 2015 |
| month_name | Text | Yes | |
| day_name | Text | Yes | Monday to Sunday |
| week_start | Date | Yes | Monday of the week |
| day_type | Text | Yes | Weekday or Weekend |
| year_month | Text | Yes | Format yyyy-MM |
| quarter_num, month_num, dow_num | Whole number | No | Sort helpers. `dow_num` is 1 for Monday |

### Fact_OrderLines
| Column | Type | Visible | Notes |
|---|---|---|---|
| order_key | Whole number | No | To `Dim_Order` |
| pizza_key | Whole number | No | To `Dim_Pizza` |
| quantity | Whole number | No | Pizzas on the line. Use `Total Quantity Sold` |

### Dim_Ingredient
| Column | Type | Visible | Notes |
|---|---|---|---|
| ingredient_key | Whole number | No | Surrogate key |
| ingredient | Text | Yes | One of 65 ingredients, as recorded |

### Bridge_Pizza_Ingredient
| Column | Type | Visible | Notes |
|---|---|---|---|
| pizza_key | Whole number | No | To `Dim_Pizza` |
| ingredient_key | Whole number | No | To `Dim_Ingredient` |

The table is hidden. It holds 518 pizza and ingredient pairs.
