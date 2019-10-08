select
  '[' || table.email ||'](https://mail.google.com/mail/?view=cm&fs=1&to=' || replace(table.email,'+'
,'%2B') || '&su=&body=)'