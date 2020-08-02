create table Comments
(
    Id int identity
        constraint Comments_pk
            primary key nonclustered,
    Text nvarchar(max) not null,
    Label nvarchar(100),
    Аssessment int not null
)
go

create unique index Comments_Id_uindex
    on Comments (Id)
go

