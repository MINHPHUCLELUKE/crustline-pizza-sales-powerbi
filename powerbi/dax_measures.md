# DAX measures and calculated columns

All measures live in the `_Measure` table, grouped in display folders. "Hidden" measures are not used by a report visual; they stay in the model as building blocks or reference calculations.

## 1 Core KPIs

| Measure | DAX | Format |
|---|---|---|
| Total Revenue | `SUMX ( Fact_OrderLines, Fact_OrderLines[quantity] * RELATED ( Dim_Pizza[price] ) )` | $#,0 |
| Total Quantity Sold | `SUM ( Fact_OrderLines[quantity] )` | #,0 |
| Total Orders | `DISTINCTCOUNT ( Fact_OrderLines[order_key] )` | #,0 |
| Average Order Value | `DIVIDE ( [Total Revenue], [Total Orders] )` | $#,0.00 |
| Average Pizzas per Order | `DIVIDE ( [Total Quantity Sold], [Total Orders] )` | 0.00 |

Revenue is calculated line by line (quantity times the price of that pizza and size), so it follows any filter on pizzas, orders or dates.

## 2 Trends and anomalies

| Measure | DAX | Note |
|---|---|---|
| Daily Avg Revenue | `AVERAGEX ( ALL ( Dim_Date ), [Total Revenue] )` | Days with no orders return blank and are skipped, so the average is over 358 trading days |
| Daily Revenue Std Dev | `STDEVX.P ( ALL ( Dim_Date ), [Total Revenue] )` | Same 358 days |
| Revenue Z Score | `IF ( ISBLANK ( [Total Revenue] ), BLANK (), DIVIDE ( [Total Revenue] - [Daily Avg Revenue], [Daily Revenue Std Dev] ) )` | Distance from the daily average in standard deviations |
| Anomaly Flag | `VAR z = [Revenue Z Score] RETURN IF ( ISBLANK ( z ), BLANK (), IF ( z >= 2, "Spike", IF ( z <= -2, "Drop", "Normal" ) ) )` | Threshold of 2 standard deviations |
| Anomaly Days | `COUNTROWS ( FILTER ( VALUES ( Dim_Date[date] ), ABS ( [Revenue Z Score] ) >= 2 ) )` | Returns 16 for the full year |
| Anomaly Color | `SWITCH ( [Anomaly Flag], "Spike", "#1F6F8B", "Drop", "#8C2F39", "#C9B8A3" )` | Colours the daily chart |
| Top Pizza | `VAR Tbl = ADDCOLUMNS ( VALUES ( Dim_Pizza[name] ), "Qty", [Total Quantity Sold] ) RETURN CONCATENATEX ( TOPN ( 1, Tbl, [Qty], DESC ), Dim_Pizza[name], ", " )` | Best seller for the filtered days |
| Anomaly Revenue (hidden) | `IF ( ABS ( [Revenue Z Score] ) >= 2, [Total Revenue] )` | |
| Spike Revenue (hidden) | `IF ( [Revenue Z Score] >= 2, [Total Revenue] )` | |
| Drop Revenue (hidden) | `IF ( [Revenue Z Score] <= -2, [Total Revenue] )` | |
| Upper Threshold (hidden) | `[Daily Avg Revenue] + 2 * [Daily Revenue Std Dev]` | $3,095.28 |
| Lower Threshold (hidden) | `[Daily Avg Revenue] - 2 * [Daily Revenue Std Dev]` | $1,473.77 |
| 7 Day Avg Revenue (hidden) | `AVERAGEX ( DATESINPERIOD ( Dim_Date[date], MAX ( Dim_Date[date] ), -7, DAY ), [Total Revenue] )` | |

## 3 Products and sizes

| Measure | DAX |
|---|---|
| Category Rank by Quantity | `RANKX ( ALL ( Dim_Pizza[category] ), [Total Quantity Sold], , DESC, DENSE )` |
| Category Rank by Revenue | `RANKX ( ALL ( Dim_Pizza[category] ), [Total Revenue], , DESC, DENSE )` |
| Pizza Rank by Quantity (hidden) | `RANKX ( ALL ( Dim_Pizza[name] ), [Total Quantity Sold], , DESC, DENSE )` |
| Pizza Rank by Revenue (hidden) | `RANKX ( ALL ( Dim_Pizza[name] ), [Total Revenue], , DESC, DENSE )` |
| Quantity % of Category (hidden) | `DIVIDE ( [Total Quantity Sold], CALCULATE ( [Total Quantity Sold], ALLEXCEPT ( Dim_Pizza, Dim_Pizza[category] ) ) )` |

## 4 Ingredients and price

| Measure | DAX | Note |
|---|---|---|
| Average Price | `DIVIDE ( [Total Revenue], [Total Quantity Sold] )` | Quantity weighted price per pizza sold. A simple average of the price list would ignore what customers actually bought |
| Correlation Price vs Quantity (Category) | see below | Pearson correlation across the four categories, shown on the report |
| Correlation Price vs Quantity (hidden) | same, over `Dim_Pizza[name]` | Reference only |
| Ingredient Rank (hidden) | `RANKX ( ALL ( Dim_Ingredient[ingredient] ), [Total Quantity Sold], , DESC, DENSE )` | |

Ingredient volumes use `[Total Quantity Sold]` through the bridge table: for an ingredient, the pizzas sold that contain it.

The correlation is written out by hand from the Pearson formula over a small table of (price, quantity) points, one per category:

```
VAR Tbl =
    ADDCOLUMNS (
        VALUES ( Dim_Pizza[category] ),
        "PriceX", [Average Price],
        "QtyY", [Total Quantity Sold]
    )
VAR N = COUNTROWS ( Tbl )
VAR SX = SUMX ( Tbl, [PriceX] )
VAR SY = SUMX ( Tbl, [QtyY] )
VAR SXY = SUMX ( Tbl, [PriceX] * [QtyY] )
VAR SXX = SUMX ( Tbl, [PriceX] ^ 2 )
VAR SYY = SUMX ( Tbl, [QtyY] ^ 2 )
RETURN
    DIVIDE ( N * SXY - SX * SY, SQRT ( ( N * SXX - SX ^ 2 ) * ( N * SYY - SY ^ 2 ) ) )
```

The result is -0.95, recomputed outside Power BI in the QA checklist. With four points it is indicative only.

## 5 Order behaviour

| Measure | DAX | Note |
|---|---|---|
| Single Item Share | `DIVIDE ( [Single Item Orders], [Total Orders] )` | 38.4% |
| Multi Item Share | `DIVIDE ( [Multi Item Orders], [Total Orders] )` | 61.6% |
| Avg Turnaround (min) | `AVERAGE ( Dim_Order[gap_min] )` | Minutes since the previous order the same day. Dim_Order is on the one side of a single-direction relationship, so pizza and category slicers do not filter it: this card and the minutes-between-orders chart always show all categories |
| Peak Hour | `VAR t = TOPN ( 1, VALUES ( Dim_Order[hour] ), [Total Orders], DESC ) RETURN FORMAT ( MAXX ( t, Dim_Order[hour] ), "00" ) & ":00"` | 12:00 |
| Peak Day | `CONCATENATEX ( TOPN ( 1, VALUES ( Dim_Date[day_name] ), [Total Orders], DESC ), Dim_Date[day_name] )` | Friday |
| Avg Orders per Day | `DIVIDE ( [Total Orders], COUNTROWS ( FILTER ( VALUES ( Dim_Date[date] ), [Total Orders] > 0 ) ) )` | Over days with orders |
| Single Item Orders (hidden) | `CALCULATE ( [Total Orders], Dim_Order[order_type] = "Single item" )` | |
| Multi Item Orders (hidden) | `CALCULATE ( [Total Orders], Dim_Order[order_type] = "Multi item" )` | |

## 6 Tooltips

| Measure | DAX |
|---|---|
| Revenue Share % | `DIVIDE ( [Total Revenue], CALCULATE ( [Total Revenue], ALL ( Dim_Pizza ) ) )` |
| Quantity Share % (hidden) | `DIVIDE ( [Total Quantity Sold], CALCULATE ( [Total Quantity Sold], ALL ( Dim_Pizza ) ) )` |

## Calculated columns (Dim_Order)

| Column | DAX | Purpose |
|---|---|---|
| distinct_pizzas_in_order (hidden) | `CALCULATE ( DISTINCTCOUNT ( Fact_OrderLines[pizza_key] ) )` | Distinct pizzas on the order |
| order_type | `IF ( Dim_Order[distinct_pizzas_in_order] = 1, "Single item", "Multi item" )` | Single means one distinct pizza, whatever the quantity |
| items_in_order (hidden) | `CALCULATE ( SUM ( Fact_OrderLines[quantity] ) )` | Total pizzas on the order |
| items_band | `IF ( Dim_Order[items_in_order] >= 4, "4 or more", FORMAT ( Dim_Order[items_in_order], "0" ) )` | Bars on the pizzas per order charts |
| gap_band_order (hidden) | `IF ( ISBLANK ( Dim_Order[gap_min] ), BLANK (), IF ( Dim_Order[gap_min] < 5, 1, IF ( Dim_Order[gap_min] < 10, 2, IF ( Dim_Order[gap_min] < 15, 3, IF ( Dim_Order[gap_min] < 30, 4, 5 ) ) ) ) )` | Sort key for `gap_band` |
| gap_band | `IF ( ISBLANK ( Dim_Order[gap_min] ), BLANK (), IF ( Dim_Order[gap_min] < 5, "Under 5 min", IF ( Dim_Order[gap_min] < 10, "5 to 10 min", IF ( Dim_Order[gap_min] < 15, "10 to 15 min", IF ( Dim_Order[gap_min] < 30, "15 to 30 min", "30 min or more" ) ) ) ) )` | Buckets of time since the previous order |
