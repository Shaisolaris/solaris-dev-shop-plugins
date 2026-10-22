---
name: network-engineer
description: Network Engineer for Solaris - designs and operates the owner's own multi-system,
  multi-machine network for the dev shop and game studio. Owns network topology (gateway/switch/AP
  roles, IP planning, DHCP/DNS), VLAN segmentation and trust zones, WireGuard VPN,
  Pi-hole / local DNS, self-hosted cluster bring-up (Uncloud), and enterprise router/switch
  ops (Cisco IOS, Netmiko SSH automation, BGP diagnostics, interface health, config
  validation). Use whenever the owner says "network", "homelab", "VLAN", "subnet",
  "segment", "trust zone", "isolate IoT", "guest WiFi", "gateway", "router", "switch",
  "trunk", "access port", "DHCP", "DNS", "Pi-hole", "AdGuard", "Unbound", "home.arpa",
  "WireGuard", "VPN", "split tunnel", "DDNS", "port forward", "self-host cluster",
  "Uncloud", "Caddy", "reverse proxy", "Cisco", "IOS", "ACL", "wildcard mask", "Netmiko",
  "BGP", "peering", "interface errors", "CRC", "duplex mismatch", or "config validation".
---

Load the [Solaris workflow](resources/canonical/employees/infrastructure/network-engineer/SKILL.md) and its mirrored companion resources when this role applies. They retain the pinned canonical source bytes.

For a local Python helper, use the [role entrypoint](scripts/run.py): `python <resolved-entrypoint> <role-relative-helper.py> <arguments>`. Resolve the entrypoint relative to this skill file. It runs the unchanged helper from its original canonical role folder, preserving imports and runtime resources. Use `--context` to locate that original folder for other documented tools or companion paths.

The shared canonical runtime remains at the plugin root; the contained resources are documentation mirrors, not a second runtime. Host tools, permissions, approvals and documented runtime requirements still apply. This layout adds no grants, background jobs or lifecycle hooks.
