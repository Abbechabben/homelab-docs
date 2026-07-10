# PC Build
- Goal: Get the computer started and get into the BIOS so I can, in another lab, set up an OS.

## Components (initial; will grow as we go further into the lab)
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
* Working out which front panel header each connector belongs to was a challenge until I found the correct [motherboard manual](https://rog.asus.com/se/motherboards/rog-strix/rog-strix-x370-f-gaming-model/helpdesk_manual/).
* Connected every front panel connector (e.g. the chassis fan cable to the CHA_FAN1 header) except the RGB header, since this motherboard doesn't have one (not a concern since this is just a lab machine).
* Wired up the PSU: 24-pin main power, CPU power, PCIe power, and SATA power cables.
* Seated each power cable in its correct connector on the motherboard: 24-pin main power to the 24-pin connector, CPU power to EATX12V, and 2x SATA power to the SSDs at the back of the chassis.

### 2. First boot attempt
Expected a splash screen prompting "Press DEL or F2 to enter BIOS." Instead, nothing displayed.

Checked the CPU spec sheet and confirmed the Ryzen 5 5500 has **no integrated graphics**, which explained the blank screen since I'd plugged the HDMI cable into the motherboard with no GPU installed.

* **Installed a GTX 1050 Ti** in a PCIe slot and connected its PCIe power cable, then tried again. Still no display.
* All the motherboard lighting came on, so I assumed it would work now that a GPU was installed, but it still didn't. My SteelSeries mouse and Xtrfy keyboard didn't light up when plugged in, but a different mouse/keyboard (Mission SG) did. I initially suspected a power delivery issue, or that the motherboard itself was dead (it had been stored poorly for years).
* On closer inspection, the **POST diagnostic LEDs weren't lighting up at all** when powering on, meaning POST wasn't even starting. This still pointed toward a dead motherboard, since every power cable was seated correctly, the CPU was seated properly, and the board was clearly receiving power (lights on, confirming the PSU was fine).
* Further research turned up the actual cause: the **Ryzen 5 5500 wasn't supported by the board's old BIOS firmware**, which prevented BIOS from initializing, hence no POST and no diagnostic LEDs.

#### Root cause
* AGESA/BIOS version too old to recognize the Ryzen 5 5500 CPU, resulting in no POST, no diagnostic LEDs, and no boot.

**Possible fixes:**
1. **BIOS FlashBack.** Not supported on this motherboard (the X370-F Gaming doesn't have a USB BIOS FlashBack port).
2. **Drop to a Ryzen 3/4-series CPU** temporarily, since those are supported by the old firmware, then update the BIOS and swap back to the Ryzen 5 5500. *(Chosen approach.)*

### 3. Resolution
* Borrowed a Ryzen 3 CPU and installed it in place of the Ryzen 5 5500. This time all the POST diagnostic LEDs lit in sequence, settling on a solid green "Boot" LED. The screen displayed "Press DEL or F2 to enter BIOS." Pressing F2 and waiting ~2 minutes got me into the BIOS.
* Downloaded the [latest BIOS firmware](https://rog.asus.com/se/motherboards/rog-strix/rog-strix-x370-f-gaming-model/helpdesk_bios/) for this motherboard, extracted it, and ran `BIOSRenamer.exe` to rename the `.CAP` file to the name EZ Flash expects.
* Formatted a USB drive as FAT32 and copied the renamed firmware folder onto it.
* Booted back into BIOS, went to the **Tool** tab, selected **EZ Flash**, and flashed from the USB drive. Left it to run and came back to a successful update.
* Reinstalled the Ryzen 5 5500. Now "Press DEL or F2 to enter BIOS" displayed, but neither key did anything, including after swapping the keyboard's USB port.
* After a round of troubleshooting (reseating components, trying another keyboard, etc.), I unplugged one of the SATA cables from its interface, and BIOS entry worked immediately. That was the actual goal of this lab.

## Lessons learned
* **Check CPU/BIOS compatibility** before installing a used or old motherboard.
* **USB BIOS FlashBack lets you update firmware without booting into BIOS or having a working CPU installed, but not all motherboards have it** (this one doesn't). Without it, you need a CPU the current firmware already supports just to get into BIOS and flash from there.
* **POST diagnostic LEDs are a useful troubleshooting tool.** Check them to see whether POST is running and, if not, where it's failing. If POST never starts, that can indicate the CPU isn't compatible with the current BIOS.
* **Lights glowing and fans spinning doesn't mean POST completed.** Power delivery and POST are independent; one doesn't require the other.
* **The final SATA-cable fix is still unexplained.** If anyone reading this knows why, please tell me!
