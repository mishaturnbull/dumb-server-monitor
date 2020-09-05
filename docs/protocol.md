# Dumb Server Monitor Network Protocol

This is not specified in any RFCs. :)

TCP connections should be established by the client to the server.  Data will be sent
in chunks no longer than 1024 bytes.

Valid data fields is as follows:

| Field    | Min Size | Max Size|
| -------- | ------------ | ------- |
| Flag | 1 byte | 1 byte |
| Client name | 1 byte | 32 bytes |
| Transmission timestamp | 4 byte | 8 byte |
| Time + password hash | 0 bytes | 64 bytes |

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

The program transmits a hashed combination of the client name field and the
has of the password set in the config file.  The hash is generated as follows:

1. The password is encoded in ascii and stripped of leading/trailing whitespace
2. The password is hashed with SHA256.  This hash is stored temporarily.
3. The transmission timestamp is converted to a string and concatenated with the hash from step 2.
4. The string from step 3 is hashed with SHA256.

