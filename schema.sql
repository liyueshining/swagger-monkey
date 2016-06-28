drop table if exists urlinfos;
create table urlinfos (
  key integer primary key autoincrement,
  title text not null,
  url text not null,
  description text,
  vote integer default 0
);