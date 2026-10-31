# DNS Server Installation (BIND9)

Setting up a local authoritative + caching DNS server with BIND9 on Linux, placed in the Management VLAN.

> The IP addresses, VLAN numbers and domain names below are from my network. Replace them with yours.

## 1. Plan where it will sit on the network

- Management VLAN (99), IP address `10.0.0.29/28`
- Maybe create a dedicated "Services" VLAN for proper segmentation (opening port 53 from every VLAN into Management weakens the segmentation)

## 2. Firewall configuration (ACLs)

Other VLANs must be able to reach the DNS server on UDP/53, and the server must be able to reach its forwarders.

These are the filter ACLs on my router's virtual interfaces (router-on-a-stick), all applied **inbound**. Add the first rule for every VLAN once the DNS server is ready.

```
! Clients -> DNS server (repeat per VLAN, adjust source network)
permit udp 10.0.0.0 0.0.0.15 host 10.0.0.29 eq 53

! DNS server -> clients (replies)
permit udp host 10.0.0.29 eq 53 10.0.0.0 0.0.0.15

! DNS server -> forwarders
permit udp host 10.0.0.29 host 1.1.1.1 eq 53
permit udp host 10.0.0.29 host 9.9.9.9 eq 53

! TCP fallback for larger DNS responses
permit tcp host 10.0.0.29 host 1.1.1.1 eq 53
permit tcp host 10.0.0.29 host 9.9.9.9 eq 53
```

## 3. Install BIND9

```bash
sudo apt update
sudo apt install bind9 bind9utils bind9-doc
```

## 4. Define the zone

All BIND files live in `/etc/bind/`.

```bash
cd /etc/bind/
sudo nano named.conf.local
```

`named.conf.local` contains all the DNS zones you want on your network. A **zone** is the domain the DNS server is responsible for, in this case `abbe.home.arpa`.

```
zone "abbe.home.arpa" {
    type primary;
    file "/etc/bind/db.abbe.home.arpa";
};
```

- `type primary` = this server holds the authoritative copy of the zone (a `secondary` would replicate from a primary)
- `file` = where the database of DNS records is stored

## 5. Create the zone file

```bash
sudo nano /etc/bind/db.abbe.home.arpa
```

This file defines how the server answers for this zone. It starts with the **SOA record**, which holds the parameters for the zone.

```
$TTL 300    ; how long clients cache records (seconds)
@   IN  SOA dns1.abbe.home.arpa. admin.abbe.home.arpa. (
            1       ; serial - increase on every change
            3600    ; refresh - only matters with a secondary server
            900     ; retry   - only matters with a secondary server
            604800  ; expire  - only matters with a secondary server
            300 )   ; negative TTL - how long "doesn't exist" is cached

; dns1.abbe.home.arpa. is the primary name server for the zone
; admin.abbe.home.arpa. is the admin's email, the first "." stands for "@"
; so this means admin@abbe.home.arpa

@       IN  NS  dns1.abbe.home.arpa.
dns1    IN  A   10.0.0.29
proxmox IN  A   10.0.0.30
```

- `@` = shorthand for the zone name (`abbe.home.arpa`)
- `NS` = Name Server record, "which host is the name server for this zone?"
- `A` = Address record, maps a hostname to an IPv4 address
- **The trailing dot matters.** `dns1.abbe.home.arpa.` is a complete name. Without the dot, the zone name is appended and you get `dns1.abbe.home.arpa.abbe.home.arpa`.
- Comments in zone files start with `;`, not `#`.
- Tip: a serial in the format `YYYYMMDDNN` (e.g. `2026103101`) makes it easy to see when a change was made.

## 6. Configure the server options

```bash
sudo nano /etc/bind/named.conf.options
```

```
options {
    directory "/var/cache/bind";
    listen-on { 10.0.0.29; 127.0.0.1; };
    allow-query { localhost; 10.0.0.0/24; };
    allow-recursion { localhost; 10.0.0.0/24; };
    forwarders { 1.1.1.1; 9.9.9.9; };
};
```

| Option | Meaning |
|---|---|
| `directory` | BIND's working directory |
| `listen-on` | Which addresses BIND listens on |
| `allow-query` | Who may ask BIND anything |
| `allow-recursion` | Who BIND will resolve external names for |
| `forwarders` | Where to send queries the local server doesn't know the answer to |

## 7. Test the configuration

Check the config files and the zone file (they are checked by different tools):

```bash
sudo named-checkconf
sudo named-checkzone abbe.home.arpa /etc/bind/db.abbe.home.arpa
```

Then test from another computer (on that VLAN, or once the firewall rules are in place):

```bash
dig @10.0.0.29 proxmox.abbe.home.arpa   # local record
dig @10.0.0.29 example.com              # recursion via forwarders
```

`nslookup` works as well (windows).

## 8. Restart and enable the service

```bash
sudo systemctl restart bind9
sudo systemctl enable bind9
```

## 9. Finish up

- Apply the ACL rules from step 2
- Assign the DNS server in the router's DHCP configuration so clients use it automatically

## What I learned

- `.local` is reserved for mDNS (Multicast DNS), so don't use it as a local domain. Use `home.arpa` (RFC 8375), for example `abbe.home.arpa`.
- Zone = the domain the DNS server is responsible for
- Different record types (`SOA`, `NS`, `A`) and what they do
- Forwarder = where to send a query when the server doesn't know the IP for that hostname
- Zone files need the trailing dot on full names, and use `;` for comments
- `named-checkconf` checks config files, `named-checkzone` checks zone files
