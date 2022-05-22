## My first project in Python :)

The script periodically polls the Telegram channel [whale_alert_io](https://t.me/whale_alert_io) and adds new records to
the database, pre-breaking the message content into useful data.
The script also sends a bunch of messages in one event to RabbitMQ.

A typical message looks something like this:

``
🚨 🚨 🚨 🚨 🚨 🚨 🚨 🚨 🚨 🚨 27,205 #ETH (109,887,570 USD) transferred from unknown wallet to #Binance Details (https://whale-alert.io/transaction/ethereum/a975f1f53ef445d6ef6320abf4c7ad8047886cdb0a9b00f7cc61c54534f219bb)
``

The type of asset, the amount, the link to the explorer's website is extracted from it, and the message is cleared of
different icons at the beginning of the text. The rest of the fields in the table are intended for subsequent processing
of transactions. It is assumed that there will be another application that will open links to this site and pump out
additional information from there, which will be persisted in the `alert_details` table, and the results of execution
will be persisted in the `whale_alerts` table in the appropriate fields.

### SQL structure (PostgreSQL)

The main table `whale_alerts`

``` sql
CREATE TABLE public.whale_alerts (
	id int8 NOT NULL,
	message text NULL,
	link varchar(255) NULL,
	posted_at timestamp NULL,
	asset varchar(16) NULL,
	amount numeric NULL,
	process_status varchar(16) NOT NULL DEFAULT 'NEW'::character varying,
	processed_at timestamp NULL,
	process_attempts int2 NOT NULL DEFAULT 0,
	CONSTRAINT whale_alerts_pkey PRIMARY KEY (id)
);
COMMENT ON COLUMN public.whale_alerts.asset IS 'Crypto currency or stable coin';
CREATE INDEX "IDX_AMOUNT" ON public.whale_alerts USING btree (amount);
CREATE INDEX "IDX_ASSET" ON public.whale_alerts USING btree (asset);
CREATE INDEX "IDX_POSTED_AT" ON public.whale_alerts USING btree (posted_at);
CREATE INDEX "IDX_PROCESSED_STATUS" ON public.whale_alerts USING btree (process_status);
```
