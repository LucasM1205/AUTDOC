--
-- PostgreSQL database dump
--

-- Dumped from database version 13.18 (Debian 13.18-1.pgdg120+1)
-- Dumped by pg_dump version 13.18 (Debian 13.18-1.pgdg120+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO "user";

--
-- Name: benutzer; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public.benutzer (
    id integer NOT NULL,
    email character varying(255) NOT NULL,
    rolle character varying(50) NOT NULL,
    passwort character varying(255) NOT NULL,
    erstellt_am timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    student_id integer
);


ALTER TABLE public.benutzer OWNER TO "user";

--
-- Name: benutzer_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public.benutzer_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.benutzer_id_seq OWNER TO "user";

--
-- Name: benutzer_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public.benutzer_id_seq OWNED BY public.benutzer.id;


--
-- Name: dokumenten_metadaten; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public.dokumenten_metadaten (
    id integer NOT NULL,
    dokument_name character varying(255) NOT NULL,
    typ character varying(50) NOT NULL,
    erstelldatum timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.dokumenten_metadaten OWNER TO "user";

--
-- Name: dokumenten_metadaten_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public.dokumenten_metadaten_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.dokumenten_metadaten_id_seq OWNER TO "user";

--
-- Name: dokumenten_metadaten_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public.dokumenten_metadaten_id_seq OWNED BY public.dokumenten_metadaten.id;


--
-- Name: fachbereich_sekretariat; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public.fachbereich_sekretariat (
    id integer NOT NULL,
    joker_antrag_id integer NOT NULL,
    joker_verfuegbar boolean DEFAULT true,
    letzte_aenderung timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    bemerkungen text
);


ALTER TABLE public.fachbereich_sekretariat OWNER TO "user";

--
-- Name: fachbereich_sekretariat_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public.fachbereich_sekretariat_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.fachbereich_sekretariat_id_seq OWNER TO "user";

--
-- Name: fachbereich_sekretariat_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public.fachbereich_sekretariat_id_seq OWNED BY public.fachbereich_sekretariat.id;


--
-- Name: joker_antraege; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public.joker_antraege (
    id integer NOT NULL,
    student_id integer NOT NULL,
    fach character varying(255),
    pruefungsnummer character varying(50),
    pruefer character varying(255),
    joker_verwendet boolean DEFAULT false,
    doppelstudium boolean DEFAULT false,
    doppelstudium_name character varying(255),
    datum_erstellung timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    status character varying(50) DEFAULT 'Ausstehend'::character varying,
    bemerkungen text,
    dokumenten_metadaten_id integer
);


ALTER TABLE public.joker_antraege OWNER TO "user";

--
-- Name: joker_antraege_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public.joker_antraege_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.joker_antraege_id_seq OWNER TO "user";

--
-- Name: joker_antraege_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public.joker_antraege_id_seq OWNED BY public.joker_antraege.id;


--
-- Name: pruefungsausschuss; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public.pruefungsausschuss (
    id integer NOT NULL,
    joker_antrag_id integer NOT NULL,
    unterschrift character varying(255),
    bedenken text,
    datum_bearbeitung timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.pruefungsausschuss OWNER TO "user";

--
-- Name: pruefungsausschuss_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public.pruefungsausschuss_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.pruefungsausschuss_id_seq OWNER TO "user";

--
-- Name: pruefungsausschuss_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public.pruefungsausschuss_id_seq OWNED BY public.pruefungsausschuss.id;


--
-- Name: studenten; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public.studenten (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    vorname character varying(255) NOT NULL,
    matrikelnummer character varying(50) NOT NULL,
    fachbereich character varying(255) NOT NULL,
    studiengang character varying(255) NOT NULL,
    unterschrift character varying(255),
    erstellt_am timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.studenten OWNER TO "user";

--
-- Name: studenten_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public.studenten_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.studenten_id_seq OWNER TO "user";

--
-- Name: studenten_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public.studenten_id_seq OWNED BY public.studenten.id;


--
-- Name: benutzer id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.benutzer ALTER COLUMN id SET DEFAULT nextval('public.benutzer_id_seq'::regclass);


--
-- Name: dokumenten_metadaten id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.dokumenten_metadaten ALTER COLUMN id SET DEFAULT nextval('public.dokumenten_metadaten_id_seq'::regclass);


--
-- Name: fachbereich_sekretariat id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.fachbereich_sekretariat ALTER COLUMN id SET DEFAULT nextval('public.fachbereich_sekretariat_id_seq'::regclass);


--
-- Name: joker_antraege id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.joker_antraege ALTER COLUMN id SET DEFAULT nextval('public.joker_antraege_id_seq'::regclass);


--
-- Name: pruefungsausschuss id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.pruefungsausschuss ALTER COLUMN id SET DEFAULT nextval('public.pruefungsausschuss_id_seq'::regclass);


--
-- Name: studenten id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.studenten ALTER COLUMN id SET DEFAULT nextval('public.studenten_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: user
--

COPY public.alembic_version (version_num) FROM stdin;
\.


--
-- Data for Name: benutzer; Type: TABLE DATA; Schema: public; Owner: user
--

COPY public.benutzer (id, email, rolle, passwort, erstellt_am, student_id) FROM stdin;
1	student@thm.de	Student	scrypt:32768:8:1$zaRNrEykgx7kwy9q$0d9322a6f7a801ef847746c3c68b166a8203a1d8a06ffb35e28ec31122c3444cf6d0a02615bf6d33cda9be52a0b06107a5b3c9cb64dd4c038efa525a1f5e69ba	2024-12-07 15:34:48.223631	1
\.


--
-- Data for Name: dokumenten_metadaten; Type: TABLE DATA; Schema: public; Owner: user
--

COPY public.dokumenten_metadaten (id, dokument_name, typ, erstelldatum) FROM stdin;
1	joker_antrag_2.pdf	PDF	2024-12-07 16:26:28.505866
2	joker_antrag_3.pdf	PDF	2024-12-07 16:28:35.894029
3	joker_antrag_4.pdf	PDF	2024-12-07 16:37:08.238257
4	joker_antrag_5.pdf	PDF	2024-12-07 19:00:25.572479
5	joker_antrag_6.pdf	PDF	2024-12-07 19:03:00.938299
6	joker_antrag_7.pdf	PDF	2024-12-07 19:14:00.087039
7	joker_antrag_8.pdf	PDF	2024-12-07 19:28:03.107153
\.


--
-- Data for Name: fachbereich_sekretariat; Type: TABLE DATA; Schema: public; Owner: user
--

COPY public.fachbereich_sekretariat (id, joker_antrag_id, joker_verfuegbar, letzte_aenderung, bemerkungen) FROM stdin;
\.


--
-- Data for Name: joker_antraege; Type: TABLE DATA; Schema: public; Owner: user
--

COPY public.joker_antraege (id, student_id, fach, pruefungsnummer, pruefer, joker_verwendet, doppelstudium, doppelstudium_name, datum_erstellung, status, bemerkungen, dokumenten_metadaten_id) FROM stdin;
1	1	Mathematik 1	MAT101	Prof. Dr. Beispiel	f	f	\N	2024-12-07 15:35:00.724953	Ausstehend	\N	\N
2	2	testfach	123456	Testmann, Thomas	f	f	\N	2024-12-07 16:26:28.0562	Ausstehend	\N	1
3	2	testfach	123456	Testmann, Thomas	f	f	\N	2024-12-07 16:28:35.419795	Ausstehend	\N	2
4	2	testfach	123456	Testmann, Thomas	f	f	\N	2024-12-07 16:37:07.668487	Ausstehend	\N	3
5	1	testfach	123456	Testmann, Thomas	f	f	\N	2024-12-07 19:00:24.926013	Ausstehend	\N	4
6	1	testfach	123456	Testmann, Thomas	f	f	\N	2024-12-07 19:02:59.266296	Ausstehend	\N	5
7	1	testfach	123456	Testmann, Thomas	f	f	\N	2024-12-07 19:13:59.648592	Ausstehend	\N	6
8	1	testfach	123456	Testmann, Thomas	f	f	\N	2024-12-07 19:28:02.586321	Ausstehend	\N	7
9	1	Projekt 1	123456	Herr Kammer	f	f	\N	2024-12-09 09:17:46.05581	Ausstehend	\N	\N
\.


--
-- Data for Name: pruefungsausschuss; Type: TABLE DATA; Schema: public; Owner: user
--

COPY public.pruefungsausschuss (id, joker_antrag_id, unterschrift, bedenken, datum_bearbeitung) FROM stdin;
\.


--
-- Data for Name: studenten; Type: TABLE DATA; Schema: public; Owner: user
--

COPY public.studenten (id, name, vorname, matrikelnummer, fachbereich, studiengang, unterschrift, erstellt_am) FROM stdin;
1	Muster	Max	123456	Informatik	Bachelor	\N	2024-12-07 15:31:10.420923
2	Kaczmarczyk	mARKO	12345	MND	Wirtschaftsinformatik	\N	2024-12-07 16:26:28.048089
\.


--
-- Name: benutzer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public.benutzer_id_seq', 1, true);


--
-- Name: dokumenten_metadaten_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public.dokumenten_metadaten_id_seq', 7, true);


--
-- Name: fachbereich_sekretariat_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public.fachbereich_sekretariat_id_seq', 1, false);


--
-- Name: joker_antraege_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public.joker_antraege_id_seq', 9, true);


--
-- Name: pruefungsausschuss_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public.pruefungsausschuss_id_seq', 1, false);


--
-- Name: studenten_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public.studenten_id_seq', 2, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: benutzer benutzer_email_key; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.benutzer
    ADD CONSTRAINT benutzer_email_key UNIQUE (email);


--
-- Name: benutzer benutzer_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.benutzer
    ADD CONSTRAINT benutzer_pkey PRIMARY KEY (id);


--
-- Name: dokumenten_metadaten dokumenten_metadaten_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.dokumenten_metadaten
    ADD CONSTRAINT dokumenten_metadaten_pkey PRIMARY KEY (id);


--
-- Name: fachbereich_sekretariat fachbereich_sekretariat_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.fachbereich_sekretariat
    ADD CONSTRAINT fachbereich_sekretariat_pkey PRIMARY KEY (id);


--
-- Name: joker_antraege joker_antraege_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.joker_antraege
    ADD CONSTRAINT joker_antraege_pkey PRIMARY KEY (id);


--
-- Name: pruefungsausschuss pruefungsausschuss_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.pruefungsausschuss
    ADD CONSTRAINT pruefungsausschuss_pkey PRIMARY KEY (id);


--
-- Name: studenten studenten_matrikelnummer_key; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.studenten
    ADD CONSTRAINT studenten_matrikelnummer_key UNIQUE (matrikelnummer);


--
-- Name: studenten studenten_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.studenten
    ADD CONSTRAINT studenten_pkey PRIMARY KEY (id);


--
-- Name: benutzer benutzer_student_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.benutzer
    ADD CONSTRAINT benutzer_student_id_fkey FOREIGN KEY (student_id) REFERENCES public.studenten(id);


--
-- Name: fachbereich_sekretariat fachbereich_sekretariat_joker_antrag_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.fachbereich_sekretariat
    ADD CONSTRAINT fachbereich_sekretariat_joker_antrag_id_fkey FOREIGN KEY (joker_antrag_id) REFERENCES public.joker_antraege(id);


--
-- Name: joker_antraege joker_antraege_dokumenten_metadaten_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.joker_antraege
    ADD CONSTRAINT joker_antraege_dokumenten_metadaten_id_fkey FOREIGN KEY (dokumenten_metadaten_id) REFERENCES public.dokumenten_metadaten(id);


--
-- Name: joker_antraege joker_antraege_student_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.joker_antraege
    ADD CONSTRAINT joker_antraege_student_id_fkey FOREIGN KEY (student_id) REFERENCES public.studenten(id);


--
-- Name: pruefungsausschuss pruefungsausschuss_joker_antrag_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.pruefungsausschuss
    ADD CONSTRAINT pruefungsausschuss_joker_antrag_id_fkey FOREIGN KEY (joker_antrag_id) REFERENCES public.joker_antraege(id);


--
-- PostgreSQL database dump complete
--

