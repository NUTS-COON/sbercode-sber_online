create table comment
(
    "Id" serial not null
        constraint comment_pk
            primary key,
    text varchar not null,
    label varchar(100),
    mood integer not null
);

alter table comment owner to postgres;

create unique index comment_id_uindex
    on comment ("Id");

