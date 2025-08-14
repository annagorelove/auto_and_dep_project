CREATE TABLE public.products (
	category varchar NOT NULL,
	item varchar NOT NULL,
	price int4 NOT NULL,
	CONSTRAINT products_unique UNIQUE (category, item, price)
);

CREATE TABLE public.discount (
	price int4 NOT NULL,
	discount float4 NULL,
	CONSTRAINT discount_unique UNIQUE (price, discount)
);

CREATE TABLE public.store_receipt (
	doc_id varchar NOT NULL,
	item varchar NOT NULL,
	amount int4 NOT NULL,
	category varchar NOT NULL,
	price int4 NOT NULL,
	discount float4 NULL,
	CONSTRAINT store_receipt_unique UNIQUE (doc_id, item, amount, category, price, discount)
);