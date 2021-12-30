CREATE TABLE public.whale_alerts
(
    id               int8         NOT NULL,
    message          text         NULL,
    link             varchar(255) NULL,
    posted_at        timestamp    NULL,
    asset            varchar(16)  NULL,
    amount           numeric      NULL,
    process_status   varchar(16)  NOT NULL DEFAULT 'NEW'::character varying,
    processed_at     timestamp    NULL,
    process_attempts int2         NOT NULL DEFAULT 0,
    CONSTRAINT whale_alerts_pkey PRIMARY KEY (id)
);
COMMENT ON COLUMN public.whale_alerts.asset IS 'Crypto currency or stable coin';
CREATE INDEX "IDX_AMOUNT" ON public.whale_alerts USING btree (amount);
CREATE INDEX "IDX_ASSET" ON public.whale_alerts USING btree (asset);
CREATE INDEX "IDX_POSTED_AT" ON public.whale_alerts USING btree (posted_at);
CREATE INDEX "IDX_PROCESSED_STATUS" ON public.whale_alerts USING btree (process_status);

CREATE TABLE public.alert_details
(
    alert_id        int8         NOT NULL,
    blockchain      varchar(32)  NULL,
    "type"          varchar(32)  NULL,
    hash            varchar(128) NULL,
    transaction_url varchar(255) NULL,
    from_wallet     varchar(128) NULL,
    to_wallet       varchar(128) NULL,
    CONSTRAINT alert_details_pkey PRIMARY KEY (alert_id),
    CONSTRAINT "FK_ALERT_ID" FOREIGN KEY (alert_id) REFERENCES public.whale_alerts (id) ON DELETE CASCADE ON UPDATE CASCADE
);
