# Report guide

Six pages, 1920 by 1080, with the same layout on each: brand panel and page navigation on the left, title and slicers on top, visuals in the middle and a short takeaway at the bottom.

## Shared design

- **Navigation:** a page navigator in the left panel, with the current page highlighted.
- **Slicers:** a date range slicer on every page, and a category slicer on every page except Orders (order level questions do not depend on pizza category). Slicers are synced across pages, so a choice on one page carries to the others.
- **Colour:** one colour per pizza category on every page (Classic tomato red, Supreme gold, Veggie green, Chicken blue). Spike and drop colours are used only on the Trends page. Heatmaps use a light-to-dark cheese to tomato ramp.
- **Theme:** custom palette on a warm cream page with white cards and thin borders. Chart titles say what is shown, and notes sit next to the visuals they affect.
- **Order of reading:** each page starts with headline cards or the main chart at the top left and ends with the takeaway.

## Pages

| # | Page | Question | Visuals |
|---|---|---|---|
| 1 | Overview | How did the year go? | Five KPI cards (total revenue, quantity sold, total orders, average order value, average pizzas per order), monthly revenue line, revenue by category, top 5 pizzas by revenue, orders by day of week |
| 2 | Trends | When did sales spike or drop? | Weekly revenue with an average line (first and last week are partial), daily revenue coloured by anomaly (blue spike, red drop) with an average line, top pizzas on a selected day, cards for anomaly days, daily average and standard deviation, a table of anomaly days with z score and best seller. Click a date in the table to filter the top pizzas chart |
| 3 | Day & Hour | When are we busy? | Cards for peak hour, peak day, average orders per day and average turnaround, a day by hour heatmap, orders by hour, average orders per day by weekday, average minutes between orders by hour |
| 4 | Products | What sells? | Top 5 and bottom 5 pizzas by quantity and by revenue, category ranking table, units sold by size and category |
| 5 | Ingredients | What goes into what sells, and does price matter? | Price against units sold by category with the correlation card, top 10 and bottom 10 ingredients by units sold, ingredient by category matrix (top 15) |
| 6 | Orders | How do customers order? | Cards for pizzas per order, single and multi pizza order share and average turnaround, time since the previous order, single versus multi pizza donut, average order value and order count by pizzas per order |

## Interaction

- Cross-filtering works between visuals on a page, and slicers filter everything they apply to.
- The daily revenue chart colours points through the `Anomaly Color` measure, so the same 2 standard deviation rule defines the flag, the colour, the anomaly card and the table.
- Pages open with no filters applied, and the file opens on the Overview page.
