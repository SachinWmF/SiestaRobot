import html

from telegram.ext.filters import Filters
from telegram import Update, message, ParseMode
from telegram.ext import CallbackContext
from telegram.utils.helpers import mention_html

from EmikoRobot.modules.helper_funcs.decorators import emikocmd, emikomsg
from EmikoRobot.modules.helper_funcs.channel_mode import user_admin, AdminPerms
from EmikoRobot.modules.sql.antichannel_sql import antichannel_status, disable_antichannel, enable_antichannel
from EmikoRobot.modules.log_channel import gloggable, loggable


@emikocmd(command="antichannelmode", group=100)
@user_admin(AdminPerms.CAN_RESTRICT_MEMBERS)
def set_antichannel(update: Update, context: CallbackContext):
    message = update.effective_message
    chat = update.effective_chat
    args = context.args
    if len(args) > 0:
        s = args[0].lower()
        if s in ["yes", "on"]:
            enable_antichannel(chat.id)
            message.reply_html("Enabled antichannel in {}".format(html.escape(chat.title)))
        elif s in ["off", "no"]:
            disable_antichannel(chat.id)
            message.reply_html("Disabled antichannel in {}".format(html.escape(chat.title)))
        else:
            message.reply_text("Unrecognized arguments {}".format(s))
        return
    message.reply_html(
        "Antichannel setting is currently {} in {}".format(antichannel_status(chat.id), html.escape(chat.title)))

@emikomsg(Filters.chat_type.groups, group=110)
@loggable
def eliminate_channel(update: Update, context: CallbackContext):
    message = update.effective_message
    chat = update.effective_chat
    log_message = ""
    bot = context.bot
    if not antichannel_status(chat.id):
        return
    if message.sender_chat and message.sender_chat.type == "channel" and not message.is_automatic_forward:
        sender_chat = message.sender_chat
        r = bot.ban_chat_sender_chat(sender_chat_id=sender_chat.id, chat_id=chat.id)
        if r:
            message.reply_text("Channel {} was unbanned successfully from {}".format(
                html.escape(message.reply_to_message.sender_chat.title),
                html.escape(chat.title)
            ),
                parse_mode="html"
            )
    
    log = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        f"#BANNED_CHANNELS\n"
        f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
        f"<b>User:</b> {mention_html(member.user.id, html.escape(member.user.first_name))}"
    )  