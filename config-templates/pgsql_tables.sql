-- syslogs table
CREATE TABLE IF NOT EXISTS syslogs (
    id SERIAL PRIMARY KEY,
    service character varying(255) NOT NULL,
    log_message text NOT NULL,
    created timestamptz NOT NULL
);

-- aii metrics table
CREATE TABLE IF NOT EXISTS aai_metrics (
    id SERIAL PRIMARY KEY,
    metric_name character varying(255) NOT NULL,
    metric_value int NOT NULL,
    created timestamptz NOT NULL
);

-- Indexes
CREATE INDEX IF NOT EXISTS syslogs_i1 ON syslogs (service);
CREATE INDEX IF NOT EXISTS syslogs_i2 ON syslogs (created);
CREATE INDEX IF NOT EXISTS aai_metrics_i1 ON aai_metrics (created);
CREATE INDEX IF NOT EXISTS aai_metrics_i2 ON aai_metrics (metric_value);