from . import setup_file
import re

def is_private_bot_channel(ctx):
    return True if "bot-" in ctx.message.channel.name and ctx.message.guild.id == 630872062310875176 else False


def is_owner(ctx):
    return str(ctx.message.author.id) == setup_file['discord']['owner_id']

def bot_admin(ctx):
    if is_owner(ctx):
        return True
    return str(ctx.message.author.id) in setup_file['discord']['admins']


def server_owner(ctx):
    if is_owner(ctx):
        return True
    if bot_admin(ctx):
        return True
    return ctx.message.author == ctx.message.guild.owner


def server_admin(ctx):
    if is_owner(ctx):
        return True
    if bot_admin(ctx):
        return True
    if server_owner(ctx):
        return True
    return ctx.message.author.guild_permissions.administrator