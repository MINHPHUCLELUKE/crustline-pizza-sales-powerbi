# Power Query steps

The raw CSV is imported as is. The file is never edited outside Power BI, and all cleaning is done in M. Both source queries read one text parameter, `SourceFilePath`, so pointing the report at your own copy of the CSV means changing one value.

## Query map

| Query | Role | Loaded to model |
|---|---|---|
| `SourceFilePath` | Text parameter with the full path of the CSV | No |
| `data_pizza` | Raw import, ten untyped columns | No |
| `data_pizza_clean` | Typed and cleaned order lines, plus size name and size order | No |
| `pizza_ingredients` | One row per pizza and ingredient, from the comma separated list | No |
| `Pizza_Ingredients_Full` | Distinct pizza and ingredient pairs, the input of the ingredient tables | No |
| `Dim_Pizza` | One row per pizza and size | Yes |
| `Dim_Order` | One row per order, with date, hour and gap since the previous order | Yes |
| `Dim_Date` | One row per day of 2015 | Yes |
| `Fact_OrderLines` | One row per order line, keys and quantity | Yes |
| `Dim_Ingredient` | One row per ingredient | Yes |
| `Bridge_Pizza_Ingredient` | Pizza to ingredient pairs | Yes |

## data_pizza (raw)

```
let
  Source = Csv.Document(File.Contents(SourceFilePath), [Delimiter = ",", Columns = 10, Encoding = 65001])
in
  Source
```

## data_pizza_clean

What it does: promotes headers, sets types (with the en-US culture so prices and dates parse the same on any machine), trims and cleans text columns, then derives `size_name` and `size_order` from the size code.

```
let
  Source = Csv.Document(File.Contents(SourceFilePath), [Delimiter = ",", Columns = 10, Encoding = 65001]),
  #"Promoted headers" = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
  #"Changed column type" = Table.TransformColumnTypes(#"Promoted headers", {{"order_id", Int64.Type}, {"date", type date}, {"time", type time}, {"pizza_id", type text}, {"quantity", Int64.Type}, {"size", type text}, {"price", type number}, {"name", type text}, {"category", type text}, {"ingredients", type text}}, "en-US"),
  #"Changed column type 1" = Table.TransformColumnTypes(#"Changed column type", {{"price", Currency.Type}}),
  #"Trimmed text" = Table.TransformColumns(#"Changed column type 1", {{"ingredients", each Text.Trim(_), type nullable text}, {"category", each Text.Trim(_), type nullable text}, {"name", each Text.Trim(_), type nullable text}, {"pizza_id", each Text.Trim(_), type nullable text}, {"size", each Text.Trim(_), type nullable text}}),
  #"Cleaned text" = Table.TransformColumns(#"Trimmed text", {{"ingredients", each Text.Clean(_), type nullable text}, {"category", each Text.Clean(_), type nullable text}, {"name", each Text.Clean(_), type nullable text}, {"pizza_id", each Text.Clean(_), type nullable text}, {"size", each Text.Clean(_), type nullable text}}),
  #"Inserted conditional column" = Table.AddColumn(#"Cleaned text", "size_name", each if [size] = "S" then "Small" else if [size] = "M" then "Medium" else if [size] = "L" then "Large" else if [size] = "XL" then "X Large" else if [size] = "XXL" then "XX Large" else if [size] = "" then null else ""),
  #"Inserted conditional column 1" = Table.AddColumn(#"Inserted conditional column", "size_order", each if [size] = "S" then 1 else if [size] = "M" then 2 else if [size] = "L" then 3 else if [size] = "XL" then 4 else if [size] = "XXL" then 5 else null),
  #"Changed column type 2" = Table.TransformColumnTypes(#"Inserted conditional column 1", {{"size_name", type text}, {"size_order", Int64.Type}})
in
  #"Changed column type 2"
```

## pizza_ingredients

What it does: keeps one row per pizza, splits the ingredient list on ", " into rows, trims each item and repairs one ingredient whose first character arrives garbled (see the data quality report).

```
let
  Source = data_pizza_clean,
  #"Removed other columns" = Table.SelectColumns(Source, {"pizza_id", "ingredients"}),
  #"Removed duplicates" = Table.Distinct(#"Removed other columns", {"pizza_id", "ingredients"}),
  #"Split column by delimiter" = Table.ExpandListColumn(Table.TransformColumns(#"Removed duplicates", {{"ingredients", Splitter.SplitTextByDelimiter(", "), let itemType = (type nullable text) meta [Serialized.Text = true] in type {itemType}}}), "ingredients"),
  #"Trimmed text" = Table.TransformColumns(#"Split column by delimiter", {{"ingredients", each Text.Trim(_), type nullable text}}),
  #"Fixed Nduja" = Table.TransformColumns(#"Trimmed text", {{"ingredients", each if _ <> null and Text.Contains(_, "Nduja") then "'" & Text.Middle(_, Text.PositionOf(_, "Nduja")) else _, type nullable text}}),
  #"Renamed columns" = Table.RenameColumns(#"Fixed Nduja", {{"ingredients", "ingredient"}})
in
  #"Renamed columns"
```

## Pizza_Ingredients_Full

```
let
  Source = pizza_ingredients,
  #"Removed duplicates" = Table.Distinct(Source, {"pizza_id", "ingredient"})
in
  #"Removed duplicates"
```

Ingredients are used exactly as recorded. No base ingredient (for example mozzarella or tomato sauce) is added.

## Dim_Pizza

One row per distinct pizza, size and price, with a surrogate key. "The " and " Pizza" are removed from names so labels fit in charts.

```
let
  Source = data_pizza_clean,
  #"Removed other columns" = Table.SelectColumns(Source, {"pizza_id", "name", "category", "size", "size_name", "size_order", "price"}),
  #"Removed duplicates" = Table.Distinct(#"Removed other columns"),
  #"Added index" = Table.AddIndexColumn(#"Removed duplicates", "Index", 1, 1, Int64.Type),
  #"Renamed columns" = Table.RenameColumns(#"Added index", {{"Index", "Index_Key"}}),
  #"Reordered columns" = Table.ReorderColumns(#"Renamed columns", {"Index_Key", "pizza_id", "name", "category", "size", "size_name", "size_order", "price"}),
  #"Renamed columns 1" = Table.RenameColumns(#"Reordered columns", {{"Index_Key", "pizza_key"}}),
  #"Replaced value" = Table.ReplaceValue(#"Renamed columns 1", "The ", "", Replacer.ReplaceText, {"name"}),
  #"Replaced value 1" = Table.ReplaceValue(#"Replaced value", " Pizza", "", Replacer.ReplaceText, {"name"})
in
  #"Replaced value 1"
```

## Dim_Order

One row per order. Orders are sorted by date and time and numbered. Each order is joined to the one before it to get `gap_min`, the minutes since the previous order on the same day (blank for the first order of a day). `hour` is taken from the time.

```
let
  Source = data_pizza_clean,
  #"Removed other columns" = Table.SelectColumns(Source, {"order_id", "date", "time"}),
  #"Removed duplicates" = Table.Distinct(#"Removed other columns"),
  #"Added custom" = Table.TransformColumnTypes(Table.AddColumn(#"Removed duplicates", "order_datetime", each [date] & [time]), {{"order_datetime", type datetime}}),
  #"Sorted rows" = Table.Sort(#"Added custom", {{"order_datetime", Order.Ascending}, {"order_id", Order.Ascending}}),
  #"Added index" = Table.AddIndexColumn(#"Sorted rows", "Index", 1, 1, Int64.Type),
  #"Renamed columns" = Table.RenameColumns(#"Added index", {{"Index", "Order_key"}}),
  #"Reordered columns" = Table.ReorderColumns(#"Renamed columns", {"Order_key", "order_id", "date", "time", "order_datetime"}),
  #"Inserted subtraction" = Table.AddColumn(#"Reordered columns", "Subtraction", each [Order_key] - 1, Int64.Type),
  #"Renamed columns 1" = Table.RenameColumns(#"Inserted subtraction", {{"Subtraction", "prev_key"}}),
  #"Merged queries" = Table.NestedJoin(#"Renamed columns 1", {"prev_key"}, #"Renamed columns 1", {"Order_key"}, "Renamed columns 1", JoinKind.LeftOuter),
  #"Expanded Renamed columns 1" = Table.ExpandTableColumn(#"Merged queries", "Renamed columns 1", {"order_datetime"}, {"order_datetime.1"}),
  #"Renamed columns 2" = Table.RenameColumns(#"Expanded Renamed columns 1", {{"order_datetime.1", "previous_Datetime"}}),
  #"Inserted date subtraction" = Table.AddColumn(#"Renamed columns 2", "Subtraction", each Duration.Days([order_datetime] - [previous_Datetime]), type nullable Int64.Type),
  #"Changed column type" = Table.TransformColumnTypes(#"Inserted date subtraction", {{"Subtraction", type duration}}),
  #"Calculated total minutes" = Table.TransformColumns(#"Changed column type", {{"Subtraction", each Duration.TotalMinutes(_), type nullable number}}),
  #"Added custom 1" = Table.TransformColumnTypes(Table.AddColumn(#"Calculated total minutes", "diff_min", each Duration.TotalMinutes([order_datetime] - [previous_Datetime])), {{"diff_min", type number}}),
  #"Inserted date" = Table.AddColumn(#"Added custom 1", "Date (2)", each DateTime.Date([previous_Datetime]), type nullable date),
  #"Renamed columns 3" = Table.RenameColumns(#"Inserted date", {{"Date (2)", "Prev_date"}}),
  #"Inserted conditional column" = Table.AddColumn(#"Renamed columns 3", "gap_min", each if [Prev_date] = null then null else if [Prev_date] <> [date] then null else [diff_min]),
  #"Removed columns" = Table.RemoveColumns(#"Inserted conditional column", {"prev_key", "previous_Datetime", "diff_min", "Prev_date"}),
  #"Changed column type 1" = Table.TransformColumnTypes(#"Removed columns", {{"gap_min", type number}}),
  #"Removed columns 1" = Table.RemoveColumns(#"Changed column type 1", {"Subtraction"}),
  #"Inserted hour" = Table.AddColumn(#"Removed columns 1", "Hour", each Time.Hour([time]), type nullable Int64.Type),
  #"Renamed columns 4" = Table.RenameColumns(#"Inserted hour", {{"Order_key", "order_key"}, {"Hour", "hour"}})
in
  #"Renamed columns 4"
```

## Dim_Date

A calendar for every day of 2015, with year, quarter, month, names, Monday-based weekday number, week start, weekday or weekend flag and year-month. It is marked as the date table in the model.

```
let
  Source = List.Dates(#date(2015,1,1), 365, #duration(1,0,0,0)),
  #"Converted to table" = Table.FromList(Source, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
  #"Renamed columns" = Table.RenameColumns(#"Converted to table", {{"Column1", "date"}}),
  #"Changed column type" = Table.TransformColumnTypes(#"Renamed columns", {{"date", type date}}),
  #"Inserted year" = Table.AddColumn(#"Changed column type", "Year", each Date.Year([date]), type nullable number),
  #"Inserted quarter" = Table.AddColumn(#"Inserted year", "Quarter", each Date.QuarterOfYear([date]), type nullable number),
  #"Renamed columns 1" = Table.RenameColumns(#"Inserted quarter", {{"Year", "year"}, {"Quarter", "quarter_num"}}),
  #"Inserted month" = Table.AddColumn(#"Renamed columns 1", "Month", each Date.Month([date]), type nullable number),
  #"Renamed columns 2" = Table.RenameColumns(#"Inserted month", {{"Month", "month"}}),
  #"Inserted month name" = Table.AddColumn(#"Renamed columns 2", "Month name", each Date.MonthName([date]), type nullable text),
  #"Renamed columns 3" = Table.RenameColumns(#"Inserted month name", {{"Month name", "month_name"}}),
  #"Inserted day name" = Table.AddColumn(#"Renamed columns 3", "Day name", each Date.DayOfWeekName([date]), type nullable text),
  #"Renamed columns 4" = Table.RenameColumns(#"Inserted day name", {{"Day name", "day_name"}}),
  #"Added custom" = Table.AddColumn(#"Renamed columns 4", "dow_num", each Date.DayOfWeek([date], Day.Monday) + 1),
  #"Added custom 1" = Table.AddColumn(#"Added custom", "week_start", each Date.StartOfWeek([date], Day.Monday)),
  #"Added custom 2" = Table.AddColumn(#"Added custom 1", "day_type", each if [dow_num] >= 6 then "Weekend" else "Weekday"),
  #"Added custom 3" = Table.AddColumn(#"Added custom 2", "year_month", each Date.ToText([date], "yyyy-MM")),
  #"Changed column type 1" = Table.TransformColumnTypes(#"Added custom 3", {{"dow_num", Int64.Type}, {"week_start", type date}, {"day_type", type text}, {"year_month", type text}, {"year", Int64.Type}, {"quarter_num", Int64.Type}, {"month", Int64.Type}}),
  #"Renamed columns 5" = Table.RenameColumns(#"Changed column type 1", {{"month", "month_num"}})
in
  #"Renamed columns 5"
```

## Fact_OrderLines

Order lines with the pizza and order surrogate keys looked up by merge, and the text ids removed.

```
let
  Source = data_pizza_clean,
  #"Removed other columns" = Table.SelectColumns(Source, {"order_id", "pizza_id", "quantity"}),
  #"Merged queries" = Table.NestedJoin(#"Removed other columns", {"pizza_id"}, Dim_Pizza, {"pizza_id"}, "Dim_Pizza", JoinKind.LeftOuter),
  #"Expanded Dim_Pizza" = Table.ExpandTableColumn(#"Merged queries", "Dim_Pizza", {"pizza_key"}, {"pizza_key"}),
  #"Merged queries 1" = Table.NestedJoin(#"Expanded Dim_Pizza", {"order_id"}, Dim_Order, {"order_id"}, "Dim_Order", JoinKind.LeftOuter),
  #"Expanded Dim_Order" = Table.ExpandTableColumn(#"Merged queries 1", "Dim_Order", {"order_key"}, {"order_key"}),
  #"Removed columns" = Table.RemoveColumns(#"Expanded Dim_Order", {"order_id", "pizza_id"})
in
  #"Removed columns"
```

## Dim_Ingredient

```
let
  Source = Pizza_Ingredients_Full,
  #"Removed other columns" = Table.SelectColumns(Source, {"ingredient"}),
  #"Sorted rows" = Table.Sort(#"Removed other columns", {{"ingredient", Order.Ascending}}),
  #"Removed duplicates" = Table.Distinct(#"Sorted rows"),
  #"Added index" = Table.AddIndexColumn(#"Removed duplicates", "Index", 0, 1, Int64.Type),
  #"Reordered columns" = Table.ReorderColumns(#"Added index", {"Index", "ingredient"}),
  #"Renamed columns" = Table.RenameColumns(#"Reordered columns", {{"Index", "ingredient_key"}}),
  #"Removed columns" = Table.RemoveColumns(#"Renamed columns", {"ingredient_key"}),
  #"Added index 1" = Table.AddIndexColumn(#"Removed columns", "Index", 1, 1, Int64.Type),
  #"Reordered columns 1" = Table.ReorderColumns(#"Added index 1", {"Index", "ingredient"}),
  #"Renamed columns 1" = Table.RenameColumns(#"Reordered columns 1", {{"Index", "ingredient_key"}})
in
  #"Renamed columns 1"
```

## Bridge_Pizza_Ingredient

```
let
  Source = Pizza_Ingredients_Full,
  #"Merged queries" = Table.NestedJoin(Source, {"pizza_id"}, Dim_Pizza, {"pizza_id"}, "Dim_Pizza", JoinKind.LeftOuter),
  #"Expanded Dim_Pizza" = Table.ExpandTableColumn(#"Merged queries", "Dim_Pizza", {"pizza_key"}, {"pizza_key"}),
  #"Merged queries 1" = Table.NestedJoin(#"Expanded Dim_Pizza", {"ingredient"}, Dim_Ingredient, {"ingredient"}, "Dim_Ingredient", JoinKind.LeftOuter),
  #"Expanded Dim_Ingredient" = Table.ExpandTableColumn(#"Merged queries 1", "Dim_Ingredient", {"ingredient_key"}, {"ingredient_key"}),
  #"Removed columns" = Table.RemoveColumns(#"Expanded Dim_Ingredient", {"ingredient", "pizza_id"})
in
  #"Removed columns"
```
