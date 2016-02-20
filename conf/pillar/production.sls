#!yaml|gpg

environment: production

domain: pcs.rochapps.com

repo:
  url: git@github.com:rochapps/pcs.git
  branch: master

# Addtional public environment variables to set for the project
env:
  FOO: BAR

# Uncomment and update username/password to enable HTTP basic auth
# Password must be GPG encrypted.
http_auth:
  "admin": |-
    -----BEGIN PGP MESSAGE-----
    Version: GnuPG v1.4.11 (GNU/Linux)

    hQEMA2HmQDqv0piHAQgAwz1mhQ5XraQKgSxL9Xw9vQptV4IYxKf2jQVAb1RlP5qm
    hq0tZIUr8EG3iO3Gr4D28qkDtTbmTNVJ4m5YM5Q65TMd4t8rhUtuJlB6355m2Fae
    VFwXY9/fp6sPtRSEq1AvonBWiy48fHQP4IQtpYJF8d9bUqUhFgliXs/tDNwi8x4P
    Lk2wEUynCA3YjuNeLbRWZs7e7C9mquweMDVvJNsbbjk08xANhjIBJpmvH61gS74k
    9I8NjXMw5gXFyQPo6fnveSITjnqygdsLAQnMto2WN/7fM7vUaNj0aDJdtukxNb46
    mF7Hz5v5AUeE/ZsGV/sQFwbIxbkO3fyqwxrfaBsDT9JBAeh2mHndY62vhnaWMloo
    BqiobsEJ25hc96zXs9N9D6FVIjhHoBDhQD1qSlQaykFm75BuEXsuJa0mx6AChXLp
    rUQ=
    =KZvC
    -----END PGP MESSAGE-----

# Private environment variables.
# Must be GPG encrypted.
secrets:
  "SECRET_KEY": |-
    -----BEGIN PGP MESSAGE-----
    Version: GnuPG v1.4.11 (GNU/Linux)

    hQEMA2HmQDqv0piHAQf9Fv3i5STGYT8riXD+/0M3RZE5V62d602liGD1uqIfKxoa
    n7GAZPMzym1rGrK1noyGZyBOLSXgy7WHXuKfPWXHCk2/aemcw+UmfpEfU0VhopN2
    43wV9chjtVO5vEmK8ONID1FTb8nb0VsZxWPnIwUN8rYBnhv8Bl6AruBOjMB7Js+T
    dO98FUNXwa/4K7mqdRu5ErYszRxzh17j9h1CKzJBqInUyul0fTU9r+Di3sfYfkyN
    Ppe5yvVukKGG0X/wdWxey+s5KOv/LBn2tRTt0Rjh1dEfmoPDte0+C8B+dsXuV+Qh
    ULzdjxHJLwxkmWZtU8C0UC/gXxy8P57XVfaGjAt3ptJ7AWyu/FoE7B8EWjZdRsYj
    Iz8l4YzD5UuZ3EPfzZKmS3dwQRacg38N+abFfjLWvTiBPjtM+0itRt8Ju6Eybylf
    Av1jkRt+umteVN9q6gQg1tSEB3WKxrg5Ap3YkG0nsUN0mhSe4zULuvVPApjsUSFo
    fcB7Gfn4QXFK9Sqm
    =t9wu
    -----END PGP MESSAGE-----

# Private deploy key. Must be GPG encrypted.
github_deploy_key: |-
  -----BEGIN PGP MESSAGE-----
  Version: GnuPG v1.4.11 (GNU/Linux)

  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
  =0XaT
  -----END PGP MESSAGE-----

# Uncomment and update ssl_key and ssl_cert to enabled signed SSL/
# Must be GPG encrypted.
# {% if 'balancer' in grains['roles'] %}
# ssl_key: |-
#    -----BEGIN PGP MESSAGE-----
#    -----END PGP MESSAGE-----
#
# ssl_cert: |-
#    -----BEGIN PGP MESSAGE-----
#    -----END PGP MESSAGE-----
# {% endif %}
