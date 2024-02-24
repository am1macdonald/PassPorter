-- DROP SCHEMA public;

CREATE SCHEMA public AUTHORIZATION pg_database_owner;

-- public.client_sites definition

-- Drop table

-- DROP TABLE public.client_sites;

CREATE TABLE public.client_sites (
	id serial4 NOT NULL,
	client_id int4 NOT NULL,
	hostname varchar NOT NULL,
	redirect varchar NOT NULL,
	CONSTRAINT client_sites_pkey PRIMARY KEY (id)
);


-- public.clients definition

-- Drop table

-- DROP TABLE public.clients;

CREATE TABLE public.clients (
	id serial4 NOT NULL,
	client_id varchar NOT NULL,
	client_name varchar NOT NULL,
	CONSTRAINT clients_pkey PRIMARY KEY (id)
);


-- public.users definition

-- Drop table

-- DROP TABLE public.users;

CREATE TABLE public.users (
	user_id serial4 NOT NULL,
	username varchar NOT NULL,
	password_hash varchar NOT NULL,
	email varchar NOT NULL,
	created_at timestamp NULL DEFAULT now(),
	last_login timestamp NULL,
	CONSTRAINT "Users_pkey" PRIMARY KEY (user_id),
	CONSTRAINT users_unique UNIQUE (username, email)
);


-- public.email_verification definition

-- Drop table

-- DROP TABLE public.email_verification;

CREATE TABLE public.email_verification (
	id serial4 NOT NULL,
	user_id int4 NOT NULL,
	confirmation_token varchar NOT NULL DEFAULT gen_random_uuid(),
	expiration_date timestamp NOT NULL DEFAULT (now() + '7 days'::interval),
	confirmed bool NOT NULL DEFAULT false,
	confirmation_date timestamp NULL,
	attempts int4 NOT NULL DEFAULT 0,
	CONSTRAINT email_verification_pkey PRIMARY KEY (id),
	CONSTRAINT email_verification_unique UNIQUE (confirmation_token),
	CONSTRAINT email_verification_users_fk FOREIGN KEY (user_id) REFERENCES public.users(user_id) ON DELETE CASCADE DEFERRABLE
);
