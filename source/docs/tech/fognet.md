---
layout: page
navbar: Docs
no_header: true
footer: false
---

# FogNet: FogCloud Network Protocal

FogNet is a network protocal that allows hosts running FogSync to communicate
with each other. This includes operations for DHT and file sync.

## Transports

FogNet supports direct communication via both TCP and UDP, as well as indirect
communication via the FogNet mesh network. This is nessisary to handle all of
the cases for NATing firewalls, IPv4 vs. IPv6 hosts, and transport over TOR.

## Basic Concepts

FogNet allows communication between hosts on the internet that may have
changing IP addresses and/or be behind restrictive firewalls by using a DHT to
store mappings between public crytographic IDs and current network location and
providing a P2P mesh network that helps establish connections and potentially
even relay data.

Each person who uses FogNet has a cryptographic key pair to identify themselves.
The SHA256 hash of the public key is called the Person ID. 

Each host on FogNet has a crytographic key pair, and the hash of the public key
is used as a network identifier. The SHA256 hash of the public key is called the
Host ID.

Each host that is currently actively connected to the network also has a
temporary Mesh ID that determines its routing position in the network. This
Mesh ID is generated using a moderately expensive proof of work function and
must be regenerated periodically - this is to make Sybil attacks on the
network harder.

The mappings between Person to Hosts and Host to Mesh ID are stored in a DHT.

FogNet does a couple of basic things:

 - Maintains the mesh and DHT.
 - Provides high level communication functionality between hosts on the network.

## Mesh Routing

High level routing in FogNet takes place between Host IDs.

Each host maintains a table of other active hosts on the network, such that

 - There's a good distribution across the NodeID space.
 - The standard DHT bucket distribution is covered.

