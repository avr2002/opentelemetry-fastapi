# OpenTelemetry w/ Python: *Beyond "Hello, World!"*


RANDOM NOTES:


What is telemetry data?

Telemetry refers to data emitted from a system and its behavior. The data can come in the form of traces, metrics, and logs.


- [LGTM stack](https://grafana.com/go/webinar/getting-started-with-grafana-lgtm-stack/?pg=docs-grafana-latest-setup-grafana-set-up-grafana-monitoring): 
    - Loki-for logs,
    - Grafana - for dashboards and visualization,
    - Tempo - for traces, and 
    - Mimir - for metrics.



- Observability focuses on understanding the internal state of your systems based on the data they produce, which helps determine if your infrastructure is healthy. [Reference: Grafana Docs](https://grafana.com/docs/grafana/latest/fundamentals/intro-to-prometheus/)


- Metrics is a time series data that has an associated timestamp and a numerical value, which can represent some state or event in your system. Metrics often have associated labels, called **dimensions/attributes**, which help you identify the data you are looking at.

    - For example, a metric could be the number of requests your server is handling, and the dimensions could be the HTTP method, the status code, or the endpoint being accessed.
