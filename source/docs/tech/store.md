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

FogSync is specified primarily based on the primitives from DJB et al's NaCl
library. In addition, HMAC-SHA256 is abused in a couple of ways that are
hopefully secure.

 - http://nacl.cr.yp.to
 - http://godoc.org/code.google.com/p/go.crypto/nacl

The NaCl Box primitive is used as the primary mechanism to encrypt and authenticate
messages and data. This provides the semantics of public+secret key encryption
and MAC authentication.

The NaCl Secretbox primitive is used to encrypt user SyncConfig.

XSalsa20 is used for data block encryption.

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

Each share has an XSalsa20 key, used to encrypt share data. 
Each share has a HMAC-SHA512 key, used to generate IVs and file names.

## Data Layouts

### SyncConfig

The following information is stored as encrypted gzipped JSON:

 - User "Box" keypair.
 - A list of devices with public key, trust status, and address.
 - A list of shares, with share keys.

### Share Metadata

For each share, each device stores the following information:

 - For each file, the history of all HMACs and timestamps.

### Archive Data

For each share, each archiving device stores old versions of each
file in a store directory by their HMAC code.

This archive is trimmed based on various heuristics to conserve
disk space.

### Untrusted Store

Data and metadata are stored encrypted.

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
 - The trusted device adds the untrusted device to the SyncConfig.
 - The trusted device gives the device list (public key, address) to
   the untrusted device.

## Sync Protocol Scenarios

### File Updated Locally

When a file changes locally, the FogSync client performs the following
procedure:

 - Copy the file to cache.
 - Gzip it.
 - Construct a HMAC-SHA256 tree of 64k blocks.
 - Encrypt the blocks with XSalsa20 (iv = block HMAC)
 - Broadcast an update event.
 - Send the file to an untrusted device, if any. 

### Got an Update Event

 - Download the file.
 - If the existing version hasn't changed, copy in the new version.
 - Else, conflict!

### Data Request

### Data

## Sync Protocol

### Event Log



