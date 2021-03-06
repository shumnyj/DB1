PGDMP     '                    w           testpost    10.6    11.2     �
           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                       false            �
           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                       false            �
           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                       false            �
           1262    24576    testpost    DATABASE     �   CREATE DATABASE testpost WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'Russian_Ukraine.1251' LC_CTYPE = 'Russian_Ukraine.1251';
    DROP DATABASE testpost;
             postgres    false            �
           0    0    DATABASE testpost    COMMENT     *   COMMENT ON DATABASE testpost IS 'lab db';
                  postgres    false    2814                        0    0    DATABASE testpost    ACL     +   GRANT ALL ON DATABASE testpost TO shumnyj;
                  postgres    false    2814            �            1259    24586    authors    TABLE     �   CREATE TABLE public.authors (
    fname character varying(32) NOT NULL,
    sname character varying(32) NOT NULL,
    exp integer,
    written integer,
    publisher character varying(64)
);
    DROP TABLE public.authors;
       public         shumnyj    false            �            1259    24578    books    TABLE     �   CREATE TABLE public.books (
    title character varying(64),
    pages integer,
    barcode integer NOT NULL,
    printing boolean,
    author_fname character varying(32),
    author_sname character varying(32),
    pub character varying(64)
);
    DROP TABLE public.books;
       public         shumnyj    false            �            1259    24583 
   publishers    TABLE     �   CREATE TABLE public.publishers (
    pname character varying(64) NOT NULL,
    address character varying(100),
    publ integer,
    director character varying(64)
);
    DROP TABLE public.publishers;
       public         shumnyj    false            �
          0    24586    authors 
   TABLE DATA               H   COPY public.authors (fname, sname, exp, written, publisher) FROM stdin;
    public       shumnyj    false    198   �       �
          0    24578    books 
   TABLE DATA               a   COPY public.books (title, pages, barcode, printing, author_fname, author_sname, pub) FROM stdin;
    public       shumnyj    false    196   U       �
          0    24583 
   publishers 
   TABLE DATA               D   COPY public.publishers (pname, address, publ, director) FROM stdin;
    public       shumnyj    false    197   �       y
           2606    24590    authors authors_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.authors
    ADD CONSTRAINT authors_pkey PRIMARY KEY (fname, sname);
 >   ALTER TABLE ONLY public.authors DROP CONSTRAINT authors_pkey;
       public         shumnyj    false    198    198            u
           2606    24582    books book_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.books
    ADD CONSTRAINT book_pkey PRIMARY KEY (barcode);
 9   ALTER TABLE ONLY public.books DROP CONSTRAINT book_pkey;
       public         shumnyj    false    196            w
           2606    24592    publishers publishers_pkey 
   CONSTRAINT     [   ALTER TABLE ONLY public.publishers
    ADD CONSTRAINT publishers_pkey PRIMARY KEY (pname);
 D   ALTER TABLE ONLY public.publishers DROP CONSTRAINT publishers_pkey;
       public         shumnyj    false    197            z
           2606    24593    books author    FK CONSTRAINT     �   ALTER TABLE ONLY public.books
    ADD CONSTRAINT author FOREIGN KEY (author_sname, author_fname) REFERENCES public.authors(sname, fname) MATCH FULL;
 6   ALTER TABLE ONLY public.books DROP CONSTRAINT author;
       public       shumnyj    false    196    196    2681    198    198            {
           2606    24603    books book_pub_fkey    FK CONSTRAINT     v   ALTER TABLE ONLY public.books
    ADD CONSTRAINT book_pub_fkey FOREIGN KEY (pub) REFERENCES public.publishers(pname);
 =   ALTER TABLE ONLY public.books DROP CONSTRAINT book_pub_fkey;
       public       shumnyj    false    197    2679    196            |
           2606    24598    authors publisher    FK CONSTRAINT     �   ALTER TABLE ONLY public.authors
    ADD CONSTRAINT publisher FOREIGN KEY (publisher) REFERENCES public.publishers(pname) MATCH FULL;
 ;   ALTER TABLE ONLY public.authors DROP CONSTRAINT publisher;
       public       shumnyj    false    198    2679    197            �
   K   x�=�1
�@D�zr��s�[Y���!�j���5oś�ܱTF��ܡ��bK��Ë=�� K����/ʹ����      �
   b   x�u�;
�0��zr��F����m����$X
����X!��`,X�i�W�).���CEe�bC�Ɋ��������=̌^S��4%�q�s�M(:      �
   )   x�+0�LL)2�440�L�,2�*0	q����b���� ��	     