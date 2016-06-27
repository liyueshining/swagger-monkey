drop table if exists urlinfos;
create table urlinfos (
  key integer primary key autoincrement,
  title string not null,
  url string not null,
  description sting,
  vote integer
);