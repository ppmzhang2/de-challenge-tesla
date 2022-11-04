# Data Engineer Challenge - Tesla

Please write an application preferably in python, that calls the [USGS API](https://earthquake.usgs.gov/fdsnws/event/1/) and store the result in a relational database of your choice.

## Processing & Analytical Goals:

1. Please query all events that have occurred during year 2017
2. Read a JSON response from the API
3. Design the database objects required to store the result in a relational fashion.
4. Store the response in those objects
5. Provide query/analysis to give biggest earthquake of 2017
6. Provide query/analysis to give most probable hour of the day for the earthquakes bucketed by the range of magnitude:
    * `[0, 1)`
    * `[1, 2)`
    * `[2, 3)`
    * `[3, 4)`
    * `[4, 5)`
    * `[5, 6)`
    * `[6, inf)`

## Answers

### Data Processing (1 - 4)

According to the USGS API document, JSON response of all events in 2017 can be queried via parameterized link:

```html
https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2017-01-01&endtime=2017-12-31
```

where the date parameters are formatted as `YYYY-MM-DD`. To query data efficiently the `AIOHTTP` [asynchronous request method](./app/earthquake.py) is used.

The response GeoJSON summary format:

```
{
  type: "FeatureCollection",
  metadata: {
    generated: Long Integer,
    url: String,
    title: String,
    api: String,
    count: Integer,
    status: Integer
  },
  bbox: [
    minimum longitude,
    minimum latitude,
    minimum depth,
    maximum longitude,
    maximum latitude,
    maximum depth
  ],
  features: [
    {
      type: "Feature",
      properties: {
        mag: Decimal,
        place: String,
        time: Long Integer,
        updated: Long Integer,
        tz: Integer,
        url: String,
        detail: String,
        felt:Integer,
        cdi: Decimal,
        mmi: Decimal,
        alert: String,
        status: String,
        tsunami: Integer,
        sig:Integer,
        net: String,
        code: String,
        ids: String,
        sources: String,
        types: String,
        nst: Integer,
        dmin: Decimal,
        rms: Decimal,
        gap: Decimal,
        magType: String,
        type: String
      },
      geometry: {
        type: "Point",
        coordinates: [
          longitude,
          latitude,
          depth
        ]
      },
      id: String
    },
    …
  ]
}
```

Only the `features` will be extracted, according to which the SQLite [database schema](./app/models/tables.py) is structured.

To save earthquakes event data in 2017:

```sh
pdm run python -m app save 2017-01-01 2017-12-31
```

### Analytics (5 - 6)

To export the top 10 biggest earthquakes of 2017:

```sh
pdm run python -m app top
```

Sample answer is stored [here](./answers/top_earthquakes.csv).

To plot the [earthquake frequency](./answers/count_plot.pdf) by hour of one day (UTC) in different magnitude buckets:

```sh
pdm run python -m app plot
```

## Reference

1. https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php
2. https://earthquake.usgs.gov/fdsnws/event/1
