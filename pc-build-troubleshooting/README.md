# PC Build
- Goal: Get the computer started and get into the BIOS so I, in another lab be able to setup an OS

## Components (initial, will become more the longer further down the lab we go...)
* CPU: AMD Ryzen 5 5500
* Motherboard: ASUS ROG STRIX X370-F GAMING
* CPU Cooler: Zalman CNPS9X Performa Plus
* RAM: DDR4 HyperX Fury
* Case: Phanteks Eclipse G370A (includes intake fans)
* PSU: ASUS TUF Gaming 750W (Gold, modular)

## Method

### 1. Building phase
* Put on my antistatic strap and clipped it to the chassis.
* Screwed the motherboard into the chassis.
* Installed the RAM in dual-channel configuration (slots A2 & B2):

  <img width="450" height="176" alt="RAM slots A2 and B2" src="https://github.com/user-attachments/assets/ae844dde-18ff-4c7d-9366-38731ad5ee99" />

* Installed the CPU and CPU fan (thermal paste applied beforehand) onto the motherboard.
* Mounted two SATA drives in the back of the chassis and connected them to the motherboard via SATA cables.
* Working out which front panel header each connector belongs to was a challenge until I found the correct [motherboard manual](https://rog.asus.com/se/motherboards/rog-strix/rog-strix-x370-f-gaming-model/helpdesk_manual/) — *(replace with the direct manual page/PDF; the old link was a signed URL that will expire)*.
* Connected every front panel connector (e.g. the chassis fan cable to the CHA_FAN1 header) except the RGB header, since this motherboard doesn't have one — not a concern since this is just a lab machine.
* Wired up the PSU: 24-pin main power, CPU power, PCIe power, and SATA power cables.
* Seated each power cable in its correct connector on the motherboard: 24-pin main power to the 24-pin connector, CPU power to EATX12V, and 2x SATA power to the SSDs at the back of the chassis.

### 2. First boot attempt
Expected a splash screen prompting "Press DEL or F2 to enter BIOS" — instead, nothing displayed.

Checked the CPU spec sheet and confirmed the Ryzen 5 5500 has no integrated graphics, which explained the blank screen since I'd plugged the HDMI cable into the motherboard with no GPU installed.

* Installed a GTX 1050 Ti in a PCIe slot and connected its PCIe power cable, then tried again — still no display.
* All the motherboard lighting came on, so I assumed it would work now that a GPU was installed, but it still didn't. My Steelseries mouse and Xtrfy keyboard didn't light up when plugged in, but a different mouse/keyboard (Mission SG) did. I initially suspected a power delivery issue, or that the motherboard itself was dead (it had been stored poorly for years).
* On closer inspection, the POST diagnostic LEDs weren't lighting up at all when powering on — meaning POST wasn't even starting. This still pointed toward a dead motherboard, since every power cable was seated correctly, the CPU was seated properly, and the board was clearly receiving power (lights on, confirming the PSU was fine).
* Further research turned up the actual cause: the Ryzen 5 5500 wasn't supported by the board's old BIOS firmware, which prevented BIOS from initializing — hence no POST and no diagnostic LEDs.

**Possible fixes:**
1. **BIOS flashback** — not supported on this motherboard.
2. **Drop to a Ryzen 3/4-series CPU** temporarily, since those are supported by the old firmware, then update the BIOS and swap back to the Ryzen 5 5500. *(Chosen approach.)*

### 3. Resolution
* Borrowed a Ryzen 3 CPU and installed it in place of the Ryzen 5 5500. This time all the POST diagnostic LEDs lit in sequence, settling on a solid green "Boot" LED. The screen displayed "Press DEL or F2 to enter BIOS" — pressing F2 and waiting ~2 minutes got me into the BIOS.
* Downloaded the [latest BIOS firmware](https://rog.asus.com/se/motherboards/rog-strix/rog-strix-x370-f-gaming-model/helpdesk_bios/) for this motherboard, extracted it, and ran `BIOSRenamer.exe` to rename the `.CAP` file to the name EZ Flash expects.
* Formatted a USB drive as FAT32 and copied the renamed firmware folder onto it.
* Booted back into BIOS, went to the **Tool** tab, selected **EZ Flash**, and flashed from the USB drive. Left it to run and came back to a successful update.
* Reinstalled the Ryzen 5 5500. Now "Press DEL or F2 to enter BIOS" displayed, but neither key did anything — including after swapping the keyboard's USB port.
* After a round of troubleshooting (reseating components, trying another keyboard, etc.), I unplugged one of the SATA cables from its interface — and BIOS entry worked immediately. That was the actual goal of this lab.
