<h4>Hyperlink to Email - Gmail</h4>


Periscope has a lot of cool functionality around converting links to a simpler format using Markdown language. However, doing things that require more advanced functionality such as bringing up an email takes a little more maneuvering. Luckily, the internet can be a kind place with logic from time to time. From this post:

https://stackoverflow.com/questions/6548570/url-to-compose-a-message-in-gmail-with-full-gmail-interface-and-specified-to-b

We can use this format:

select
  '[' || table.email ||'](https://mail.google.com/mail/?view=cm&fs=1&to=' || replace(table.email,'+'
,'%2B') || '&su=&body=)'


If you're using something other than gmail and find out how to get this working, please post below!

Note: for plus signs, use %2B to replace any + in your email address!