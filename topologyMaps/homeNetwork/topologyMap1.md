## Purpose
To create a logical topology map of my home network and use it to identify what might be blocking full link rate, such as bad cabling, outdated switches, or misconfiguration.

## Process
Starting at the ONT, I followed the cable from the ONT to the router and noted the cable category. I then continued mapping every connection from the router down to each switch and endpoint, recording the cable speed rating and the maximum supported speed of each switch along the way.

When I reached the server labeled **(6)**, I noticed the switch's link light was orange on that specific connection, indicating the link was capped at 100Mbps (100Base-TX) instead of running at 1000Base-T like the rest of the network.

## Root Cause & Fix
The problem was on the Cat 5e-labeled cable connecting server **(6)** to the switch.

I started by checking the cable which was labeled Cat 5e, should support 1000Base-T. I also confirmed both NICs (the server's and the switch's) supported 1000Base-T. At this point I was confused, and started suspecting some kind of NIC or network configuration inside the Proxmox VM itself was capping the link. I dug through Proxmox network settings and found nothing that explained it.

After some searching, I learned that mislabeled cables are a known issue, so I cut the cable open to check and found... Only 2 twisted pairs inside, probably cat 3 rather than Cat 5e. This was the root cause: **1000Base-T requires all 4 pairs** to negotiate a gigabit link, while 100Base-TX only uses 2 pairs. A 2-pair cable will still link up, but silently caps the connection at 100Mbps instead of failing outright, which is exactly the symptom I saw.

<img width="500" height="500" alt="2436" src="https://github.com/user-attachments/assets/e45af01b-4154-47fe-85ca-4155c855ecde" />
<img width="500" height="500" alt="2435" src="https://github.com/user-attachments/assets/4a284d2f-c663-4d54-bf6c-512b36a0dbc9" />


I replaced the cable with a proper Cat 6 cable and the connection immediately negotiated 1000Base-T.

<img width="908" height="538" alt="Topology map showing the affected connection at (6)" src="https://github.com/user-attachments/assets/3f375d1c-2787-4543-8a22-9a20a4dc723d" />

**Current topology after the fix (all links running at expected speed):**

<img width="388" height="366" alt="Updated topology at 1000Base-T" src="https://github.com/user-attachments/assets/09decdec-0f43-48aa-839f-5db95e957a25" />

## Key Takeaway
A cable's printed label isn't always reliable when troubleshooting unexpected speed caps, physically verifying the cable (pair count, category markings) should be part of the process, especially with cheaper or unbranded cables.
