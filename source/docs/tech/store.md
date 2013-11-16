---
layout: page
navbar: Docs
no_header: true
footer: false
---

# FogCloud File Store and Sync Protocol

## Basic Idea

Each user has a set of devices that synchronize various shared directories
or other data ("shares").

These devices can be trusted or untrusted. Trusted devices get unencrypted
data and secret keys, untrusted devices see only encrypted data and public
keys. 

Each user needs to track two keys:

 - Their "secret master key" which allows them to specify new trusted
   devices.
 - Their public key, to be shared with other users.

In order to simplify adding devices, the configuration of the set of
synchronized devices is stored in the DHT. This is called the SyncConfig.

## Cryptographic Primitives

The Box primitive from DJB et al's NaCl library is used as the primary
mechanism to encrypt and authenticate messages and data. This provides the
semantics of public+secret key encryption and MAC authentication.

 - http://nacl.cr.yp.to/box.html 
 - http://godoc.org/code.google.com/p/go.crypto/nacl/box

The NaCL Secretbox primitive is used to encrypt user SyncConfig.

HMAC-SHA256 is used for secure deterministic generation of IVs and file names.

### User Keys

Each user has a "Box" keypair, used as the primary mechanism for user
authentication.

Each user has a 128-bit "secret master key" that's used to add new trusted
devices to their FogSync setup. SHA256 is used to generate several
deterministic values that are used for restore info:
 
 - The DHT key where the SyncConfig is stored. 
 - The Twofish key that encrypts the SyncConfig.
 - The HMAC key to verify the SyncConfig.

### Device Keys

Each device has a "Box" keypair. This is used as the primary mechanism for
securing communication between devices.

### Share Keys

Each share has a "Box" keypair, used to encrypt and authenticate files.

Each share has a HMAC-SHA512 key, used to generate IVs and file names.

## Initial Setup

### New User

A user starts setting up FogSync on a single device, and then adds additional
devices later. This must be a trusted device.

The device:

 - Generates User Key
 - Generates Restore Key
 - Generates Device Key
 - For each share, generates share keys

### New Trusted Device

Once a user has at least one device set up with FogSync, they can add additional
devices.

To add a trusted device:

 - The user enters their "secret master key".
 - The device looks up the user's SyncConfig in the DHT.
 - The device adds itself to the SyncConfig.

### New Untrusted Device

Once a user has a trusted device set up with FogSync, they can add untrusted devices.

To add an untrusted device:

 - The user enters the address and key for the untrusted device into a
   trusted device.
 - The trusted device adds the untrusted device to the restore info.



Each syncing device is

 - Either trusted or untrusted. Untrusted devices should never see
   unencrypted data.
 - Either archiving or not archiving. Devices that are archiving
   store old versions of files in an archive.



