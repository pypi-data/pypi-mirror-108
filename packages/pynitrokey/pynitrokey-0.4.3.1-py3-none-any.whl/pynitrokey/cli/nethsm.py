# -*- coding: utf-8 -*-
#
# Copyright 2021 Nitrokey Developers
#
# Licensed under the Apache License, Version 2.0, <LICENSE-APACHE or
# http://apache.org/licenses/LICENSE-2.0> or the MIT license <LICENSE-MIT or
# http://opensource.org/licenses/MIT>, at your option. This file may not be
# copied, modified, or distributed except according to those terms.

import contextlib
import datetime

import click
import urllib3

import pynitrokey.nethsm

def make_enum_type(enum_cls):
    return click.Choice([variant.value for variant in enum_cls], case_sensitive=False)


DATETIME_TYPE = click.DateTime(formats=["%Y-%m-%dT%H:%M:%S%z"])
ROLE_TYPE = make_enum_type(pynitrokey.nethsm.Role)
LOG_LEVEL_TYPE = make_enum_type(pynitrokey.nethsm.LogLevel)
UNATTENDED_BOOT_STATUS_TYPE = make_enum_type(pynitrokey.nethsm.UnattendedBootStatus)
ALGORITHM_TYPE = make_enum_type(pynitrokey.nethsm.KeyAlgorithm)
MECHANISM_TYPE = make_enum_type(pynitrokey.nethsm.KeyMechanism)
DECRYPT_MODE_TYPE = make_enum_type(pynitrokey.nethsm.DecryptMode)
SIGN_MODE_TYPE = make_enum_type(pynitrokey.nethsm.SignMode)


def print_row(values, widths):
    row = [value.ljust(width) for (value, width) in zip(values, widths)]
    print(*row, sep="\t")


def print_table(headers, data):
    widths = [len(header) for header in headers]
    for row in data:
        for i in range(len(widths)):
            row[i] = str(row[i])
            widths[i] = max(widths[i], len(row[i]))

    print_row(headers, widths)
    print_row(["-" * width for width in widths], widths)
    for row in data:
        print_row(row, widths)


@click.group()
@click.option(
    "-h", "--host", "host", required=True, help="Set the host of the NetHSM API"
)
@click.option(
    "-v",
    "--api-version",
    "version",
    default="v1",
    help="Set the version of the NetHSM API",
)
@click.option("-u", "--username", "username", help="The NetHSM user name")
@click.option("-p", "--password", "password", help="The NetHSM password")
@click.option(
    "--verify-tls/--no-verify-tls",
    default=True,
    help="Whether to verify the TLS certificate of the NetHSM",
)
@click.pass_context
def nethsm(ctx, host, version, username, password, verify_tls):
    """Interact with NetHSM, see subcommands."""
    ctx.ensure_object(dict)

    ctx.obj["NETHSM_HOST"] = host
    ctx.obj["NETHSM_VERSION"] = version
    ctx.obj["NETHSM_USERNAME"] = username
    ctx.obj["NETHSM_PASSWORD"] = password
    ctx.obj["NETHSM_VERIFY_TLS"] = verify_tls

    if not verify_tls:
        urllib3.disable_warnings()


@contextlib.contextmanager
def connect(ctx, require_auth=True):
    host = ctx.obj["NETHSM_HOST"]
    version = ctx.obj["NETHSM_VERSION"]
    username = None
    password = None
    verify_tls = ctx.obj["NETHSM_VERIFY_TLS"]

    if require_auth:
        username = ctx.obj["NETHSM_USERNAME"]
        password = ctx.obj["NETHSM_PASSWORD"]
        if not username:
            username = click.prompt(f"[auth] User name for NetHSM {host}")
        if not password:
            password = click.prompt(
                f"[auth] Password for user {username} on NetHSM {host}", hide_input=True
            )

    with pynitrokey.nethsm.connect(host, version, username, password, verify_tls) as nethsm:
        import urllib3.exceptions

        try:
            yield nethsm
        except pynitrokey.nethsm.NetHSMError as e:
            raise click.ClickException(e)
        except urllib3.exceptions.MaxRetryError as e:
            if isinstance(e.reason, urllib3.exceptions.SSLError):
                raise click.ClickException(f"Could not connect to the NetHSM: {e.reason}\nIf you use a self-signed certificate, please set the --no-verify-tls option.")
            else:
                raise e


@nethsm.command()
@click.argument("passphrase", required=False)
@click.pass_context
def unlock(ctx, passphrase):
    """Bring a locked NetHSM into operational state."""
    with connect(ctx, require_auth=False) as nethsm:
        if not passphrase:
            passphrase = click.prompt(
                f"Unlock passphrase for NetHSM {nethsm.host}", hide_input=True
            )
        nethsm.unlock(passphrase)
        print(f"NetHSM {nethsm.host} unlocked")


@nethsm.command()
@click.pass_context
def lock(ctx):
    """Bring an operational NetHSM into locked state.

    This command requires authentication as a user with the Administrator
    role."""
    with connect(ctx) as nethsm:
        nethsm.lock()
        print(f"NetHSM {nethsm.host} locked")


@nethsm.command()
@click.option(
    "-u",
    "--unlock-passphrase",
    hide_input=True,
    confirmation_prompt=True,
    prompt=True,
    help="The unlock passphrase to set",
)
@click.option(
    "-a",
    "--admin-passphrase",
    hide_input=True,
    confirmation_prompt=True,
    prompt=True,
    help="The admin passphrase to set",
)
@click.option(
    "-t",
    "--system-time",
    type=DATETIME_TYPE,
    help="The system time to set (default: the time of this system)",
)
@click.pass_context
def provision(ctx, unlock_passphrase, admin_passphrase, system_time):
    """Initial provisioning of a NetHSM.

    If the unlock or admin passphrases are not set, they have to be entered
    interactively.  If the system time is not set, the current system time is
    used."""
    if not system_time:
        system_time = datetime.datetime.now(datetime.timezone.utc)
    with connect(ctx, require_auth=False) as nethsm:
        nethsm.provision(unlock_passphrase, admin_passphrase, system_time)
        print(f"NetHSM {nethsm.host} provisioned")


@nethsm.command()
@click.option(
    "--details/--no-details",
    default=True,
    help="Also query the real name and role of the user",
)
@click.pass_context
def list_users(ctx, details):
    """List all users on the NetHSM.

    This command requires authentication as a user with the Administrator
    role."""
    with connect(ctx) as nethsm:
        user_ids = nethsm.list_users()

        print(f"Users on NetHSM {nethsm.host}:")
        print()

        headers = ["User ID"]
        if details:
            headers += ["Real name", "Role"]
            data = []
            for user_id in user_ids:
                user = nethsm.get_user(user_id=user_id.value)
                data.append([user_id, user.real_name, user.role.value])
        else:
            data = [[user_id] for user_id in user_ids]

        print_table(headers, data)


@nethsm.command()
@click.argument("user-id")
@click.pass_context
def get_user(ctx, user_id):
    """Query the real name and role for a user ID on the NetHSM.

    This command requires authentication as a user with the Administrator or
    Operator role."""
    with connect(ctx) as nethsm:
        user = nethsm.get_user(user_id=user_id)
        print(f"User {user_id} on NetHSM {nethsm.host}")
        print(f"Real name:  {user.real_name}")
        print(f"Role:       {user.role.value}")


@nethsm.command()
@click.option("-n", "--real-name", prompt=True, help="The real name of the new user")
@click.option(
    "-r", "--role", type=ROLE_TYPE, prompt=True, help="The role of the new user"
)
@click.option(
    "-p",
    "--passphrase",
    prompt=True,
    hide_input=True,
    confirmation_prompt=True,
    help="The passphrase of the new user",
)
@click.option("-u", "--user-id", help="The user ID of the new user")
@click.pass_context
def add_user(ctx, real_name, role, passphrase, user_id):
    """Create a new user on the NetHSM.

    If the real name, role or passphrase are not specified, they have to be
    specified interactively.  If the user ID is not set, it is generated by the
    NetHSM.

    This command requires authentication as a user with the Administrator
    role."""
    with connect(ctx) as nethsm:
        user_id = nethsm.add_user(real_name, role, passphrase, user_id)
        print(f"User {user_id} added to NetHSM {nethsm.host}")


@nethsm.command()
@click.argument("user-id")
@click.pass_context
def delete_user(ctx, user_id):
    """Delete the user with the given user ID on the NetHSM.

    This command requires authentication as a user with the Administrator
    role."""
    with connect(ctx) as nethsm:
        nethsm.delete_user(user_id)
        print(f"User {user_id} deleted on NetHSM {nethsm.host}")


@nethsm.command()
@click.option("-u", "--user-id", help="The user ID of the user")
@click.option(
    "-p",
    "--passphrase",
    prompt=True,
    hide_input=True,
    confirmation_prompt=True,
    help="The new passphrase of the user",
)
@click.pass_context
def set_passphrase(ctx, user_id, passphrase):
    """Set the passphrase for the user with the given ID (or the current user).

    This command requires authentication as a user with the Administrator or
    Operator role.  Users with the Operator role can only change their own
    passphrase."""
    with connect(ctx) as nethsm:
        if not user_id:
            user_id = nethsm.username
        nethsm.set_passphrase(user_id, passphrase)
        print(f"Updated the passphrase for user {user_id} on NetHSM {nethsm.host}")


@nethsm.command()
@click.pass_context
def info(ctx):
    """Query the vendor and product information for a NetHSM."""
    with connect(ctx, require_auth=False) as nethsm:
        (vendor, product) = nethsm.get_info()
        print(f"Host:    {nethsm.host}")
        print(f"Vendor:  {vendor}")
        print(f"Product: {product}")


@nethsm.command()
@click.pass_context
def state(ctx):
    """Query the state of a NetHSM."""
    with connect(ctx, require_auth=False) as nethsm:
        state = nethsm.get_state()
        print(f"NetHSM {nethsm.host} is {state.value}")


@nethsm.command()
@click.argument("length", type=int)
@click.pass_context
def random(ctx, length):
    """Retrieve random bytes from the NetHSM as a Base64 string.

    This command requires authentication as a user with the Operator role."""
    with connect(ctx) as nethsm:
        print(nethsm.get_random_data(length))


@nethsm.command()
@click.pass_context
def metrics(ctx):
    """Query the metrics of a NetHSM.

    This command requires authentication as a user with the Metrics role."""
    with connect(ctx) as nethsm:
        headers = ["Metric", "Value"]
        data = nethsm.get_metrics()
        print_table(headers, [list(row) for row in sorted(data.items())])


@nethsm.command()
@click.option(
    "--details/--no-details",
    default=True,
    help="Also query the key data",
)
@click.pass_context
def list_keys(ctx, details):
    """List all keys on the NetHSM.

    This command requires authentication as a user with the Administrator or
    Operator role."""
    with connect(ctx) as nethsm:
        key_ids = nethsm.list_keys()

        print(f"Keys on NetHSM {nethsm.host}:")
        print()

        headers = ["Key ID"]
        if details:
            headers += ["Algorithm", "Mechanisms", "Operations"]
            data = []
            for key_id in key_ids:
                key = nethsm.get_key(key_id=key_id.value)
                data.append(
                    [key_id, key.algorithm, ", ".join(key.mechanisms), key.operations]
                )
        else:
            data = [[key_id] for key_id in key_ids]

        print_table(headers, data)


@nethsm.command()
@click.argument("key_id")
@click.option("--public-key", is_flag=True, help="Query the public key as a PEM file")
@click.pass_context
def get_key(ctx, key_id, public_key):
    """Get information about a key on the NetHSM.

    This command requires authentication as a user with the Administrator or
    Operator role."""
    with connect(ctx) as nethsm:
        if public_key:
            print(nethsm.get_key_public_key(key_id))
        else:
            key = nethsm.get_key(key_id)
            mechanisms = ", ".join(key.mechanisms)
            print(f"Key {key_id} on NetHSM {nethsm.host}:")
            print(f"Algorithm:       {key.algorithm}")
            print(f"Mechanisms:      {mechanisms}")
            print(f"Operations:      {key.operations}")
            print(f"Modulus:         {key.modulus}")
            print(f"Public exponent: {key.public_exponent}")


@nethsm.command()
@click.argument("key-id")
@click.pass_context
def delete_key(ctx, key_id):
    """Delete the key pair with the given key ID on the NetHSM.

    This command requires authentication as a user with the Administrator
    role."""
    with connect(ctx) as nethsm:
        nethsm.delete_key(key_id)
        print(f"Key {key_id} deleted on NetHSM {nethsm.host}")


def prompt_mechanisms(algorithm):
    available_mechanisms = []
    print("Supported mechanisms for this algorithm:")
    for mechanism in pynitrokey.nethsm.KeyMechanism:
        if mechanism.value.startswith(algorithm):
            available_mechanisms.append(mechanism.value)
            print(f"  {mechanism.value}")

    print("Please enter at least one mechanism.  Enter an empty string to "
          "finish the list of mechanisms.")

    mechanism_type = click.Choice(available_mechanisms, case_sensitive=False)
    mechanisms = []
    cont = True
    while cont:
        default = None
        prompt = "Add mechanism"
        if mechanisms:
            prompt += " (or empty string to continue)"
            default = ""
        mechanism = click.prompt(
            prompt,
            type=mechanism_type,
            default=default,
            show_choices=False,
            show_default=False,
        )
        if mechanism:
            mechanisms.append(mechanism)
        else:
            cont = False

    if not mechanisms:
        raise click.ClickException("No key mechanisms selected!")

    return mechanisms


@nethsm.command()
@click.option(
    "-a",
    "--algorithm",
    type=ALGORITHM_TYPE,
    prompt=True,
    help="The algorithm for the new key",
)
@click.option(
    "-m",
    "--mechanism",
    "mechanisms",
    type=MECHANISM_TYPE,
    multiple=True,
    help="The mechanisms for the new key",
)
@click.option(
    "-p",
    "--prime-p",
    help="The prime p for RSA keys",
)
@click.option(
    "-q",
    "--prime-q",
    help="The prime q for RSA keys",
)
@click.option(
    "-e",
    "--public-exponent",
    help="The public exponent for RSA keys",
)
@click.option(
    "-d",
    "--data",
    help="The key data for ED25519 or ECDSA_* keys",
)
@click.option(
    "-k",
    "--key-id",
    help="The ID of the new key",
)
@click.pass_context
def add_key(ctx, algorithm, mechanisms, prime_p, prime_q, public_exponent, data, key_id):
    """Add a key pair on the NetHSM.

    If the key ID is not set, it is generated by the NetHSM.

    This command requires authentication as a user with the Administrator
    role."""
    mechanisms = list(mechanisms) or prompt_mechanisms(algorithm)

    if algorithm == "RSA":
        if data:
            raise click.ClickException("-d/--data must not be set for RSA keys")
        if not prime_p:
            prime_p = click.prompt("Prime p")
        if not prime_q:
            prime_q = click.prompt("Prime q")
        if not public_exponent:
            public_exponent = click.prompt("Public exponent")
    else:
        if prime_p:
            raise click.ClickException("-p/--prime-p may only be set for RSA keys")
        if prime_q:
            raise click.ClickException("-q/--prime-q may only be set for RSA keys")
        if public_exponent:
            raise click.ClickException("-e/--public-exponent may only be set for RSA keys")
        if not data:
            data = click.prompt("Key data")

    with connect(ctx) as nethsm:
        key_id = nethsm.add_key(
            key_id=key_id,
            algorithm=algorithm,
            mechanisms=mechanisms,
            prime_p=prime_p,
            prime_q=prime_q,
            public_exponent=public_exponent,
            data=data,
        )
        print(f"Key {key_id} added to NetHSM {nethsm.host}")


@nethsm.command()
@click.option(
    "-a",
    "--algorithm",
    type=ALGORITHM_TYPE,
    prompt=True,
    help="The algorithm for the generated key",
)
@click.option(
    "-m",
    "--mechanism",
    "mechanisms",
    type=MECHANISM_TYPE,
    multiple=True,
    help="The mechanisms for the generated key",
)
@click.option(
    "-l",
    "--length",
    type=int,
    prompt=True,
    help="The length of the generated key",
)
@click.option(
    "-k",
    "--key-id",
    help="The ID of the generated key",
)
@click.pass_context
def generate_key(ctx, algorithm, mechanisms, length, key_id):
    """Generate a key pair on the NetHSM.

    This command requires authentication as a user with the Administrator
    role."""
    mechanisms = list(mechanisms) or prompt_mechanisms(algorithm)
    with connect(ctx) as nethsm:
        key_id = nethsm.generate_key(algorithm, mechanisms, length, key_id)
        print(f"Key {key_id} generated on NetHSM {nethsm.host}")


@nethsm.command()
@click.option("--logging", is_flag=True, help="Query the logging configuration")
@click.option("--network", is_flag=True, help="Query the network configuration")
@click.option("--time", is_flag=True, help="Query the system time")
@click.option(
    "--unattended-boot", is_flag=True, help="Query the unattended boot configuration"
)
@click.option("--public-key", is_flag=True, help="Query the public key")
@click.option("--certificate", is_flag=True, help="Query the certificate")
@click.pass_context
def get_config(ctx, **kwargs):
    """Query the configuration of a NetHSM.

    Only the configuration items selected with the corresponding option are
    queried.  If no option is set, all items are queried.

    This command requires authentication as a user with the Administrator
    role."""
    with connect(ctx) as nethsm:
        print(f"Configuration for NetHSM {nethsm.host}:")
        show_all = not any(kwargs.values())

        if show_all or kwargs["logging"]:
            data = nethsm.get_config_logging()
            print("  Logging:")
            print("    IP address:   ", data.ip_address)
            print("    Port:         ", data.port)
            print("    Log level:    ", data.log_level)

        if show_all or kwargs["network"]:
            data = nethsm.get_config_network()
            print("  Network:")
            print("    IP address:   ", data.ip_address)
            print("    Netmask:      ", data.netmask)
            print("    Gateway:      ", data.gateway)

        if show_all or kwargs["time"]:
            time = nethsm.get_config_time()
            print("  Time:           ", time)

        if show_all or kwargs["unattended_boot"]:
            unattended_boot = nethsm.get_config_unattended_boot()
            print("  Unattended boot:", unattended_boot)

        if show_all or kwargs["public_key"]:
            public_key = nethsm.get_public_key()
            print("  Public key:")
            for line in public_key.splitlines():
                print(f"    {line}")

        if show_all or kwargs["certificate"]:
            certificate = nethsm.get_certificate()
            print("  Certificate:")
            for line in certificate.splitlines():
                print(f"    {line}")


@nethsm.command()
@click.option(
    "-p",
    "--passphrase",
    hide_input=True,
    confirmation_prompt=True,
    prompt=True,
    help="The new backup passphrase",
)
@click.pass_context
def set_backup_passphrase(ctx, passphrase):
    """Set the backup passphrase of a NetHSM.

    This command requires authentication as a user with the Administrator
    role."""
    with connect(ctx) as nethsm:
        nethsm.set_backup_passphrase(passphrase)
        print(f"Updated the backup passphrase for NetHSM {nethsm.host}")


@nethsm.command()
@click.option(
    "-p",
    "--passphrase",
    hide_input=True,
    confirmation_prompt=True,
    prompt=True,
    help="The new unlock passphrase",
)
@click.pass_context
def set_unlock_passphrase(ctx, passphrase):
    """Set the unlock passphrase of a NetHSM.

    This command requires authentication as a user with the Administrator
    role."""
    with connect(ctx) as nethsm:
        nethsm.set_unlock_passphrase(passphrase)
        print(f"Updated the unlock passphrase for NetHSM {nethsm.host}")


@nethsm.command()
@click.option(
    "-a",
    "--ip-address",
    help="The IP address of the new logging destination",
    required=True,
)
@click.option(
    "-p",
    "--port",
    type=int,
    help="The port of the new logging destination",
    required=True,
)
@click.option(
    "-l",
    "--log-level",
    type=LOG_LEVEL_TYPE,
    help="The new log level",
    required=True,
)
@click.pass_context
def set_logging_config(ctx, ip_address, port, log_level):
    """Set the logging configuration of a NetHSM.

    This command requires authentication as a user with the Administrator
    role."""
    with connect(ctx) as nethsm:
        nethsm.set_logging_config(ip_address, port, log_level)
        print(f"Updated the logging configuration for NetHSM {nethsm.host}")


@nethsm.command()
@click.option(
    "-a",
    "--ip-address",
    help="The new IP address",
    required=True,
)
@click.option(
    "-n",
    "--netmask",
    help="The new netmask",
    required=True,
)
@click.option(
    "-g",
    "--gateway",
    help="The new gateway",
    required=True,
)
@click.pass_context
def set_network_config(ctx, ip_address, netmask, gateway):
    """Set the network configuration of a NetHSM.

    This command requires authentication as a user with the Administrator
    role."""
    with connect(ctx) as nethsm:
        nethsm.set_network_config(ip_address, netmask, gateway)
        print(f"Updated the network configuration for NetHSM {nethsm.host}")


@nethsm.command()
@click.argument(
    "time",
    type=DATETIME_TYPE,
    required=False,
)
@click.pass_context
def set_time(ctx, time):
    """Set the system time of a NetHSM.

    If the time is not given as an argument, the system time of this system is used.

    This command requires authentication as a user with the Administrator
    role."""
    if not time:
        time = datetime.datetime.now(datetime.timezone.utc)
    with connect(ctx) as nethsm:
        nethsm.set_time(time)
        print(f"Updated the system time for NetHSM {nethsm.host}")


@nethsm.command()
@click.argument(
    "status",
    type=UNATTENDED_BOOT_STATUS_TYPE,
)
@click.pass_context
def set_unattended_boot(ctx, status):
    """Set the unattended boot configuration of a NetHSM.

    This command requires authentication as a user with the Administrator
    role."""
    with connect(ctx) as nethsm:
        nethsm.set_unattended_boot(status)
        print(f"Updated the unattended boot configuration for NetHSM {nethsm.host}")


@nethsm.command()
@click.pass_context
def system_info(ctx):
    """Get system information for a NetHSM instance.

    This command requires authentication as a user with the Administrator
    role."""
    with connect(ctx) as nethsm:
        info = nethsm.get_system_info()
        print(f"Host:             {nethsm.host}")
        print(f"Firmware version: {info.firmware_version}")
        print(f"Software version: {info.software_version}")
        print(f"Hardware version: {info.hardware_version}")
        print(f"Build tag:        {info.build_tag}")


@nethsm.command()
@click.pass_context
def reboot(ctx):
    """Reboot a NetHSM instance.

    This command requires authentication as a user with the Administrator
    role."""
    with connect(ctx) as nethsm:
        nethsm.reboot()
        print(f"NetHSM {nethsm.host} is about to reboot")


@nethsm.command()
@click.pass_context
def shutdown(ctx):
    """Shutdown a NetHSM instance.

    This command requires authentication as a user with the Administrator
    role."""
    with connect(ctx) as nethsm:
        nethsm.shutdown()
        print(f"NetHSM {nethsm.host} is about to shutdown")


@nethsm.command()
@click.pass_context
def reset(ctx):
    """Reset a NetHSM instance.

    This command requires authentication as a user with the Administrator
    role."""
    with connect(ctx) as nethsm:
        nethsm.reset()
        print(f"NetHSM {nethsm.host} is about to reset")


@nethsm.command()
@click.option(
    "-k",
    "--key-id",
    prompt=True,
    help="The ID of the key to decrypt the data width",
)
@click.option(
    "-d",
    "--data",
    prompt=True,
    help="The encrypted data in Base64 encoding",
)
@click.option(
    "-m",
    "--mode",
    type=DECRYPT_MODE_TYPE,
    prompt=True,
    help="The decrypt mode",
)
@click.pass_context
def decrypt(ctx, key_id, data, mode):
    """Decrypt data with a secret key on the NetHSM and print the decrypted message.

    This command requires authentication as a user with the Operator role."""
    with connect(ctx) as nethsm:
        print(nethsm.decrypt(key_id, data, mode))


@nethsm.command()
@click.option(
    "-k",
    "--key-id",
    prompt=True,
    help="The ID of the key to sign the data width",
)
@click.option(
    "-d",
    "--data",
    prompt=True,
    help="The data to sign encoded using Base64",
)
@click.option(
    "-m",
    "--mode",
    type=SIGN_MODE_TYPE,
    prompt=True,
    help="The sign mode",
)
@click.pass_context
def sign(ctx, key_id, data, mode):
    """Sign data with a secret key on the NetHSM and print the signature.

    This command requires authentication as a user with the Operator role."""
    with connect(ctx) as nethsm:
        signature = nethsm.sign(key_id, data, mode)
        print(signature)
