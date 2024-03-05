-- public.authorization_codes definition

-- Drop table

-- DROP TABLE public.authorization_codes;

CREATE TABLE public.authorization_codes (
	code varchar NOT NULL,
	client_id uuid NOT NULL,
	user_id int4 NOT NULL,
	redirect varchar NOT NULL,
	"scope" varchar NOT NULL,
	used bool NOT NULL DEFAULT false,
	expiration timestamp NOT NULL DEFAULT (now() + '00:10:00'::interval),
	CONSTRAINT authorization_codes_pkey PRIMARY KEY (code)
);


-- public.client_sites definition

-- Drop table

-- DROP TABLE public.client_sites;

CREATE TABLE public.client_sites (
	id serial4 NOT NULL,
	client_id uuid NOT NULL,
	hostname varchar NOT NULL,
	redirect varchar NOT NULL,
	CONSTRAINT client_sites_pkey PRIMARY KEY (id)
);


-- public.clients definition

-- Drop table

-- DROP TABLE public.clients;

CREATE TABLE public.clients (
	id serial4 NOT NULL,
	client_id uuid NOT NULL DEFAULT gen_random_uuid(),
	client_name varchar NOT NULL,
	client_secret_hash varchar NOT NULL,
	CONSTRAINT clients_pkey PRIMARY KEY (id),
	CONSTRAINT clients_unique UNIQUE (client_secret_hash, client_id, client_name)
);


-- public.password_reset definition

-- Drop table

-- DROP TABLE public.password_reset;

CREATE TABLE public.password_reset (
	id serial4 NOT NULL,
	user_id int4 NOT NULL,
	reset_token uuid NOT NULL DEFAULT gen_random_uuid(),
	expiration_date timestamp NOT NULL DEFAULT (now() + '1 day'::interval),
	is_valid bool NOT NULL DEFAULT true
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
	verification_status bool NOT NULL DEFAULT false,
	confirmation_date timestamp NULL,
	attempts int4 NOT NULL DEFAULT 0,
	CONSTRAINT email_verification_pkey PRIMARY KEY (id),
	CONSTRAINT email_verification_unique UNIQUE (confirmation_token),
	CONSTRAINT email_verification_users_fk FOREIGN KEY (user_id) REFERENCES public.users(user_id) ON DELETE CASCADE DEFERRABLE
);


-- public.login_attempts definition

-- Drop table

-- DROP TABLE public.login_attempts;

CREATE TABLE public.login_attempts (
	id serial4 NOT NULL,
	user_id int4 NOT NULL,
	attempts int4 NOT NULL DEFAULT 0,
	CONSTRAINT login_attempts_pk PRIMARY KEY (id),
	CONSTRAINT login_attempts_unique UNIQUE (user_id),
	CONSTRAINT login_attempts_users_fk FOREIGN KEY (user_id) REFERENCES public.users(user_id) ON DELETE CASCADE
);
