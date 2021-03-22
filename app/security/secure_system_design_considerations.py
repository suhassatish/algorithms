"""
 Give me an example of how you’d secure data so that it cannot be misused or inappropriately accessed.

 Given how much data breaches are in the news, I wanted to set some context. Assuming that there is always a chance
 that someone will get a hold of data that they are not supposed to, I’d like to render the data useless to bad actors.
 I have been studying encryption because this technique allows you to protect data that you store as well as data you
 transport.



My strategy would include:

A good encryption algorithm, properly applied;
Protection of the secret key;
Symmetric keys that are never to be reused;
Public keys to be distributed in a certificate to prevent interception attacks;
Ways to protect metadata


One consideration before we begin - just because the data-sharing channel is cryptographically protected, we shouldn’t
assume that the data can be shared carelessly. Cryptography intercepting proxies do exist and can be used to mine data.

It is exactly for this reason that Encryption keys must be rotated on a regular basis. Cryptographic algorithms are
continually being analyzed and vulnerabilities can be found.



Now, let’s execute our strategy. Since key management is important, let’s dig in there.



Symmetric keys must be carefully protected and good key rotation practices must be followed. Private keys must be
carefully protected.

Public keys must be accessible to anyone and the emphasis is on access, so no protection is needed. Still, they must be
 embedded in a certificate.



Now let's look at the data itself.



Data at rest ideally requires envelope encryption, which means a key hierarchy is established. Never encrypt all data
in a database with the same key.



Data in motion requires the use of HTTPS/TLS. Very sensitive data must still be encrypted—even over an encrypted
connection.



Data being shared with other parties needs to be processed with asymmetric encryption so that only the intended
recipient can read it.



Why this answer worked well:

It tied the need for the solution to real-world events. Engineering is a means to an end, and that context matters.
It laid out the key aspects of the solution at the get go, which is critical.
It looked at the solution through the lens of several aspects. Starting with keys and then moving to data was a smart
call.
"""