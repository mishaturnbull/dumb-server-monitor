# Dumb Server Monitor Network Protocol

This is not specified in any RFCs. :)

TCP connections should be established by the client to the server.  Data will be sent
in chunks no longer than 1024 bytes.

Valid data fields is as follows:

| Field    | Min Size | Max Size|
| -------- | ------------ | ------- |
| Flag | 1 byte | 1 byte |
| Client name | 1 byte | 32 bytes |
| Password (hashed) | 0 bytes | 64 bytes |

Fields should be separated by a single `\x1e` character.

## Flag

Determines the message type.

| Character | Meaning |
| --------- | ------- |
| `\x11`    | Regular client-server update message. |
| `\x12`    | Output over network (if enabled) |
| `\x13`    | Output to file (if enabled) |

If the flag is `\x11`, the rest of the fields are parsed as normal.
Otherwise, the remaining fields are discarded.

## Client name

A string that is assigned to this client.  For best results, make this unique among 
all the clients.  May contain any ASCII character numbered 32 and up.

## Password (hashed)

Program transmits the SHA256 hash of the set password.  If no password, sends
an empty field.  If password, sends a SHA256 hash.